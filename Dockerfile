FROM python:3.10-bullseye

WORKDIR /app

COPY data/ ./data
COPY notebooks/ ./notebooks
COPY scripts/ ./scripts
COPY requirements.txt ./requirements.txt
COPY cli.py ./cli.py
COPY start.sh ./start.sh

RUN pip install --no-cache-dir -r requirements.txt

RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
RUN tar -C /usr -xzf ollama-linux-amd64.tgz

RUN chmod +x ./start.sh

ENTRYPOINT ["bash"]
