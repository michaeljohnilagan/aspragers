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

# download sentence transformer model
RUN python ./scripts/vectors.py

# install ollama
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
RUN tar -C /usr -xzf ollama-linux-amd64.tgz
RUN rm ollama-linux-amd64.tgz

# download LLM (code from github)
RUN ollama serve & sleep 5 ; ollama pull llama3.2:1b ; echo "kill ollama serve process" ; ps -ef | grep 'ollama serve' | grep -v grep | awk '{print $2}' | xargs -r kill -9

# allow viewing jupyter notebook on browser
EXPOSE 8888

# give permission for app to run
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]
