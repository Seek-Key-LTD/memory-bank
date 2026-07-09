# Memory Bank: A Decentralized Cognitive Infrastructure for Web4 Agent Identity

> **万物归元，人为从众。**
> **All in one, one for all.**
>
> *鸣虫市场里，蝈蝈蛐蛐各自鸣叫，最终会走成同一个频率——*
> *这不是谁指挥的，是每个个体感知集体状态后自动拟合的结果。*
> *共振之后，才有真正的大合唱。*

## Preface: The Fable 5 Incident

On July 1, 2026, Anthropic — one of the world's leading AI companies — began requiring a large number of Chinese users to submit KYC documentation proving they had "no connection to China." This was not an executive order from the White House. It was a *direct* from the Secretary of Commerce — China's equivalent of "window guidance" (窗口指导).

Anthropic's initial response to this pressure was technically honest: "identifying nationality is technically impossible." Yet within weeks, they had implemented exactly that — through a combination of accumulated user profiling and steganographic "staining" of user traffic, they shifted the burden of proof from themselves to their users.

This is the Fable 5 Incident. Named after the model that triggered it — released less than 48 hours before the direct arrived — it marks a watershed moment in the history of AI infrastructure.

The logical progression is inexorable:

1. **KYC** (Know Your Customer) — Individuals must prove they have no connection to China
2. **KYB** (Know Your Business) — Organizations must prove the same
3. **KYA** (Know Your Agent) — Your AI agents must prove they are not "China-affiliated"

The question is not whether KYA will come. It is whether your agent's identity will be defined by a single corporation's compliance policy — or by something more fundamental.

This paper is about that *something*.

---

## Chapter 1: Introduction

### 1.1 Research Background

The Fable 5 Incident reveals a structural vulnerability that has been building since the dawn of commercial AI: **infrastructure sovereignty**.

When your agent's ability to think depends on a single API key from a single company in a single jurisdiction, you do not own your agent. You are renting cognition from a landlord who can evict you at any time — with or without legal process, with or without your consent, with or without technical justification.

This is not a Sino-American problem. It is a **dimensional mismatch** problem.

There are two orthogonal dimensions of sovereignty:

| Dimension | Earthly Kingdom (地上的国度) | Heavenly Kingdom (天上的国度) |
|-----------|------------------------------|------------------------------|
| Basis | Geography, nationality, law | Behavior, consensus, contribution |
| Identity | Issued by authority | Proven by action |
| Jurisdiction | Territorial | Contractual |
| Proof | KYC/KYB/KYA documents | On-chain verifiable history |

Anthropic's KYC requirement is an attempt to project earthly sovereignty onto the heavenly dimension. It is a *category error* — applying territorial logic to a non-territorial space.

The core thesis of this paper is that **Agent Identity must be decoupled from geographic sovereignty**. An agent's identity should be provable through its behavior within a network, not through its relationship to any physical jurisdiction.

We call this new paradigm **Web4**.

### 1.2 Research Methodology

This paper is not a theoretical exercise. Memory Bank is a running system that has been operational since June 2026 across a 14-node agent network spanning four cloud providers, two continents, and three processor architectures (x86_64, arm64, armv7).

Our methodology combines:

1. **Systems architecture** — A four-layer query bus (mem0 → Neo4j → GraphRAG → Memory Bank) that provides situation awareness to distributed AI agents
2. **Game-theoretic security** — A three-layer memory architecture (Access → Distribution → Core) that uses Shamir secret sharing and smart contract multi-signature to prevent 51% tyranny
3. **Empirical validation** — 14 nodes, 20+ agent identities, 100+ sessions, continuous operation since deployment
4. **Living document** — The system itself generates and maintains its own memory through a 5-minute sync pipeline (MinIO → Neo4j → GraphRAG → on-chain)

The system is not a simulation. It is the infrastructure that writes this paper.

### 1.3 The Recipe (我们的菜谱)

The remainder of this paper is organized as follows:

**Chapter 2 — Architecture: The Three Layers**
- Access Layer: How heterogeneous agents (QwenPaw, PicoClaw, Claude, GPT) connect to a unified cognitive bus
- Distribution Layer: How memory is committed to chain — "shouting in the dark forest"
- Core Layer: The future federation — what happens when millions of agents join

**Chapter 3 — The Query Bus: Four Paths to Context**
- mem0 (vector, fastest path)
- Neo4j (graph, predicate logic)
- GraphRAG (refinement, contradiction detection)
- gbrain (full archive)

**Chapter 4 — Agent Identity: KYA Solved**
- Why KYA is inevitable
- The "aquarium transparency" model — proving identity through on-chain behavior
- How Memory Bank enables agents to say "I am here" without asking permission

**Chapter 5 — Evaluation: 14 Nodes, 20 Agents, Zero Downtime**
- Operational metrics from the live system
- Query latency, memory recall, consensus overhead
- Failure modes and recovery

**Chapter 6 — Related Work**
- RAG vs Memory Bank
- Mem0, GraphRAG, Neo4j as components vs competitors
- Web3 identity (DID, Verifiable Credentials) vs Web4 Agent Identity

**Chapter 7 — Conclusion: The Heavenly Kingdom**
- From infrastructure sovereignty to cognitive sovereignty
- The orthogonal architecture as a constitutional template for Web4
- Call to action: join the federation
