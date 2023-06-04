# terraphim-platform-pipeline
Cloud (python) based pipeline for Terraphim AI assistant

WIP: don't use - to be rewritten

## Overview

## Testing 
```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY  cord19medical "MATCH (e:entity)-[r]->(t:entity) where (e.role='project-manager') RETURN DISTINCT e.id,e.name,e.rank, e.role"
```

or 
```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY  cord19medical "MATCH (e:entity)-[r]->(t:entity) where (e.role='lazy-project-manager') RETURN DISTINCT e.id,e.name,e.rank, e.role"
```