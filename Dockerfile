FROM python:3.10-bullseye

WORKDIR /app

# files to be used
COPY data/ ./data
COPY notebooks/ ./notebooks
COPY scripts/ ./scripts
COPY requirements.txt ./requirements.txt
COPY cli.py ./cli.py
COPY start.sh ./start.sh

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# install ollama
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
RUN tar -C /usr -xzf ollama-linux-amd64.tgz

# give permission for app to run
RUN chmod +x ./start.sh

ENTRYPOINT ["bash"]
