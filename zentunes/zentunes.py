import os
from pydub import AudioSegment
from collections import OrderedDict
from zentunes.lib.playht import PlayHTAPI
import configparser
import eyed3


class AudioGenerator:
    def __init__(
        self,
        api,
        script_parts,
        background_music_path,
        output_path,
        audio_path="tmp_audio",
    ):
        self.api = api
        self.script_parts = script_parts
        self.background_music_path = background_music_path
        self.output_path = output_path
        self.audio_path = audio_path

    def generate_audio(self):
        final_audio = AudioSegment.empty()  # Start with an empty segment

        for index, (part, gap_duration) in enumerate(self.script_parts.items()):
            filename = f"voice_part_{index}.mp3"
            filename = os.path.join(self.audio_path, filename)

            mp3_path = self.api.get_audio(part, filename)
            segment = AudioSegment.from_file(mp3_path, format="mp3")
            final_audio += segment + AudioSegment.silent(duration=gap_duration * 1000)

        background_music = AudioSegment.from_file(
            self.background_music_path, format="mp3"
        )

        if len(background_music) < len(final_audio):
            while len(background_music) < len(final_audio):
                background_music += background_music
        background_music = background_music[: len(final_audio)]

        combined_audio = background_music.overlay(final_audio, position=0)
        combined_audio.export(self.output_path, format="mp3")

    @staticmethod
    def add_metadata_to_mp3(file_path, title, artist, album):
        audiofile = eyed3.load(file_path)
        if audiofile.tag is None:
            audiofile.initTag()
        audiofile.tag.artist = artist
        audiofile.tag.album = album
        audiofile.tag.title = title
        audiofile.tag.save()

    def add_metadata(self, title, artist, album):
        self.add_metadata_to_mp3(self.output_path, title, artist, album)


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    # Extract values from config file
    artist = config["Metadata"]["artist"]
    album = config["Metadata"]["album"]
    title = config["Metadata"]["title"]

    auth_token = config["PlayHT"]["auth_token"]
    user_id = config["PlayHT"]["user_id"]

    background_music_path = config["AudioPaths"]["background_music"]
    output_path = config["AudioPaths"]["output"]

    script_parts = OrderedDict()
    for key in config["Script"]:
        text, duration = config["Script"][key].rsplit(":", 1)
        script_parts[text.strip()] = int(duration)

    for key, value in script_parts.items():
        script_parts[key] = int(value)

    return (
        artist,
        album,
        title,
        auth_token,
        user_id,
        background_music_path,
        output_path,
        script_parts,
    )


def main():
    # Read values from config file
    CONFIG_PATH = "config.ini"
    (
        artist,
        album,
        title,
        auth_token,
        user_id,
        background_music_path,
        output_path,
        script_parts,
    ) = read_config(CONFIG_PATH)

    api = PlayHTAPI(auth_token=auth_token, user_id=user_id)

    generator = AudioGenerator(api, script_parts, background_music_path, output_path)
    generator.generate_audio()
    generator.add_metadata(title, artist, album)


if __name__ == "__main__":
    main()
