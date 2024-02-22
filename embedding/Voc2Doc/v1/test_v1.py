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
# test_sentence = "How to optimally allocate 12 remaining bits in a 32-bit IP address divided into 3 subnets, each supporting 1024 hosts, considering scalability if not specified?"
# test_sentence = "can I code with VScode on Macbook?" #158
# test_sentence = "project development enviroment Can  I code at VS code on my Macbook(as MAC also uses Linux and the command are about the same) but not on the VM and switch them to VM in the end? When I use VM to code it would pretty lag that it usually respond for 2 seconds when I type keyboard. What I'm concerned about is if I switch these codes to our VM will any problems happen?  It works so far so good on my Mac. Yes. You can work on Macbook and many students do the same.Although I don't feel there would be any issues when you transition to studentVM, but make sure that you have enough time at the end to test out your code in the studentVM before you make your final submission. You can also code using remote development with VS Code: the app on your Mac can be the client, and you can set it up to SSH into your VM so that the actual location of the code (and terminal windows you open in VS Code) is on your VM. This way you can have the environment of the VM with the experience of coding on your Mac, this is what I'm doing."
test_sentence = "Correct room return gateway Hi , I 'm wondering correct place return gateway ? Or I want return gateway University , I go ? Much appreciated ! The building PHE , Professor Goodney seems office morning . You try return CS front desk SAL . But returning SAL , may need contact Professor Goodney first ."
test_sentence = "Correct room return gateway"
test_sentence = "where should I return the gateway"
print("result for " + test_sentence + "\n")
test_data = word_tokenize(test_sentence.lower())
v1 = model.infer_vector(test_data)
# print("V1_infer:", v1)

# Load the mapping from the tags to the original texts
with open('notPre450.json', 'r', encoding='utf-8') as file:
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
