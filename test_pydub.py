import StringIO
import pydub
from pydub import AudioSegment

# # mp3の末尾に無音を追加する
sound = AudioSegment.from_mp3("aman.mp3")

duration = sound.duration_seconds
silence = AudioSegment.silent(duration=duration*1000*1.5)

added_sound = sound + silence
added_sound.export("aman_repeat.mp3", format="mp3")
