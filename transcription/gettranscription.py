from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import moviepy.editor as mp
import speech_recognition as sr
import json

import os

# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the absolute paths for upload and JSON folders
UPLOAD_FOLDER = os.path.join(current_dir, 'uploads')
JSON_FOLDER = os.path.join(current_dir, 'json')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['JSON_FOLDER'] = 'json'
ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_video(video_path, interval=10):
    clip = mp.VideoFileClip(video_path)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')

    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    transcripts = []
    for i in range(0, int(clip.duration), interval):
        start_time = i
        end_time = min(i + interval, int(clip.duration))

        with sr.AudioFile(audio_path) as source:
            audio_segment = r.record(source, duration=end_time-start_time, offset=start_time)
        
        try:
            transcript = r.recognize_google(audio_segment)
            # Add transcript entries for each 10-second interval
            transcript_lines = transcript.split("\n")
            for j, line in enumerate(transcript_lines):
                transcripts.append({
                    "timestamp": f"({(start_time + j * 10) // 60}:{(start_time + j * 10) % 60:02})",
                    "transcript": line
                })
        except sr.UnknownValueError:
            transcripts.append({
                "timestamp": f"({start_time // 60}:{start_time % 60:02})",
                "transcript": "_" # Could not understand audio or N/A
            })
        except sr.RequestError as e:
            transcripts.append({
                "timestamp": f"({start_time // 60}:{start_time % 60:02})",
                "transcript": f"Error with Google Speech Recognition service: {e}"
            })

    os.remove(audio_path)

    return transcripts

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return redirect(url_for('transcription_result', filename=filename))

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/transcription/<filename>')
def transcription_result(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    transcripts = transcribe_video(filepath)

    # Save transcription to a JSON file
    json_filename = f'{filename}.json'  # JSON filename without the path
    json_filepath = os.path.join(app.config['JSON_FOLDER'], json_filename)
    with open(json_filepath, 'w') as json_file:
        json.dump(transcripts, json_file)

    # Pass the JSON filename to the template
    return render_template('result.html', filename=filename, json_url=url_for('download_transcription', filename=filename))

@app.route('/download/<filename>')
def download_transcription(filename):
    json_filename = f'{filename}'  
    json_filepath = os.path.join(app.config['JSON_FOLDER'], json_filename)
    return send_file(json_filepath, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
