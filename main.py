from pydub import AudioSegment
from google.cloud import texttospeech
from split_into_sentences import split_into_sentences
import io

prefix = 'c1-'
path = './list.txt'
name = 'en-US-Wavenet-D'

client = texttospeech.TextToSpeechClient()

voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
    name=name)

audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
    speaking_rate=0.8)

def text_to_audio(text: str) -> AudioSegment:
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # debug
    # filepath = f'./temp/{text}.mp3'
    # with open(filepath, 'wb') as out:
    #     out.write(response.audio_content)

    # https: // github.com/rudolfratusinski/simple-nlp-chatbot/blob/master/chatbot.py
    return AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3")


def create_silent(audio: AudioSegment) -> AudioSegment:
    duration = audio.duration_seconds
    return AudioSegment.silent(duration=duration*1000*1.45)


with open(path) as f:
    lines = [l.strip() for l in f.readlines() if l.strip() != '']

for index, line in enumerate(lines):
    filename = prefix + str(index + 1).zfill(3) + '-' +  line.strip().replace('.', '').replace('/', '')

    combined = AudioSegment.empty()
    sentences = split_into_sentences(line) if split_into_sentences(line) else [line]

    for index, sentence in enumerate(sentences):
        audio = text_to_audio(sentence)
        silent = create_silent(audio)
        combined += audio + silent


    filepath = f'./voices/{filename}.mp3'
    combined.export(filepath, format="mp3")
    print(f'Audio content written to {filepath}')
