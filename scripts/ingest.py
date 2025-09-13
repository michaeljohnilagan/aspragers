import pandas as pd
import minsearch
import vectors


def get_data_records(filename):
    df = pd.read_csv(filename, sep='\t', dtype=str)
    df_preprocessed = vectors.preprocess_for_vectorization(df)
    records = df_preprocessed.to_dict('records')
    return records

def make_index_vector(data_filename, vectors_filename):
    records = get_data_records(data_filename)
    vectors = pd.read_csv(vectors_filename, header=None, sep=',')
    vindex = minsearch.VectorSearch(keyword_fields={'author', 'year'})
    vindex.fit(vectors, records)
    return vindex

def make_index_keyword(data_filename):
    records = get_data_records(data_filename)
    kwindex = minsearch.Index(text_fields=['title', 'abstract', 'journal'], \
    keyword_fields=['author', 'year'])
    kwindex.fit(records)
    return kwindex
