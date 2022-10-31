from pathlib import Path
from typing import Protocol


class Downloadable(Protocol):
    def download(self) -> Path:
        """Acquire a downloadable asset that can be stored in a file.

        Returns:
            Path: The path to the downloaded asset.

        Raises:
            Exception: When the download encounters an error.
        """
        ...

