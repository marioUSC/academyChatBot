from eTA.service.LLM.gpt import query_GPT
from eTA.service.LLM.llama2 import query_llama2
from eTA.service.embedding.getAnswer import find_similar_questions
from llama_index.core import StorageContext, load_index_from_storage, set_global_service_context, ServiceContext, VectorStoreIndex
import os

# This function calls the embedding model to retrieve the most similar QA pairs.
# It then forwards these pairs to the LLM (Large Language Model) for summarization.
# After receiving the summarized response, it returns the reply to the user.
def handleQuery(question, table_name):
    
    # Base prompt with instructions for the model
    base_prompt = """Please carefully review the provided Q&A pairs to identify and extract \
                knowledge that is directly relevant to the new question. Focus exclusively on the \
                details that directly address the new question, while completely ignoring any \
                information or pairs that are unrelated. Your response should be a single, \
                human-like answer that precisely addresses the new question based on \
                the most relevant information found within the provided Q&A pairs. \n"""

    # Get the most silimar QA pairs from embedding model
    knowledge = find_similar_questions(question, table_name, 5)

    # Concatenate the base prompt with the specific question and the context
    knowledge_prompt = f" Q&A pairs knowledge base:  : {knowledge}"
    question_prompt = f"Question: {question}"

    # Aks LLM to summerize the result
    final_prompt = base_prompt + question_prompt + knowledge_prompt 
    result = query_GPT(final_prompt)
    # print('update111:' + result)
    return result

# Embedding model using Llama Index
def llamaQuery(user_question):
    # Setup the llama-index service context
    service_context = ServiceContext.from_defaults(
        embed_model="local:intfloat/e5-small-v2"
    )
    set_global_service_context(service_context)

    # Load the index from storage
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, '../service/llamaIndex/index')
    model_path = os.path.normpath(model_path)

    storage_context = StorageContext.from_defaults(persist_dir=model_path)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    # Use the query engine to get a response
    response_object = query_engine.query(user_question)
    
    # Convert the response object to a string (if it's not already)
    # This step depends on the structure of your 'NodeWithScore' object and how you want to format the response
    # Here, we're assuming the response object can be converted directly or has an attribute that can be used
    response = str(response_object)  # Adjust this line as necessary based on the actual response structure

    return response

if __name__ == '__main__':
    # handleQuery('where should I return the gateway?')
    print(llamaQuery('test'))