from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import json

# Load the model
model = Doc2Vec.load("d2v.model")

# Define a test sentence and tokenize it
# test_sentence = "where should I return the gateway"

# test_sentence = "I cannot connect to Node-RED"

#EE450
# test_sentence = "what type of formula sheet we can use? "
test_sentence = "How to optimally allocate 12 remaining bits in a 32-bit IP address divided into 3 subnets, each supporting 1024 hosts, considering scalability if not specified?"
print("result for " + test_sentence + "\n")
test_data = word_tokenize(test_sentence.lower())
v1 = model.infer_vector(test_data)
# print("V1_infer:", v1)

# Load the mapping from the tags to the original texts
with open('EE450_Piazza.json', 'r', encoding='utf-8') as file:
    tag_to_text = json.load(file)

# Find the most similar documents
similar_docs = model.dv.most_similar([v1], topn=3)
print("Similar Documents:")
similar_questions = []
for tag, similarity in similar_docs:
    print(f"Tag: {tag}, Similarity: {similarity}")
    similar_questions.append(tag_to_text[tag])

# Save the similar questions to a new file
with open('similar_questions.txt', 'w', encoding='utf-8') as file:
    for question in similar_questions:
        file.write(question + "\n\n")
        file.write("\n" + '='*10 + "\n")

print("Similar questions saved to similar_questions.txt")
