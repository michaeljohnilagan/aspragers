#!/bin/bash
echo 'AspRAGers is loading...'
ollama serve > /app/ollama.log 2>&1 &
sleep 5
ollama pull llama3.2:1b
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts
python -m cli