# VoiceID AI Pro

VoiceID AI Pro is a desktop speaker-recognition workflow built with CustomTkinter, SQLite, and audio tooling for login, signup, enrollment, playback, upload, and voice sample management.

## Features

- Secure signup and login with hashed passwords
- Multi-user speaker list pulled from the database
- Voice recorder with play/delete controls
- Voice enrollment folder per user
- Audio upload into the active user dataset
- Sidebar navigation with logout
- SQLite-backed user storage and recordings table

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m app.main
```

## Notes

- New users created from signup are stored in SQLite and appear in the speaker dropdown and dashboard user list.
- Recorded samples are saved under `dataset/<username>/`.
- Uploading audio copies the selected file into the current user's dataset folder.