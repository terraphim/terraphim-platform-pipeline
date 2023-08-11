#!/bin/bash
echo $(hostname -I) redisgraph | sudo tee -a /etc/hosts
echo $(hostname -I) rgcluster | sudo tee -a /etc/hosts
cd (/code/terraphim-platform-pipeline/ && bash /code/terraphim-platform-pipeline/cluster_pipeline_stream_prod.sh) & 