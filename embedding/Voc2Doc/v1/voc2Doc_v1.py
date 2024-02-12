import json
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# Read data from preprocessed JSON file
with open('EE450_Piazza.json', 'r', encoding='utf-8') as file:
    preprocessed_data = json.load(file)

# Prepare data for Doc2Vec
tagged_data = []
for tag, text in preprocessed_data.items():
    # Tokenize the preprocessed text
    tokens = word_tokenize(text.lower())
    # Create a TaggedDocument
    tagged_data.append(TaggedDocument(words=tokens, tags=[tag]))

# Parameters for the Doc2Vec model
max_epochs = 100
vec_size = 100
alpha = 0.025

# Initialize and train the Doc2Vec model
model = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    # print(f'Iteration {epoch}')
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    # Update the learning rate
    model.alpha -= 0.0002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

# Save the model
model.save("d2v.model")
print("Model saved as d2v.model")
