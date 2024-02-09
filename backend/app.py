from flask import Flask, request, jsonify
from controller.handleQuery import handleQuery
app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_answer_question():
    data = request.get_json()  
    question = data.get('question')

    questionPrompt = "Question: {}".format(question)

    answer = "This is test answer for question, for saving cost"

    
    return jsonify({"question": question, "answer": answer})

@app.route('/ask', methods=['POST'])
def answer_question():
    data = request.get_json()  
    question = data.get('question')

    questionPrompt = "Question: {}".format(question)

    answer = handleQuery(question)

    
    return jsonify({"question": question, "answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
