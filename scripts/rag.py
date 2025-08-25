import pandas as pd
import minsearch
import ollama
from sentence_transformers import SentenceTransformer


def vsearch(query, num_results):
    vectorizer = SentenceTransformer(model_name_or_path='all-MiniLM-L6-v2')
    query_embedded = vectorizer.encode([query])
    search_result = vindex.search(query_embedded, num_results=num_results)
    return search_result

def kwsearch(query, num_results):
    boost = {'title' : 1.0, 'journal': 1.0, 'abstract': 2.0}
    results = kwindex.search(query=query, boost_dict=boost, \
    num_results=num_results)
    return results

def build_prompt(query, search_result):
    prompt_template = """
    You are an expert on autism spectrum disorders and Asperger's syndrome. 
    Answer the QUESTION based on the CONTEXT, a set of papers from PubMed. 
    Make sure to mention the relevant PubMed IDs (pmid) in your answer.
    If there are no relevant papers, say so.

    QUESTION: {question}
    CONTEXT: \n
    {context}
    """.strip()
    context = ''
    for record in search_result:
        context = context + f"pmid: {record['pmid']}\n\
        title: {record['title']}\njournal: {record['journal']}\nyear: \
        {record['year']}\nauthor: {record['author']}\naffiliation: \
        {record['affiliation']}\nabstract: {record['abstract']}\n\n"
    prompt = prompt_template.format(question=query, context=context)
    return prompt.strip()

def llm(prompt, model_handle_llm, seed=None):
    if seed:
        seed_dict = {'seed' : seed}
    else:
        seed_dict = None
    response = ollama.chat(model=model_handle_llm, messages=[{'role' : 'user', \
    'content' : prompt}], options=seed_dict)
    return response['message']['content']

def rag(query, do_vector_search, num_results, model_handle_llm, seed=None):
    if do_vector_search:
        search_result = vsearch(query, num_results)
    else:
        search_result = kwsearch(query, num_results)
    prompt = build_prompt(query, search_result)
    answer = llm(prompt, model_handle_llm, seed)
    return answer


# the knowledge base text
kb_df_filename = './data/data-kb.csv'
kb_df = pd.read_csv(kb_df_filename, sep='\t', dtype=str)
for column_name in kb_df.columns:
    kb_df[column_name] = kb_df[column_name].fillna('') # make NAs blank
kb_rec = kb_df.to_dict('records')

# the knowledge base vectors
vectors_filename = './data/embed-kb.csv'
vectors = pd.read_csv(vectors_filename, header=None, sep=',')

# the index (using vectors)
vindex = minsearch.VectorSearch(keyword_fields={'author', 'year'})
vindex.fit(vectors, kb_rec)
