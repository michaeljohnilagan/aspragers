import rag
from datetime import datetime

if __name__ == '__main__':
    # messages to the user
    welcome_message = '\n'+str(datetime.now())+\
    ' | AspRAGers is ready! Enter your question,'+\
    ' RANDOM to draw a random question,'+\
    ' or EXIT to exit.'+'\n'
    wait_message = '\n'+str(datetime.now())+\
    ' | AspRAGers is generating a response. Please wait...'+'\n'
    
    # RAG parameters
    do_vector_search = rag.config['do_vector_search']
    num_results = rag.config['num_results']
    model_handle_llm = rag.config['model_handle_llm']
    questions_filename = 'data/data-synth-question.csv'

    # take user input as query, then respond
    while True:
        query = input(welcome_message)
        if query.lower().strip() == 'exit':
            break
        if query.lower().strip() == 'random':
            query = rag.get_random_question(questions_filename)
            print(query)
        print(wait_message)
        print(rag.rag(query, \
        do_vector_search=do_vector_search, num_results=num_results, \
        model_handle_llm=model_handle_llm, seed=None))
