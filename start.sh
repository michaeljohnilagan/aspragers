#!/bin/bash
echo 'AspRAGers is loading...'
pip install --no-cache-dir -q -r requirements.txt
ollama serve > /app/ollama.log 2>&1 &
sleep 5
ollama pull llama3.2:1b
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts
python -m cli