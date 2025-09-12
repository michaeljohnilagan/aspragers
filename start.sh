#!/bin/bash
echo 'AspRAGers is loading...'
ollama serve > /app/ollama.log 2>&1 &
sleep 5
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts
python -m cli