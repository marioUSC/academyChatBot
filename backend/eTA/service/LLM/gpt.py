from openai import OpenAI

def query_GPT(question):
    # Initialize the OpenAI client
    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        stream=False,
    )

    # Return the content of the response
    return stream.choices[0].message.content

