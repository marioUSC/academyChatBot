from .service.LLM.gpt import query_GPT
from .service.LLM.llama2 import query_llama2
from .service.embedding.getAnswer import find_similar_questions

def handleQuery(question):
    # Base prompt with instructions for the model
    base_prompt = """Please carefully review the provided Q&A pairs to identify and extract \
                knowledge that is directly relevant to the new question. Focus exclusively on the \
                details that directly address the new question, while completely ignoring any \
                information or pairs that are unrelated. Your response should be a single, \
                human-like answer that precisely addresses the new question based on \
                the most relevant information found within the provided Q&A pairs. \n"""


    knowledge = find_similar_questions(question)

    # Concatenate the base prompt with the specific question and the context
    knowledge_prompt = f" Q&A pairs knowledge base:  : {knowledge}"
    question_prompt = f"Question: {question}"

    final_prompt = base_prompt + question_prompt + knowledge_prompt 
    result = query_GPT(final_prompt)
    print(result)
    return result

if __name__ == '__main__':
    handleQuery('where should I return the gateway?')