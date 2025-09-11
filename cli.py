import rag
from datetime import datetime

if __name__ == '__main__':
    # messages to the user
    welcome_message = '\n'+str(datetime.now())+\
    ' | AspRAGers is ready! Enter your question, or EXIT to exit.'+'\n'
    wait_message = '\n'+str(datetime.now())+\
    ' | AspRAGers is generating a response. Please wait...'+'\n'
    
    # RAG parameters
    do_vector_search = False
    num_results = 10
    model_handle_llm = 'llama3.2:1b'

    # take user input as query, then respond
    while True:
        query = input(welcome_message)
        if query.lower().strip() == 'exit':
            break
        else:
            print(wait_message)
            print(rag.rag(query, \
            do_vector_search=do_vector_search, num_results=num_results, \
            model_handle_llm=model_handle_llm, seed=None))

