from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

# Load the model
model = Doc2Vec.load("d2v.model")

# Infer the vector for a new document
test_data = word_tokenize("introduce machine learning".lower())
v1 = model.infer_vector(test_data)
print("V1_infer:", v1)


# Assuming 'data' is the list of original sentences
data = [
    "I love machine learning. Its awesome.",
    "I love coding in python",
    "I love building chatbots",
    "they chat amazingly well",
    "Machine learning algorithms can predict stock market trends.",
    "Python is a versatile programming language.",
    "Chatbots are becoming increasingly sophisticated.",
    "Natural language processing enables machines to understand human language.",
    "Data science involves extracting knowledge from data.",
    "Artificial intelligence will shape the future of technology.",
    "Developing mobile apps can be both challenging and rewarding.",
    "Blockchain technology is revolutionizing the finance industry.",
    "Quantum computing holds the potential to solve complex problems quickly.",
    "Cybersecurity is essential for protecting digital information.",
    "Cloud computing provides scalable resources for businesses and individuals.",
    "Augmented reality offers immersive experiences for users.",
    "Renewable energy sources are key to sustainable development.",
    "Genetic engineering has advanced medical research and treatment.",
    "Autonomous vehicles are transforming the transportation sector.",
    "3D printing is enabling new possibilities in manufacturing and design."
]

# The rest of your code to load the model and infer the vector...

# Print the most similar documents and their corresponding sentences
try:
    similar_doc = model.dv.most_similar([v1])
    print("Similar Documents:")
    for i, (tag, similarity) in enumerate(similar_doc):
        if i < 3:
            print(f"Sentence: '{data[int(tag)]}' with similarity score: {similarity}")
        else:
            break
except KeyError:
    print("Tag '1' was not found in the training data.")

