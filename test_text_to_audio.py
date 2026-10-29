"""Offline checks for the Google Text-to-Speech SDK call contract."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from google.cloud import texttospeech

from main import VOICE_NAME, text_to_audio


class TextToAudioTest(unittest.TestCase):
    """Keep the SDK integration test independent of credentials and network."""

    def test_uses_current_text_to_speech_request_and_decodes_response(self):
        """Use keyword request fields and decode the returned MP3 bytes."""
        client = Mock()
        client.synthesize_speech.return_value = SimpleNamespace(
            audio_content=b'fixture')
        decoded_audio = object()

        with patch('main.AudioSegment.from_file', return_value=decoded_audio) as decode:
            result = text_to_audio(client, 'A dummy sentence.')

        self.assertIs(result, decoded_audio)
        request = client.synthesize_speech.call_args.kwargs
        self.assertEqual(request['input'].text, 'A dummy sentence.')
        self.assertEqual(request['voice'].name, VOICE_NAME)
        self.assertEqual(
            request['audio_config'].audio_encoding, texttospeech.AudioEncoding.MP3)
        audio_source = decode.call_args.args[0]
        self.assertEqual(audio_source.getvalue(), b'fixture')
        self.assertEqual(decode.call_args.kwargs, {'format': 'mp3'})


if __name__ == '__main__':
    unittest.main()
