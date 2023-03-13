import asyncio
import time
from pydub import AudioSegment
import edge_tts
import pygame
import openai # this is a modified version: the base path has been changed to a tencent proxy server
import speech_recognition as sr
import STT
import file_utils

openai.api_key = file_utils.load_dict_from_json("settings.json")["openai_key"]
if not openai.api_key:
    print("please set your api key!")
    input()
    exit()
pygame.init()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
mic = sr.Microphone()

def get_audio_length(audio_file_path="reply.mp3"):
    audio_file = AudioSegment.from_file(audio_file_path)
    audio_length = len(audio_file)
    audio_length_sec = audio_length / 1000
    return audio_length_sec

async def text_to_speech(text='', output_file="reply.mp3", voice="zh-TW-HsiaoChenNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def play_sound(filename="reply.mp3"):
    # For some reason the sound.play just doesn't work. So I have to use music instead.
    pygame.mixer.music.unload() # clear resources
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def generate_prompt(question: str):
    return question

def get_response(prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=20
    )
    return completion.choices[0].message.content

async def main():
    print("loading...")
    await text_to_speech("hello")
    STT.transcribe()
    play_sound()

    while True:
        print("listening...")
        with mic as source:
            r = sr.Recognizer()
            audio = r.listen(source)
            print("recorded")

        user_input = r.recognize_whisper(audio, language="English")
        user_prompt = generate_prompt(user_input)

        chloe_output = get_response(user_prompt).replace("\n", "")
        print(f"Jeffry: {user_input}")
        pygame.mixer.music.unload()
        await text_to_speech(chloe_output)
        play_sound()
        print(f"Chloe: {chloe_output}")
        time.sleep(get_audio_length())

if __name__ == "__main__":
    asyncio.run(main())

