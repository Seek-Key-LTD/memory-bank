# 记忆银行：可观察性分层设计与链路监测方案 (Observability Architecture)

> 版本：v1.0 | 2026-07-13  
> 作者：觅钥科技 (Seekkey) & Antigravity  
> 定位：记忆银行三层认知架构的“温度计”与“内窥镜”  

---

## 1 整体分层拓扑 (Hierarchy Topology)

记忆银行通过 Grafana 体系的“三驾马车”实现指标 (Metrics)、日志 (Logs) 和追踪 (Traces) 的三维一体化监测。整体架构分为四层：

```
┌────────────────────────────────────────────────────────┐
│                   1. 认知产生层 (Zodiac Agents)         │
│  - gbrain (PostgreSQL)  - Neo4j (图数据库)  - GraphRAG   │
└──────────────┬──────────────────┬──────────────┬───────┘
               │ (PromMetrics)    │ (OTLP/gRPC)  │ (Stdout/Journal)
               ▼                  ▼              ▼
┌────────────────────────────────────────────────────────┐
│                   2. 统一收集层 (Grafana Alloy)        │
│  - prometheus.scrape     - otelcol.receiver    - journal│
└──────────────────────────┬─────────────────────────────┘
                           │ (Remote Write / OTLP / Push)
                           ▼
┌────────────────────────────────────────────────────────┐
│                   3. 存储存储层 (Storage Backends)      │
│  - VictoriaMetrics        - Grafana Tempo     - Loki   │
│    (指标时序)              (Trace 链路数据)    (日志数据)│
└──────────────────────────┬─────────────────────────────┘
                           │ (数据源查询)
                           ▼
┌────────────────────────────────────────────────────────┐
│                   4. 可视化呈现层 (Grafana UI)          │
│  - Prometheus DS          - Tempo DS          - Loki DS│
│  - 仪表盘与大屏图表        - 链路甘特图展示    - 联动日志查询│
└────────────────────────────────────────────────────────┘
```

---

## 2 监控维度与技术栈选型

| 维度 (Pillar) | 生产源 (Sources) | 收集器 (Collector) | 存储器 (Backend) | 展现层 (Visualization) | 核心价值 (Value) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **指标 (Metrics)** | Neo4j (Port 2004)、gbrain (PostgreSQL) | Grafana Alloy (`prometheus.scrape`) | VictoriaMetrics (PMM) | Grafana (PromQL) | 监控记忆体增长、系统健康度与对齐冲突率 |
| **链路 (Traces)** | GraphRAG 提纯管道、智能体调用链 | Grafana Alloy (`otelcol.receiver`) | **Grafana Tempo** | Grafana (Trace View) | 展示“提纯”全链路时间线，定位慢模型与执行瓶颈 |
| **日志 (Logs)** | 宿主机/容器系统日志与 Agent 业务日志 | Grafana Alloy (`loki.source.journal`) | Loki | Grafana (LogQL) | 采集底层组件异常，与 Trace ID 实现无缝双向联动 |

---

## 3 详细执行规划 (Execution Plan)

### 3.1 接入层配置 (Zodiac Agents)
1. **Neo4j 监控开启**：
   在 Neo4j 主机配置文件 `neo4j.conf` 中激活 Prometheus 接口：
   ```properties
   server.metrics.prometheus.enabled=true
   server.metrics.prometheus.endpoint=0.0.0.0:2004
   ```
2. **GraphRAG 链路打标**：
   在 GraphRAG 核心执行流中引入 OpenTelemetry Python SDK，并在每个提纯节点（Peeling -> Slicing -> Aligning）打上 Trace Span 标记，最终通过 OTLP 协议将 Span 导出至 `localhost:4317` (Alloy 端口)。

### 3.2 收集层配置 (Grafana Alloy)
修改各节点的 `/etc/alloy/config.alloy`，追加 Neo4j 抓取器和 OTel 接收器：
```alloy
// 1. 抓取 Neo4j metrics 指标
prometheus.scrape "neo4j_metrics" {
  targets = [{"__address__" = "localhost:2004"}]
  forward_to = [prometheus.remote_write.pmm.receiver]
  job_name = "neo4j"
  scrape_interval = "15s"
}

// 2. 接收 GraphRAG / Agents 链路 Traces
otelcol.receiver.otlp "default" {
  grpc {
    endpoint = "0.0.0.0:4317"
  }
  http {
    endpoint = "0.0.0.0:4318"
  }
  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}

// 3. 链路追踪数据转发至 Tempo
otelcol.exporter.otlp "tempo" {
  client {
    endpoint = "tempo.capitaltrain.cn:4317" // 或实际 Tempo OTLP 接收地址
  }
}
```

### 3.3 展现层集成 (Grafana)
1. 在 Grafana 中新建数据源，选择 **Tempo**，配置 URL 指向 Tempo 服务的 API 接口。
2. 配置 **Trace-to-Logs** 关联，在查看 Trace 链路时，自动带入 `traceID` 查询对应的 Loki 日志，达到“Trace 中看时间耗时，Log 中看详细报错”的无缝联动效果。
