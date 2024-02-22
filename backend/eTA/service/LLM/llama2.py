import replicate

def query_llama2(question_prompt):
    # Stream the response from the model
    for event in replicate.stream(
        "meta/llama-2-70b",
        input={
            "debug": False,
            "top_p": 0.51,
            "prompt": question_prompt,
            "temperature": 0.5,
            "return_logits": False,
            "max_new_tokens": 500,
            "min_new_tokens": -1,
            "repetition_penalty": 1.15
        },
    ):
        # Accumulate the response
        response += str(event)
    
    # Return the accumulated response
    return response
