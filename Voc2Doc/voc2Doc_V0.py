from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

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


tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(vector_size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm=0)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.epochs)  # Use model.epochs instead of model.iter
    model.alpha -= 0.0002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save("d2v.model")
print("Model Saved")
