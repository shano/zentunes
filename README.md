# Zentunes

Zentunes is a project that combines scripted instructions with background music to produce a single audio file. It's tailored for guided exercises like stretches, meditation, and workouts, using the PlayHT API to generate voice instructions and then combining those with background music.

## Configuration

The config.ini file is the heart of Zentunes, driving the audio generation process. Here's a breakdown of each section:

### Metadata

This section captures the metadata for the final audio file.

```ini
[Metadata]
artist = Me
album = Healthy Stuff
title = Stretch 5 min, lower back
```

### PlayHT

Your authentication tokens for the PlayHT API.

```ini
[PlayHT]
auth_token = YOUR_AUTH_TOKEN
user_id = YOUR_USER_ID
```

NOTE: Never commit your config.ini with actual authentication tokens to public repositories. It's a security risk.

### AudioPaths

Specify the path to the background music and the final output path.

```ini
[AudioPaths]
background_music = tmp_audio/background_music.mp3
output = final_result.mp3
```

### Script

The script is an ordered list of instructions. Each line should have an enumerated key, followed by the instruction and its duration in seconds separated by a colon.

```ini
[Script]
1 = Get ready to start with the Knee to Chest Stretch.:5
...
10 = Great job! You're done.:5
```

## Running Zentunes

Ensure you've set up the environment using Poetry.
Fill in the config.ini file with the appropriate details.
Execute the main script:

```bash
poetry run python zentunes.py
```

This will generate the audio file based on your script and background music, then combine them, and lastly, append the metadata.