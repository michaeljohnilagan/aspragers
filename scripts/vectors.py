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
