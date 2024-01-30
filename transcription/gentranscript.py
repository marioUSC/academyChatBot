import moviepy.editor as mp 
import speech_recognition as sr 

# Load the video 
video = mp.VideoFileClip("output01.mp4") 



# Extract the audio from the video 
audio_file = video.audio 
audio_file.write_audiofile("output01.wav") 

# Initialize recognizer 
r = sr.Recognizer() 

# Load the audio file 
with sr.AudioFile("output01.wav") as source: 
	data = r.record(source) 

# Convert speech to text 
text = r.recognize_google(data) 

# Print the text 
print("\nThe resultant text from video is: \n") 
print(text) 
