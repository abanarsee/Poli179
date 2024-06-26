pip install youtube-dl speechrecognition moviepy opencv-python nltk

pip install yt_dlp

pip install pytube

pip install pytube moviepy pydub speechrecognition

import os
import time
import cv2
import nltk
import pandas as pd
from pytube import YouTube
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
from deepface import DeepFace
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import time

# Function to download YouTube video
def download_video(url):
    yt = YouTube(url)
    video_stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
    video_stream.download(filename='debate_video.mp4')

# Function to extract audio from video
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

# Function to convert audio format
def convert_audio_format(input_path, output_path, format="wav"):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format=format)

# Function to recognize speech with retries
def recognize_speech_with_retries(audio_path, retries=3, delay=5):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    for attempt in range(retries):
        try:
            with audio_file as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
        except sr.RequestError as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise sr.RequestError("Failed to recognize speech after multiple attempts")

# Download video and extract audio
url = 'https://www.youtube.com/watch?v=AciLUP0kzDo'
download_video(url)
extract_audio("debate_video.mp4", "debate_audio.mp3")

# Convert audio format to wav
convert_audio_format("debate_audio.mp3", "debate_audio.wav")

# Recognize speech with retries
try:
    text = recognize_speech_with_retries("debate_audio.wav")
    with open("debate_transcript.txt", "w") as file:
        file.write(text)
    print("Speech recognition succeeded.")
except sr.RequestError as e:
    print(f"Speech recognition failed: {e}")

pip install deepface

# Step 3: Analyze Facial Expressions
video_capture = cv2.VideoCapture("debate_video.mp4")
frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))

emotions = []

for i in range(0, frame_count, fps * 5):  # Sample every 5 seconds
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, i)
    success, frame = video_capture.read()
    if success:
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if 'dominant_emotion' in analysis:
                emotions.append(analysis['dominant_emotion'])
        except ValueError as e:
            print(f"Face could not be detected in frame {i}. Skipping this frame.")
        except Exception as e:
            print(f"An error occurred during face analysis: {e}")

video_capture.release()

with open("facial_emotions.txt", "w") as file:
    file.write("\n".join(emotions))

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load transcript
with open("debate_transcript.txt", "r") as file:
    text = file.read()

# Preprocess text
vectorizer = CountVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform([text])

# Topic modeling
lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(X)

# Display topics
topics = lda.components_
feature_names = vectorizer.get_feature_names_out()

for topic_idx, topic in enumerate(topics):
    print(f"Topic {topic_idx}:")
    print(" ".join([feature_names[i] for i in topic.argsort()[:-11:-1]]))

import pandas as pd

# Load demographics data
demographics = pd.read_csv('/mnt/data/PaperDemographicDetails.csv')

# Load emotions and topics
with open("facial_emotions.txt", "r") as file:
    emotions = file.read().splitlines()

# For simplicity, assume emotions and topics have the same length
# Correlate emotions with demographics
correlations = []

for emotion in set(emotions):
    demographic_sub = demographics[demographics['emotion'] == emotion]
    correlation = demographic_sub['voter_impression'].mean()
    correlations.append((emotion, correlation))

# Display correlations
for emotion, correlation in correlations:
    print(f"Emotion: {emotion}, Correlation: {correlation}")

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Assuming `demographics` has features and target columns
features = demographics.drop(columns=['voter_impression'])
target = demographics['voter_impression']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Logistic Regression
model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
