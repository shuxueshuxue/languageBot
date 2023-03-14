import openai
import speech_recognition as sr
from pydub import AudioSegment
import file_utils

r = sr.Recognizer()
openai.api_key = file_utils.load_from_json("settings.json")["openai_key"]

def transcribe(file_name="reply.mp3", api=False) -> str:
    if api:
        with open(file_name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    else: # run whisper locally. GPU version will be much faster. First load is slow.
        if file_name[-3:] == "mp3":
            sound = AudioSegment.from_mp3(file_name)
            file_name = file_name[-3:] + "wav"
            sound.export(file_name, format="wav")
        with sr.AudioFile(file_name) as source:
            audio = r.record(source)  # read the entire audio file
        transcript = r.recognize_whisper(audio)
    return transcript
