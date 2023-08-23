import os
import pathlib
from datetime import datetime, timedelta
from logging import handlers
from zipfile import ZIP_DEFLATED, ZipFile


class CustomRotatingFileHandler(handlers.RotatingFileHandler):
    """Custom handler for logs."""

    def __init__(
        self,
        filename,
        mode="a",
        maxBytes=0,
        backupCount=0,
        encoding=None,
        delay=0,
        errors=None,
    ):
        """Create an instance of handler."""
        pathlib.Path(filename).parent.mkdir(exist_ok=True)
        handlers.RotatingFileHandler.__init__(
            self,
            filename,
            mode,
            maxBytes,
            backupCount,
            encoding,
            delay,
            errors,
        )
        self.start_time = datetime.fromtimestamp(
            os.path.getctime(self.baseFilename)
        )
        self.archive_time = self.start_time + timedelta(days=30)

    def make_archive(self):
        """Create an archive of logs."""
        dir_path, base_filename = os.path.split(self.baseFilename)
        logs_list = [
            f
            for f in os.listdir(dir_path)
            if all(
                [
                    f.startswith(base_filename),
                    f != base_filename,
                    not f.endswith(".zip"),
                ]
            )
        ]
        str_date = datetime.now().strftime("%H-%M %d %B %Y")
        if len(logs_list) > 0:
            with ZipFile(
                f"logs/archive_{str_date}.zip",
                "a",
                compression=ZIP_DEFLATED,
                compresslevel=3,
            ) as zip_file:
                for f in logs_list:
                    file = os.path.join(dir_path, f)
                    zip_file.write(file, os.path.basename(file))
                    os.remove(file)

    def shouldRollover(self, record):
        """Check the logs archiving."""
        if datetime.now() > self.archive_time:
            self.make_archive()
            self.archive_time = datetime.now() + timedelta(days=30)
        return super().shouldRollover(record)
