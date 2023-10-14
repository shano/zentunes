import os
import requests
import time


class PlayHTAPI:
    def __init__(self, auth_token, user_id):
        self.base_url = "https://play.ht/api/v2/tts"
        self.auth_token = auth_token
        self.user_id = user_id
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "AUTHORIZATION": auth_token,
            "X-USER-ID": user_id,
        }
        self.voice = "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"

    def get_audio(self, text, filename):
        if os.path.exists(filename):
            print(f"File '{filename}' already exists. Skipping.")
            return filename

        payload = {
            "text": text,
            "voice": self.voice,
            "quality": "draft",
            "output_format": "mp3",
            "speed": 1,
            "sample_rate": 24000,
            "voice_engine": "PlayHT2.0",
            "emotion": "female_happy",
            "voice_guidance": 3,
            "style_guidance": 20,
        }

        print(f"Posting text to Play.ht API: {text}")
        job_response = requests.post(self.base_url, json=payload, headers=self.headers)
        if job_response.status_code != 201:
            print(f"Error posting to Play.ht API: {job_response.text}")
            return None

        job_data = job_response.json()
        job_id = job_data.get("id")

        print(f"Job ID received: {job_id}")

        while True:
            print(f"Polling job status for ID: {job_id}")
            job_status_response = requests.get(
                f"{self.base_url}/{job_id}", headers=self.headers
            )
            if job_status_response.status_code != 200:
                print(f"Error fetching job status: {job_status_response.text}")
                return None

            job_status = job_status_response.json()
            print(
                f"Full job status response: {job_status}"
            )  # Print the entire response for diagnosis

            if job_status.get("output"):
                print("Job completed!")
                break
            else:
                print("Job still in progress...")

            time.sleep(5)  # Poll every 5 seconds

        print("Fetching the generated audio file...")
        # Fetch the audio file with the correct headers
        audio_response = requests.get(
            f"{self.base_url}/{job_id}",
            headers={
                "accept": "audio/mpeg",
                "AUTHORIZATION": self.auth_token,
                "X-USER-ID": self.user_id,
            },
        )

        if audio_response.status_code != 200:
            print(f"Error fetching audio file: {audio_response.text}")
            return None

        with open(filename, "wb") as audio:
            audio.write(audio_response.content)

        print(f"Audio saved to {filename}")
        return filename
