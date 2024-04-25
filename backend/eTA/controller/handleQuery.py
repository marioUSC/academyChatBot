from eTA.service.LLM.gpt import query_GPT
from eTA.service.LLM.llama2 import query_llama2
from eTA.service.embedding.getAnswer import find_similar_questions
from llama_index.core import StorageContext, load_index_from_storage, set_global_service_context, ServiceContext, VectorStoreIndex
import os
import re

# This function calls the embedding model to retrieve the most similar QA pairs.
# It then forwards these pairs to the LLM (Large Language Model) for summarization.
# After receiving the summarized response, it returns the reply to the user.
def handleQuery(question, table_name, llama_Answer = "default, ignore me"):
    
    # Base prompt with instructions for the model
    base_prompt = """Please carefully review the provided Q&A pairs to identify and extract \
                knowledge that is directly relevant to the new question. Focus exclusively on the \
                details that directly address the new question, while completely ignoring any \
                information or pairs that are unrelated. Your response should be a single, \
                human-like answer that precisely addresses the new question based on \
                the most relevant information found within the provided Q&A pairs. \
                If the QA pair you picked has the link, also return all link in format(replace real_linkx as real link, and LLIINNKK as an indicator): LLIINNKK: real_link1, real_link2}\n"""

    # Get the most silimar QA pairs from embedding model
    knowledge = find_similar_questions(question, table_name, 5)

    # Concatenate the base prompt with the specific question and the context
    knowledge_prompt = f" Q&A pairs knowledge base 1:  : {knowledge}"
    question_prompt = f"Question: {question}"

    llama_prompt = f" Another reference:  : {llama_Answer}"

    # Aks LLM to summerize the result
    final_prompt = base_prompt + question_prompt + knowledge_prompt + llama_prompt
    # print(final_prompt)
    result = query_GPT(final_prompt)
    return result

# check if link exist, return link or none
def extractLinks(input_string):
    # Initialize an empty list to hold the extracted links
    links = []
    
    # Use a regular expression to search for the specified format
    # "LLIINNKK:" followed by one or more non-whitespace characters, separated by commas, possibly surrounded by whitespace
    match = re.search(r'LLIINNKK:\s*((?:\S+,?\s*)+)', input_string)
    
    # If a match is found, extract the links
    if match:
        # Get the matched group of links as a single string
        links_str = match.group(1)
        # Split the string on commas to get individual links, and strip any surrounding whitespace from each link
        links = [link.strip() for link in links_str.split(',')]
    
    # Return the list of links; this will be empty if no links were found
    return links

# remove link part of answer
def extractAnswer(input_string):
    cleaned_string = re.sub(r'LLIINNKK:.*', '', input_string)
    
    # Return the modified string which is the original string with "LLIINNKK:" and the following part removed
    return cleaned_string

def extract_links_and_answer(input_string):
    # Initialize an empty list to hold the extracted links
    links = []
    
    # Use a regular expression to find "LLIINNKK:" and everything after it
    match = re.search(r'LLIINNKK:\s*((?:\S+,?\s*)+)', input_string)
    
    # If a match is found, extract the links
    if match:
        # Extract and split the links, stripping any surrounding whitespace
        links_str = match.group(1)
        links = [link.strip() for link in links_str.split(',')]
        # Remove the matched part from the input string
        cleaned_string = re.sub(r'LLIINNKK:.*', '', input_string)
    else:
        # If no links are found, return the original string as is
        cleaned_string = input_string
    
    # Return a tuple containing the list of links and the modified input string
    return links, cleaned_string

# check if the answer can be answered
def handleAnswerValidation(answer, question):
    check_answer_prompt = f" if the following statment is a answer to the specific question, reply me with 'yes', else is it states not enough info or cannot get the answer, reply me with 'no'. \
                            don't reply anything else except 'yes' or 'no', all should be lower case: Answer: {answer} Question: {question}"
    check_result = query_GPT(check_answer_prompt)
    print('If current answer has result:' + check_result)
    return check_result

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
    input_example = "Here is an example of "
    output_links = extractLinks(input_example)
    print(output_links)  # Output: ['https://example.com', 'https://test.com']