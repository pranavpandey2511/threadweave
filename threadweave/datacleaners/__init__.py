from __future__ import annotations

import os
from abc import ABC, abstractmethod


class BaseCleaner(ABC):
    """Base cleaner class for creating cleaners

    Args:
        ABC (abstract): Abstract class inherited
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def _verify_data(self):
        pass

    def _get_dirs(self, path: str) -> List[str]:
        """Get all the directories in a path

        Args:
            path (str): Path to the directory

        Returns:
            List[str]: List of directories
        """
        return [x[0] for x in os.walk(path)]
