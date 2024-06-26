from flask import Flask, request, jsonify
from flask_cors import CORS
from eTA.controller.handleQuery import handleQuery, llamaQuery
from eTA.controller.handleDatabase import (
    handleUpload, handleScan, handleItemSearch, handleDelete,
    handleModifyItem, handleVedioUpload
)
from eTA.controller.handleVideo import transcribe_to_file
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

    if request.is_json:

        data = request.get_json()  
        question = data.get('question')
        courseID = data.get('courseID')
        questionPrompt = "Question: {}".format(question)

        answer = handleQuery(question, courseID)
        answer_llamaIndex = llamaQuery(question)
        return jsonify({"question": question, "answer": answer, "llamaIndexAnswer": answer_llamaIndex})
    else:
        return jsonify({"error": "Request must be JSON"}), 400

# Handle new upload from user
@app.route('/upload-json', methods=['POST'])
def upload_json():

    if request.is_json:
        data = request.get_json()
        courseID = data.get('courseID')
        fileID = data.get('fileID', 'default')
        content = data.get('content')

        if content is None or courseID is None:
            return jsonify({"error": "Request must be contain content to upload"}), 404

        message = handleUpload(content, courseID, fileID)  
        
        return jsonify({
            "message": message
        }), 200

    else:
        return jsonify({"error": "Request must be JSON"}), 400

# Handle new upload from user
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if request.is_json:
        data = request.get_json()
        courseID = data.get('courseID')
        fileID = data.get('fileID', 'default')
        content = data.get('content')

        if content is None or courseID is None:
            return jsonify({"error": "Request must be contain content to upload"}), 404

        message = handleVedioUpload(content, courseID, fileID)  
        
        return jsonify({
            "message": message
        }), 200

    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/readDB', methods=['POST'])
def read_from_database():
    if request.is_json:
        data = request.get_json()

        courseID = data.get('courseID')
        hasStartKey = data.get('hasStartKey')
        read_number = int(data.get('readLimit', '2'))
        if hasStartKey:
            start_key = data.get('startKey')
        else:
            start_key = None

        result = handleScan(courseID, start_key, read_number)
        return jsonify({
            "message": result['message'],
            "result": result
        }), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400


@app.route('/itemQuery', methods=['POST'])
def querySingalItem():
    if request.is_json:
        data = request.get_json()
        courseID = data.get('courseID')
        primary_key = data.get('primary_key')

        # missing required field
        if courseID is None or primary_key is None:
            return jsonify({
                "message": "Error: 'courseID' and 'primary_key' are required in JSON data."
            }), 400
        
        query_item = handleItemSearch(courseID, primary_key)
        return jsonify({
                'message': query_item['message'],
                'status': query_item['status'],
                'data': query_item['data']
            }), 200

@app.route('/itemDelete', methods=['POST'])
def deleteSingleItem():
    if request.is_json:
        data = request.get_json()
        courseID = data.get('courseID')
        primary_key = data.get('primary_key')

        # missing required field
        if courseID is None or primary_key is None:
            return jsonify({
                "message": "Error: 'courseID' and 'primary_key' are required in JSON data."
            }), 400
        
        query_item = handleDelete(courseID, primary_key)
        return jsonify({
                'message': query_item['message'],
                'status': query_item['status'],
                'data': query_item['data']
            }), 200
    else:
        return jsonify({
                'message': 'JSON request is needed',
                'status': '400'
            }), 400

@app.route('/itemUpdate', methods=['POST'])
def updateSingleItem():
    if request.is_json:
        data = request.get_json()
        courseID = data.get('courseID')
        primary_key = data.get('primary_key')
        updateContent = data.get('updateContent')
        # missing required field
        if courseID is None or primary_key is None:
            return jsonify({
                "message": "Error: 'courseID' and 'primary_key' are required in JSON data."
            }), 400
        
        update_result = handleModifyItem(updateContent, courseID, primary_key)
        return jsonify({
                'message': update_result['message'],
                'status': update_result['status']
            }), 200
    else:
        return jsonify({
                'message': 'JSON request is needed',
                'status': '400'
            }), 400
    
@app.route('/upload-rawVideo', methods=['POST'])
def upload_rawVideo():

    courseID = request.form.get('courseID')
    fileID = request.form.get('fileID', 'video upload')

    # Validate courseID
    if not courseID:
        return jsonify({'error': 'Missing courseID'}), 400

    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    video = request.files['video']

    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if video:
        video_path = f'./uploads/{video.filename}'
        video.save(video_path)
        transcript_json = transcribe_to_file(video_path)
        message = handleVedioUpload(transcript_json, courseID, fileID)  
        
        return jsonify({
            "message": message
        }), 200


    return jsonify({'error': 'Upload failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=True, port=5000)
