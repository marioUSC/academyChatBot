from flask import Flask, request, jsonify
from flask_cors import CORS
from eTA.controller.handleQuery import handleQuery, llamaQuery
from eTA.controller.handleDatabase import handleUpload, handleScan

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

# Handle new upload from user
@app.route('/upload-json', methods=['POST'])
def upload_json():

    courseID = request.headers.get('courseID')
    fileID = request.headers.get('fileID', 'default')
    if courseID:
        print(f"Received custom header courseID with value: {courseID}")
    else:
        return "Custom header courseID not found", 400

    if request.is_json:
        data = request.get_json()
        message = handleUpload(data, courseID, fileID)  
        
        return jsonify({
            "message": message,
            "custom_header": courseID
        }), 200

    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/readDB', methods=['GET'])
def read_from_database():
    courseID = request.headers.get('courseID')
    # start_key = request.headers.get('startKey', None)
    read_number = int(request.headers.get('readLimit', '2'))

    if not courseID:
        return jsonify({
            "message": 'courseID not found'
        }), 400


    if request.is_json:
        start_key = request.get_json()
        result = handleScan(courseID, start_key, read_number)
    return result, 200


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000)
