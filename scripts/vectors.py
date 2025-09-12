import os
from sentence_transformers import SentenceTransformer

# which model
model_handle = 'multi-qa-MiniLM-L6-cos-v1'

# save and use locally
model = SentenceTransformer(model_name_or_path=model_handle)
path = os.path.abspath(__file__).replace('scripts/vectors.py', \
'data/vectorizer/')
model.save(path)
model = SentenceTransformer(model_name_or_path=path)

# preprocess data for vectorization
def preprocess_for_vectorization(df):
    new_df = df.copy()
    for column_name in new_df.columns:
        new_df[column_name] = new_df[column_name].fillna('')
    return new_df
