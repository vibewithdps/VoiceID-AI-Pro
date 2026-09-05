from pathlib import Path
from app.auth.session import Session


class EnrollmentService:

    REQUIRED_SAMPLES = 20

    def __init__(self):

        user = Session.current_user()

        if user is None:
            raise Exception("No logged in user.")

        self.user_id = user[0]
        self.full_name = user[1]
        self.username = user[2] or user[1]

        self.dataset_folder = Path("dataset") / self.username

        self.dataset_folder.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------

    def get_dataset_path(self):

        return self.dataset_folder

    # -----------------------------------------

    def get_samples(self):

        files = []

        for ext in ("*.wav", "*.mp3", "*.m4a"):

            files.extend(self.dataset_folder.glob(ext))

        files = sorted(files)

        return files

    # -----------------------------------------

    def sample_count(self):

        return len(self.get_samples())

    # -----------------------------------------

    def progress(self):

        return min(
            self.sample_count(),
            self.REQUIRED_SAMPLES
        )

    # -----------------------------------------

    def progress_percent(self):

        return int(
            self.progress()
            / self.REQUIRED_SAMPLES
            * 100
        )

    # -----------------------------------------

    def is_ready_for_training(self):

        return self.sample_count() >= self.REQUIRED_SAMPLES

    # -----------------------------------------

    def next_filename(self):

        number = self.sample_count() + 1

        return self.dataset_folder / f"voice_{number:03}.wav"

    # -----------------------------------------

    def delete_last(self):

        samples = self.get_samples()

        if not samples:

            return False

        samples[-1].unlink()

        return True

    def save_recording(self, source_file):

        source_path = Path(source_file)

        destination = self.next_filename()

        if source_path.resolve() != destination.resolve():
            source_path.replace(destination)

        return destination