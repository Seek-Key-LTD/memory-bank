-- =============================================================================
-- Apache AGE (PostgreSQL 18) OpenCypher 实体因果与时序拓扑模板
-- =============================================================================

-- 1. 初始化图空间
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
SELECT create_graph('kunpengzhi_canon_graph');

-- 2. 插入学者席位与身世前世记忆
SELECT * FROM cypher('kunpengzhi_canon_graph', $$
  CREATE (putuo:Scholar {
    name: '老林',
    code_name: '普陀',
    voice_tag: 'zh-sh-fudan-calm',
    alma_mater: '复旦大学哲学系',
    monastic_years: 8,
    surgery_site: '成都华西医院',
    seat_status: '新加坡滨海湾独立对冲基金合伙人'
  })
  CREATE (yuyang:Scholar {
    name: '老于',
    code_name: '渔阳',
    voice_tag: 'zh-bj-hutong-accountant',
    abacus_rate_hz: 8,
    discipline: '制度经济学与财政史'
  })
  CREATE (zhuhu:Scholar {
    name: '竺教授',
    code_name: '竹湖',
    voice_tag: 'zh-tw-intellectual-soft',
    origin: '山西五台县老兵二代',
    station: '台湾清华大学人社院'
  })
$$) as (v agtype);

-- 3. 插入历史事件与因果依赖边
SELECT * FROM cypher('kunpengzhi_canon_graph', $$
  CREATE (e_1949:Event {event_id: 'E_1949_RETREAT', epoch_year: 1949, title: '晋绥军南撤抵台'})
  CREATE (e_1986:Event {event_id: 'E_1986_AIRLINER', epoch_year: 1986, title: '华航王锡爵降落广州白云机场'})
  CREATE (e_1987:Event {event_id: 'E_1987_VISIT', epoch_year: 1987, title: '竹湖陪老父借道香港回五台山老家探亲'})
  
  CREATE (e_1949)-[:OCCURRED_BEFORE {delta_years: 37}]->(e_1986)
  CREATE (e_1986)-[:OCCURRED_BEFORE {delta_years: 1}]->(e_1987)
$$) as (v agtype);

-- 4. 时序因果违规检测查询 (用于 CI 自动化拦截)
SELECT * FROM cypher('kunpengzhi_canon_graph', $$
  MATCH (a:Event)-[r:OCCURRED_BEFORE]->(b:Event)
  WHERE a.epoch_year > b.epoch_year
  RETURN a.title AS antecedent, a.epoch_year, b.title AS consequent, b.epoch_year
$$) as (antecedent agtype, ant_year agtype, consequent agtype, con_year agtype);
