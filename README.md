# AspRAGers

There is misinformation online about Asperger's syndrome or autism spectrum disorders.
We want our information based on published research papers.

The present project **AspRAGers** is a chatbot that answers questions about autism spectrum disorders, based on abstracts of relevant papers on PubMed.
The "RAG" in the name stands for "retrieval-augmented generation".
Note that AspRAGers reads only abstracts, not the main text.

As with any large language model (LLM), beware that correctness of the chatbot's response is not guaranteed.
Think of the response as a starting point to do your own research.

The present project was submitted to DataTalks.Club's [LLM Zoomcamp](https://datatalks.club/courses/llm-zoomcamp/) for its 2025 Cohort.

<p align="center"><a href="https://drive.google.com/file/d/117hb0OvfXsDn3lVaJr-8iMohv8SAt80v/view?usp=sharing">Demo video</a></p>

## Dataset

The dataset contains bibliographic information from a set of articles on PubMed.
Each article (row of the data table) has the following fields (columns of the data table):

* The unique PubMed ID (PMID)
* The article title
* The journal title
* The authors' names
* The authors' affiliations
* The article's abstract

The dataset was pulled programmatically from PubMed. 
You can find the tabular data in [`data/data.csv`](data/data.csv).
AspRAGers has functionality to refresh the data (more details below).

## Technologies

* Python 3.10
* [Docker](https://docker.com) for containerization
* For keyword search, [Minsearch](https://github.com/alexeygrigorev/minsearch)
* For semantic/vector search, [Sentence Transformers](https://www.sbert.net/) (also known as SBERT) and Minsearch
* [Ollama](https://ollama.com/) for the local LLM, particularly the 1B version of Llama 3.2 (`llama3.2:1b`)

## Running the application

### Running with Docker

The whole app is in one Docker image.
Building the image installs all the dependencies.

```bash
docker build -t aspragers .
```

The command line interface (CLI) allows you to talk to the chatbot.

```bash
docker run -it aspragers
```

Otherwise, you may want to re-query PubMed (to refresh the data), re-run the evaluation experiments, edit settings in the scripts, or download a different Ollama model.
In that case, you will need a Bash shell with Jupyter notebooks.

```bash
docker run -it -p 8888:8888 --entrypoint /bin/bash aspragers
```

Because a local LLM is used, there is no need for an API key.

## Using the application

### Talking to the chatbot

The CLI is intuitive.
You can ask the chatbot your own question, or you can randomly draw a question from the dataset of LLM-generated questions.
The synthetic questions are in [`data/data-synth-question.csv`](data/data-synth-question.csv).

From the shell, you can talk to the chatbot by executing the start script.

```bash
./start.sh
```

### Using a different Ollama model

From the shell, you can download the Ollama model `gemma3:1b` for example.
See [Ollama's catalog](https://ollama.com/models) for more models.

```bash
ollama serve > /app/ollama.log 2>&1 &
ollama pull gemma3:1b
```

If you want to use an Ollama model you just downloaded, you must make the change in [`cli.py`](cli.py).

### Playing with the Jupyter notebooks

From the shell, you can open Jupyter.

```bash
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

Follow the notebooks (more details below) to query PubMed or run the evaluation experiments.
Note that some of the notebooks produce CSV files that the app depends on.

### Other settings that can be changed

In [`cli.py`](cli.py), you can change the RAG behavior:

* Whether to do semantic/vector search (`do_vector_search`), versus keyword search
* How many documents are retrieved (`num_results`)
* Which Ollama model to use (`model_handle_llm`), but make sure you pull the model first

If doing semantic/vector search, in [`scripts/vectors.py`](scripts/vectors.py) you can change which SBERT model (`model_handle`) is used to vectorize documents.

## Code

The main code for the application is in the following scripts.

* [`cli.py`](cli.py) has the logic of the CLI
* [`scripts/vectors.py`](scripts/vectors.py) instantiates the SBERT model used to vectorize documents and queries
* [`scripts/ingest.py`](scripts/ingest.py) defines functions used to ingest the data
* [`scripts/rag.py`](scripts/rag.py) has the main RAG flow

The data files are ingested into Minsearch when [`cli.py`](cli.py) imports [`scripts/rag.py`](scripts/rag.py).

The data can be manually refreshed by running the following notebooks.

* [`notebooks/pubmed.ipynb`](notebooks/pubmed.ipynb) queries PubMed for the documents
* [`notebooks/embed.ipynb`](notebooks/embed.ipynb) vectorizes the documents queried

## Experiments

Evaluation was done in the following notebooks.

* [`notebooks/synth-question.ipynb`](notebooks/synth-question.ipynb) has the LLM generate questions to be used
* [`notebooks/eval-retriever.ipynb`](notebooks/eval-retriever.ipynb) compares semantic/vector search vs. lexical/keyword search for the retriever, by hit rate and mean reciprocal rank (MRR)
* [`notebooks/synth-answer.ipynb`](notebooks/synth-answer.ipynb) answers the LLM-generated questions, using Ollama models `llama3.2:1b` vs. `gemma3:1b`, given a chosen retriever from the previous notebook
* [`notebooks/eval-fullrag.ipynb`](notebooks/eval-fullrag.ipynb) compares the two Ollama models, by cosine similarity to the abstract

Number of documents retrieved was fixed at 5---no optimization.

### Retrieval evaluation

The preferred retriever was keyword search.
It had hit rate of 47% and MRR of 39%.
Note that the low metrics can be attributed to the questions being vague that multiple articles might actually be relevant to each question.

### RAG flow evaluation

The preferred Ollama model was `llama3.2:1b`.
Its mean cosine similarity was 0.65.

