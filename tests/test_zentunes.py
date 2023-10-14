import pytest
from zentunes.zentunes import PlayHTAPI, AudioGenerator, read_config
from collections import OrderedDict
from unittest.mock import MagicMock, patch


def test_get_audio_successful():
    api = PlayHTAPI(auth_token="test_token", user_id="test_id")
    api.get_audio = MagicMock(return_value="voice_part_0.mp3")
    result = api.get_audio("Test text", "voice_part_0.mp3")
    assert result == "voice_part_0.mp3"


def test_add_metadata():
    # Mock eyed3 to avoid actually editing the MP3 metadata in the test
    with patch("zentunes.zentunes.eyed3.load") as mock_load:
        mock_audiofile = MagicMock()
        mock_load.return_value = mock_audiofile
        AudioGenerator.add_metadata_to_mp3(
            "test_path.mp3", "test_title", "test_artist", "test_album"
        )
        assert mock_audiofile.tag.artist == "test_artist"
        assert mock_audiofile.tag.album == "test_album"
        assert mock_audiofile.tag.title == "test_title"


@pytest.fixture
def sample_script_parts():
    return OrderedDict({"Test part 1": 5, "Test part 2": 10})


def test_generate_audio(sample_script_parts):
    api = PlayHTAPI(auth_token="test_token", user_id="test_id")
    generator = AudioGenerator(
        api, sample_script_parts, "mock_background_music.mp3", "mock_output.mp3"
    )

    # Mock the `get_audio` method to avoid API calls and just return a dummy path
    api.get_audio = MagicMock(return_value="voice_part_0.mp3")
    # Mock `AudioSegment.from_file` to avoid file operations
    with patch("zentunes.zentunes.AudioSegment.from_file") as mock_from_file:
        mock_segment = MagicMock()
        mock_from_file.return_value = mock_segment
        generator.generate_audio()
        assert (
            mock_from_file.call_count == 3
        )  # Two parts in the script and the background music


def test_read_config_valid_file(tmpdir):
    # Create a temporary config file
    config_content = """
    [Metadata]
    artist = Me
    album = Healthy Stuff
    title = Stretch 5 min, lower back

    [PlayHT]
    auth_token = test_token
    user_id = test_id

    [AudioPaths]
    background_music = test_music.mp3
    output = test_output.mp3

    [Script]
    1 = Part 1:5
    2 = Part 2:10
    """
    config_file = tmpdir.join("test_config.ini")
    config_file.write(config_content)

    # Test read_config function
    (
        artist,
        album,
        title,
        auth_token,
        user_id,
        background_music,
        output,
        script_parts,
    ) = read_config(config_file.strpath)

    assert artist == "Me"
    assert album == "Healthy Stuff"
    assert title == "Stretch 5 min, lower back"
    assert auth_token == "test_token"
    assert user_id == "test_id"
    assert background_music == "test_music.mp3"
    assert output == "test_output.mp3"
    assert script_parts == OrderedDict({"Part 1": 5, "Part 2": 10})
