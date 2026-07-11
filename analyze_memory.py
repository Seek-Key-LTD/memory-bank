#!/usr/bin/env python3
"""memory-ops: 灌入 Agent 记忆到 Neo4j 做图分析"""

import os, re, json, hashlib
from pathlib import Path
from datetime import datetime
from minio import Minio
from neo4j import GraphDatabase

MINIO_EP = os.getenv("MINIO_EP", "localhost:9000")
MINIO_KEY = os.getenv("MINIO_KEY", "")
MINIO_SECRET = os.getenv("MINIO_SECRET", "")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "agents")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")

mc = Minio(MINIO_EP, MINIO_KEY, MINIO_SECRET, secure=False)
neo4j = GraphDatabase.driver(NEO4J_URI)

def list_markdown():
    """List all .md files in the agents bucket"""
    files = []
    for obj in mc.list_objects(MINIO_BUCKET, recursive=True):
        if obj.object_name.endswith(".md"):
            files.append(obj.object_name)
    return sorted(files)

def read_file(path):
    resp = mc.get_object(MINIO_BUCKET, path)
    return resp.read().decode("utf-8")

def parse_agent(path):
    parts = path.split("/")
    return parts[0] if len(parts) >= 1 and parts[0] != "COLLECTIVE_MEMORY.md" else "collective"

def build_graph():
    with neo4j.session() as s:
        s.run("MATCH (n) DETACH DELETE n")
        print("Cleared existing graph")

    files = list_markdown()
    print(f"Found {len(files)} markdown files")

    for fpath in files:
        agent = parse_agent(fpath)
        content = read_file(fpath)
        doc_id = hashlib.md5(fpath.encode()).hexdigest()[:12]

        title_match = re.search(r"^# (.+)$", content, re.M)
        title = title_match.group(1) if title_match else Path(fpath).stem

        with neo4j.session() as s:
            s.run(
                """MERGE (a:Agent {name: $agent})
                   MERGE (d:Document {id: $doc_id})
                   SET d.title = $title, d.path = $path, d.agent = $agent, d.content = $content, d.ingested = datetime()
                   MERGE (d)-[:BELONGS_TO]->(a)""",
                agent=agent, doc_id=doc_id, title=title, path=fpath, content=content
            )

        headers = re.findall(r"^(#{1,4}) (.+)$", content, re.M)
        for level, heading in headers:
            concept_id = hashlib.md5(f"{agent}:{heading}".encode()).hexdigest()[:12]
            with neo4j.session() as s:
                s.run(
                    """MERGE (c:Concept {id: $cid})
                       SET c.name = $name, c.level = $level
                       MERGE (d:Document {id: $did})
                       MERGE (d)-[:MENTIONS]->(c)""",
                    cid=concept_id, name=heading.strip(), level=len(level), did=doc_id
                )

        links = re.findall(r"\[\[(.+?)\]\]", content)
        for link in links:
            link_id = hashlib.md5(link.encode()).hexdigest()[:12]
            with neo4j.session() as s:
                s.run(
                    """MERGE (c:Concept {id: $cid})
                       SET c.name = $name
                       MERGE (d:Document {id: $did})
                       MERGE (d)-[:LINKS_TO]->(c)""",
                    cid=link_id, name=link.strip(), did=doc_id
                )

    print(f"Ingested {len(files)} documents into Neo4j")

def query_agent_memories(agent_name):
    with neo4j.session() as s:
        result = s.run(
            """MATCH (a:Agent {name: $agent})<-[:BELONGS_TO]-(d:Document)
               RETURN d.title, d.path, d.ingested
               ORDER BY d.ingested DESC LIMIT 10""",
            agent=agent_name
        )
        for row in result:
            print(f"  {row['d.title']:40s} {row['d.path']}")

if __name__ == "__main__":
    build_graph()
    print("\n--- Memory by Agent ---")
    agents = ["nuc", "mini", "ruby", "topaz", "ash3c", "ch4"]
    for a in agents:
        print(f"\n[{a}]")
        query_agent_memories(a)
