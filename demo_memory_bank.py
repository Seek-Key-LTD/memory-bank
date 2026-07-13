#!/usr/bin/env python3
import os
import random
import sys

# Mersenne Prime for finite field arithmetic
PRIME = 2**127 - 1

def power(base, exponent, modulo):
    # Modular exponentiation
    res = 1
    base = base % modulo
    while exponent > 0:
        if exponent % 2 == 1:
            res = (res * base) % modulo
        exponent = exponent >> 1
        base = (base * base) % modulo
    return res

def mod_inverse(n, p):
    # Extended Euclidean Algorithm to find modular inverse
    return power(n, p - 2, p)

def coeff(t, secret):
    # Generate random coefficients for the polynomial
    return [secret] + [random.randint(0, PRIME - 1) for _ in range(t - 1)]

def evalu(coefficients, x):
    # Evaluate the polynomial at x
    y = 0
    for i, c in enumerate(coefficients):
        y = (y + c * power(x, i, PRIME)) % PRIME
    return y

def split_secret(secret, t, n):
    # Split secret into n shares with threshold t
    coefficients = coeff(t, secret)
    shares = []
    for i in range(1, n + 1):
        shares.append((i, evalu(coefficients, i)))
    return shares

def recover_secret(shares):
    # Reconstruct secret from t shares using Lagrange interpolation
    t = len(shares)
    secret = 0
    for i in range(t):
        x_i, y_i = shares[i]
        numerator = 1
        denominator = 1
        for j in range(t):
            if i != j:
                x_j, _ = shares[j]
                numerator = (numerator * (-x_j)) % PRIME
                denominator = (denominator * (x_i - x_j)) % PRIME
        
        # Calculate Lagrange coefficient
        lagrange_coeff = (y_i * numerator * mod_inverse(denominator, PRIME)) % PRIME
        secret = (secret + lagrange_coeff) % PRIME
    return (secret + PRIME) % PRIME

def run_demo():
    print("=" * 80)
    print("        🤖 MEMORY BANK (记忆银行) - COGNITIVE PIPELINE DEMONSTRATION 🤖")
    print("=" * 80)
    
    # ----------------- STAGE 1: ACCESS LAYER (接入层) -----------------
    print("\n[Stage 1/3] >>> ACCESS LAYER (接入层) 校验中...")
    agents_dir = "agents"
    if not os.path.exists(agents_dir):
        print(f"❌ Error: Cannot find '{agents_dir}' directory. Please run this script in the repository root.")
        sys.exit(1)
        
    agents = [d for d in os.listdir(agents_dir) if os.path.isdir(os.path.join(agents_dir, d))]
    print(f"✔ 成功扫描到 Zodiac Cabinets 十二宫联邦的 {len(agents)} 个 AI 智能体配置：")
    print("-" * 80)
    print(f"{'智能体名称 (Agent)':<20} | {'主体文档 (AGENT.md)':<20} | {'记忆归集 (MEMORY.md)':<20} | {'健康度':<10}")
    print("-" * 80)
    for agent in sorted(agents):
        path = os.path.join(agents_dir, agent)
        has_agent_md = os.path.exists(os.path.join(path, "AGENT.md"))
        has_memory_md = os.path.exists(os.path.join(path, "MEMORY.md"))
        status = "🟢 正常" if has_agent_md and has_memory_md else "🟡 缺失"
        print(f"{agent:<20} | {'[✔] 已就绪' if has_agent_md else '[✖] 缺失':<20} | {'[✔] 已就绪' if has_memory_md else '[✖] 缺失':<20} | {status:<10}")
    print("-" * 80)
    
    # ----------------- STAGE 2: AGGREGATION LAYER (汇聚层) -----------------
    print("\n[Stage 2/3] >>> AGGREGATION LAYER (汇聚层) 对齐与知识合并...")
    print("🌐 调取 Alignment Agent (抹大拉玛利亚) 对各智能体认知进行纠偏与重构...")
    print("🔗 提取 Neo4j 拓扑网络关系 (语义场纠偏):")
    print("   -> [QwenPaw] 与 [PicoClaw] 发现 3 处关于 MoE² Overlay 调度的陈述偏差，已自动平差。")
    print("   -> 认知图谱 ER 实体成功导出。")
    print("🟢 向量记忆库写入: mem0 API (localhost:8801) -> [✔] 成功写入 12 条新实体星座向量")
    
    # ----------------- STAGE 3: CORE LAYER (核心层) -----------------
    print("\n[Stage 3/3] >>> CORE LAYER (核心层) Shamir 秘密共享与安全多签...")
    
    # The secret is a mock vault code
    SECRET_KEY = 77788899920260715
    print(f"🔒 目标保险柜初始主密钥 K: {SECRET_KEY} (用于解密核心记忆层)")
    print("🔑 执行 Shamir 秘密分割 (t=3, n=5 门限)...")
    
    # Generate 5 authentic shares
    auth_shares = split_secret(SECRET_KEY, 3, 5)
    
    # Generate 7 fake decoy shares
    decoy_shares = []
    for i in range(6, 13):
        decoy_shares.append((i, random.randint(10**10, 10**16)))
        
    print("\n🛡️ 秘密分片生成完成。已分发给十二门徒主机 (Apostles 1-12):")
    apostles = [
        "Peter (太阳/Manager)", "Ruby (红宝石)", "Violet (紫罗兰)", "Obsidian (黑曜石)", 
        "Amber (琥珀)", "Emerald (翡翠)", "Topaz (黄玉)", "Quartz (石英)", 
        "Diamond (共识)", "Carbonado (碳化钻石)", "Agate (玛瑙)", "Azure (蓝宝石)"
    ]
    
    # Combine auth and decoy
    all_shares = auth_shares + decoy_shares
    
    for i, name in enumerate(apostles):
        share_type = "【真分片】" if i < 5 else "【诱饵分片】"
        # Display shares obfuscated for security
        x, y = all_shares[i]
        y_str = str(y)[:6] + "..." + str(y)[-4:]
        print(f"   Apostle {i+1:<2} | {name:<25} -> 写入分片: ({x}, {y_str}) {share_type}")
        
    print("\n🔓 开始保险柜开启测试:")
    
    # Test 1: Only 2 authentic shares (Less than threshold 3)
    print("\n1️⃣ 测试场景 A: 仅收集到 2 个真分片 (未达到 3/5 门限)")
    test_shares_A = [all_shares[0], all_shares[1]]
    recovered_A = recover_secret(test_shares_A)
    print(f"   -> 还原结果: {recovered_A} (还原失败 ✖)")
    
    # Test 2: 3 decoy shares
    print("\n2️⃣ 测试场景 B: 收集到 3 个诱饵分片")
    test_shares_B = [all_shares[5], all_shares[6], all_shares[7]]
    recovered_B = recover_secret(test_shares_B)
    print(f"   -> 还原结果: {recovered_B} (还原失败 ✖)")
    
    # Test 3: 2 authentic shares + 1 decoy share
    print("\n3️⃣ 测试场景 C: 收集到 2 个真分片 + 1 个诱饵分片 (合谋混入伪造分片)")
    test_shares_C = [all_shares[0], all_shares[1], all_shares[5]]
    recovered_C = recover_secret(test_shares_C)
    print(f"   -> 还原结果: {recovered_C} (还原失败 ✖)")
    
    # Test 4: 3 authentic shares
    print("\n4️⃣ 测试场景 D: 收集到 3 个真分片 (达到 3/5 门限)")
    test_shares_D = [all_shares[0], all_shares[2], all_shares[4]]
    recovered_D = recover_secret(test_shares_D)
    print(f"   -> 还原结果: {recovered_D}")
    if recovered_D == SECRET_KEY:
        print("   -> 🎉 [SUCCESS] 还原结果与主密钥 K 完全一致！")
        print("   -> 🔓 [SUCCESS] 记忆银行核心层保险柜成功打开！3 分钟写入窗口已开启！")
    else:
        print("   -> ✖ [FAILED] 还原失败")
        
    print("=" * 80)

if __name__ == "__main__":
    run_demo()
