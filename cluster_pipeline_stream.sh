#!/bin/bash
gears-cli run --host 127.0.0.1 --port 30001 set_debug_key.py
gears-cli run --host 127.0.0.1 --port 30001 gears_pipeline_sentence_register.py --requirements requirements_gears_pipeline.txt
echo "NLP Pipeline registered."
gears-cli run --host 127.0.0.1 --port 30001 edges_to_graph_streamed.py --requirements requirements_gears_graph.txt
echo "edges_to_graph_streamed.py registered"
# echo "10 seconds for cluster to recover"
# sleep 10
# gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_register_medical.py --requirements requirements_all.txt
# echo "sentences_matcher_register_medical.py registered."
# gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_register_project_lazy.py --requirements requirements_all.txt
# echo "sentences_matcher_register_project_lazy.py registered."
# gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_register_project.py --requirements requirements_all.txt
# echo "sentences_matcher_register_project.py registered."
# gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_register_cyber.py --requirements requirements_all.txt
gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_register_operator.py --requirements requirements_all.txt
# gears-cli run --host 127.0.0.1 --port 30001 sentences_matcher_run_project.py --requirements requirements_gears_aho.txt
# sleep 10
# echo "Kick off matching"
# echo "Submit 25 articles into pipeline" 
# python3 RedisIntakeRedisClusterSample.py --nsamples 25


