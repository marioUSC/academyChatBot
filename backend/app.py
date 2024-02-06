from flask import Flask, request, jsonify
from controller.handleQuery import handleQuery
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return 'Hello, World!'

@app.route('/ask', methods=['POST'])
def answer_question():
    data = request.get_json()  
    question = data.get('question')

    prompt = " Q&A pairs knowledge base:  1: Correct room to return the gateway <p>Hi, I&#39;m wondering if this is the correct place to return the gateway?</p>\n<p><img src=\"/redirect/s3?bucket=uploads&amp;prefix=paste%2Fky7yf4kejiayz%2F5915de890feef2d0c5e63d0df8a9bf94288bb0afd4be04a52321c2014dec95e0%2F2302af54634af427a94e47a9f260ece.jpg\" alt=\"2302af54634af427a94e47a9f260ece.jpgNaN\" height=\"480\" /><br />Or if I want to return the gateway to the University, where do I go to?<br />Much appreciated!</p> The building should be PHE, but Professor Goodney seems not in his office this morning. You can try to return to CS front desk at SAL. But for returning at SAL, you may need to contact Professor Goodney first. \
2: Returning Gateway For returning the gateway, the professor said that we can drop it to another professor&#39;s office. May I ask where and when we can return the gateway? <md>Please send an email to the proefessor to ask about it.</md> \
3: Unable to connect to Node-RED <md>I have successfully installed Node-RED as a custom app on Gateway. However, I cannot reach port 1880 (port of Node-RED) on Gateway. I have been refreshing and waiting for half an hour. \n\n![IMG_6902.PNG](/redirect/s3?bucket=uploads&prefix=paste%2Fl7dlqs1firl1vh%2Feacf41e9ad8e0d0833d3ad30bbc4e354a02452bb532be43e7eab66aa66486b4a%2FIMG_6902.PNG)\n\nDid anyone meet the same issue?\n\nThank you fro your reply.</md> You might need to enable Node-red Setting Via LAN under Administration-&gt;Access Configuration.\
    \n"

    questionPrompt = "Question: {}".format(question)

    answer = handleQuery(question)

    # 返回回答
    return jsonify({"question": question, "answer": answer})

if __name__ == '__main__':
    app.run(debug=True)