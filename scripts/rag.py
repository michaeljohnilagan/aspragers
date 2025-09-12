import pandas as pd
import minsearch
import ollama
import os
import vectors


def vsearch(query, num_results):
    query_embedded = vectors.model.encode([query])
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

def get_kb_records(filename):
    df = pd.read_csv(filename, sep='\t', dtype=str)
    for column_name in df.columns:
        df[column_name] = df[column_name].fillna('') # make NAs blank
    kb_records = df.to_dict('records')
    return kb_records
    
def make_index_vector(kb_filename, vectors_filename):
    kb_records = get_kb_records(kb_filename)
    vectors = pd.read_csv(vectors_filename, header=None, sep=',')
    vindex = minsearch.VectorSearch(keyword_fields={'author', 'year'})
    vindex.fit(vectors, kb_records)
    return vindex

def make_index_keyword(kb_filename):
    kb_records = get_kb_records(kb_filename)
    kwindex = minsearch.Index(text_fields=['title', 'abstract', 'journal'], \
    keyword_fields=['author', 'year'])
    kwindex.fit(kb_records)
    return kwindex


# get the filenames needed
rag_script_path = os.path.abspath(__file__)
kb_filename = rag_script_path.replace('scripts/rag.py', 'data/data-kb.csv')
vectors_filename = rag_script_path.replace('scripts/rag.py', \
'data/embed-kb.csv')

# index for vector search
if True:
    vindex = make_index_vector(kb_filename, vectors_filename)

# index for keyword search
if True:
    kwindex = make_index_keyword(kb_filename)
