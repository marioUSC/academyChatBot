import json
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# Read data from 'piazza.json' file
with open('piazza.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Preprocessing function to remove HTML tags and tokenize
def preprocess_text(text):
    text = re.sub('<[^<]+?>', '', text)  # Remove HTML tags
    return word_tokenize(text.lower())

# Dictionary for mapping tags to original text
tag_to_text = {}

# Process data and create mappings
tagged_data = []
counter = 0  # Initialize a counter for unique tags
for value in json_data.values():
    # Process the question
    question = value['detail']['subject'] + " " + value['detail']['content']
    document_text = preprocess_text(question)  # Start building the document text

    # # Process each answer and add to the document text
    # for answer in value['answers'].values():
    #     answer_text = preprocess_text(answer)
    #     document_text += answer_text  # Add answer text to the document

    # Create a TaggedDocument for the combined question and answers
    document_tag = str(counter)
    tagged_data.append(TaggedDocument(words=document_text, tags=[document_tag]))
    tag_to_text[document_tag] = question + " " + " ".join(value['answers'].values())
    counter += 1  # Increment the counter

# Save the tag-to-text mapping to a JSON file
with open('tag_to_text_map2.json', 'w', encoding='utf-8') as f:
    json.dump(tag_to_text, f, ensure_ascii=False, indent=4)

# Parameters for the Doc2Vec model
max_epochs = 100
vec_size = 20
alpha = 0.025

# Initialize and train the Doc2Vec model
model = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print(f'Iteration {epoch}')
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.alpha -= 0.0002
    model.min_alpha = model.alpha

# Save the model
model.save("d2v2.model")
print("Model saved as d2v2.model")

print("Mapping file saved as tag_to_text_map2.json")
