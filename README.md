# terraphim-platform-pipeline
Cloud (python) based pipeline for Terraphim AI assistant

WIP: It's based on https://github.com/applied-knowledge-systems/the-pattern/ project and in the process of being rewritten to smaller, Rust based self-contained platform

## Overview

## Testing 
```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY  cord19medical "MATCH (e:entity)-[r]->(t:entity) where (e.role='project-manager') RETURN DISTINCT e.id,e.name,e.rank, e.role"
```

or 
```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY  cord19medical "MATCH (e:entity)-[r]->(t:entity) where (e.role='lazy-project-manager') RETURN DISTINCT e.id,e.name,e.rank, e.role"
```
