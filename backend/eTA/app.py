from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.handleQuery import handleQuery, llamaQuery
app = Flask(__name__)
CORS(app)

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
    answer_llamaIndex = llamaQuery(question)
    return jsonify({"question": question, "answer": answer, "llamaIndexAnswer": answer_llamaIndex})

# piazza

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000)
