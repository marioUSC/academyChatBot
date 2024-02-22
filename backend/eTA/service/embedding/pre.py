import replicate

def summarize_qa(question, answer):
    """
    Summarizes a question and its answer by removing irrelevant information and
    providing a concise summary using the Llama model.

    Parameters:
    - question: The question text.
    - answer: The answer text, which may contain irrelevant information.

    Returns:
    A summary of the question and answer without irrelevant details.
    """
    # Remove irrelevant information from the question and answer
    clean_question = remove_irrelevant_info(question)
    clean_answer = remove_irrelevant_info(answer)
    
    # Construct the prompt for the Llama model to summarize the Q&A
    prompt = f"Based on the following question and answer, provide a concise summary without irrelevant details such as images:\n\nQuestion: {clean_question}\nAnswer: {clean_answer}\n\nSummary:"
    
    # Call the Llama model to generate a summary
    response = replicate.run(
        "meta/llama-2-70b",
        {
            "debug": False,
            "top_p": 0.51,
            "prompt": prompt,
            "temperature": 0.5,
            "return_logits": False,
            "max_new_tokens": 500,
            "min_new_tokens": -1,
            "repetition_penalty": 1.15
        }
    )
    print(response)
    # Assuming the response contains the required summary
    # Adjust this part according to the actual structure of the response from replicate.predict
    return response  # This may need adjustment to match the actual format of the response

def remove_irrelevant_info(text):
    """
    Removes irrelevant information from a text, such as image links.

    Parameters:
    - text: The text from which to remove irrelevant information.

    Returns:
    The cleaned text without irrelevant details.
    """
    # Implement logic to remove irrelevant info, e.g., image links
    clean_text = text.replace("<img src=", "").replace("/>", "")
    return clean_text

# Example usage
question = "Correct room to return the gateway <p>Hi, I&#39;m wondering if this is the correct place to return the gateway?</p>\n<p><img src=\"/redirect/s3?bucket=uploads&amp;prefix=paste%2Fky7yf4kejiayz%2F5915de890feef2d0c5e63d0df8a9bf94288bb0afd4be04a52321c2014dec95e0%2F2302af54634af427a94e47a9f260ece.jpg\" alt=\"2302af54634af427a94e47a9f260ece.jpgNaN\" height=\"480\" /><br />Or if I want to return the gateway to the University, where do I go to?<br />Much appreciated!</p>"
answer = "The building should be PHE, but Professor Goodney seems not in his office this morning. You can try to return to CS front desk at SAL. But for returning at SAL, you may need to contact Professor Goodney first."
summary = summarize_qa(question, answer)
# print(summary)
