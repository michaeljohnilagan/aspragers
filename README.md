# AspRAGers

There is misinformation online about Asperger's syndrome or autism spectrum disorders.
We want our information based on published research papers.

The present project **AspRAGers** is a chatbot that answers questions about Asperger's syndrome or autism spectrum disorders, based on abstracts of relevant papers on PubMed.
The "RAG" in the name stands for "retrieval-augmented generation".

As with any large language model (LLM), beware that correctness of the chatbot's response is not guaranteed.

The present project was submitted to DataTalks.Club's [LLM Zoomcamp](https://datatalks.club/courses/llm-zoomcamp/) for its 2025 Cohort.

## Dataset

The knowledge base contains information from a set of articles on PubMed.
Each article (row of the data table) has the following fields (columns of the data table):

* PMID (a unique integer ID on PubMed)
* The article title
* The journal title
* The authors' names
* The authors' affiliations
* The article's abstract

The dataset was pulled programmatically from PubMed. 
You can find the tabular data in [`data/data-kb.csv`](data/data-kb.csv).
To refresh the data (or verify its reproducibility), more details below.
For semantic search, embeddings for the papers in the dataset can be found in [`data/embed-kb.csv`](data/embed-kb.csv).

## Technologies

* Python 3.10
* [Docker](https://docker.com) for containerization
* For vector search, [Sentence Transformers](https://www.sbert.net/) (also known as SBERT) and [Minsearch](https://github.com/alexeygrigorev/minsearch)
* [Ollama](https://ollama.com/) for the local LLM (so there is no need for an API key)

## Running the application

### Running with Docker

To build the Docker image and run it, do as follows.

```bash
docker build -t aspragers .
docker run -it aspragers
```

## Using the application

To use the application, we have a command line interface (CLI).

To ask the chatbot a question, do as follows.
It starts the Ollama process and executes the Python CLI script.

```bash
./start.sh
```

You can see how the data was originally produced by following the notebooks [`notebooks/ingest.ipynb`](notebooks/ingest.ipynb) and [`notebooks/embed-kb.ipynb`](notebooks/embed-kb.ipynb).
To refresh the data, you can convert these notebooks to Python scripts and run them.
Precisely, do as follows.

```bash
cd notebooks
jupyter nbconvert --to script ingest.ipynb
python ingest.py
jupyter nbconvert --to script embed-kb.ipynb
python embed-kb.py
```
