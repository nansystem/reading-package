"""Generate speech audio and surround each sentence with silence."""

import io

from google.cloud import texttospeech
from pydub import AudioSegment

from split_into_sentences import split_into_sentences

PREFIX = 'c1-'
PATH = './list.txt'
VOICE_NAME = 'en-US-Wavenet-D'


def text_to_audio(client, text: str) -> AudioSegment:
    """Synthesize one sentence and decode its MP3 response."""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name=VOICE_NAME,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.8,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return AudioSegment.from_file(io.BytesIO(response.audio_content), format='mp3')


def create_silent(audio: AudioSegment) -> AudioSegment:
    """Create a pause sized relative to the supplied audio."""
    return AudioSegment.silent(duration=audio.duration_seconds * 1000 * 1.45)


def main() -> None:
    """Read the input list and write synthesized files to voices/."""
    client = texttospeech.TextToSpeechClient()
    with open(PATH, encoding='utf-8') as source:
        lines = [line.strip() for line in source if line.strip()]

    for line_index, line in enumerate(lines):
        filename = (
            PREFIX + str(line_index + 1).zfill(3) + '-' +
            line.replace('.', '').replace('/', '')
        )
        combined = AudioSegment.empty()
        sentences = split_into_sentences(line) or [line]

        for sentence in sentences:
            audio = text_to_audio(client, sentence)
            combined += audio + create_silent(audio)

        filepath = f'./voices/{filename}.mp3'
        combined.export(filepath, format='mp3')
        print(f'Audio content written to {filepath}')


if __name__ == '__main__':
    main()
