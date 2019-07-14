from pydub import AudioSegment
from google.cloud import texttospeech


# export GOOGLE_APPLICATION_CREDENTIALS="/Users/nancy/git/reading-package/reading-package-account-key.json"
# 英文からmp3にする
text = "A man is walking with a dog."


# Instantiates a client
client = texttospeech.TextToSpeechClient.from_service_account_file("/Users/nancy/git/reading-package/reading-package-account-key.json")


"""
voices = client.list_voices()

with open('./list_voices.txt', mode='w') as f:
    for voice in voices.voices:
        f.write(voice.name + '\n')

# name一覧
en-US-Wavenet-A
en-US-Wavenet-B
en-US-Wavenet-C
en-US-Wavenet-D
en-US-Wavenet-E
en-US-Wavenet-F
"""

# Set the text input to be synthesized
synthesis_input = texttospeech.types.SynthesisInput(text=text)

for name in ['en-US-Wavenet-A',
             'en-US-Wavenet-B',
             'en-US-Wavenet-C',
             'en-US-Wavenet-D',
             'en-US-Wavenet-E',
             'en-US-Wavenet-F']:

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
        name=name)

    # # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=0.8)

    # # Perform the text-to-speech request on the text input with the selected
    # # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # # The response's audio_content is binary.
    with open(f'{name}.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "{name}.mp3"')


# # mp3の末尾に無音を追加する
# sound = AudioSegment.from_mp3("aman.mp3")

# duration = sound.duration_seconds
# silence = AudioSegment.silent(duration=duration*1000*1.5)

# added_sound = sound + silence
# added_sound.export("aman_repeat.mp3", format="mp3")
