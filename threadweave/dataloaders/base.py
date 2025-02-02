from abc import ABC, abstractmethod
from uuid import uuid4
from pydantic import BaseModel
from typing import Optional, Union, List, Tuple, Dict, Type
import os


class BaseDataloader(ABC):
    """Base dataloader class for creating dataloaders

    Args:
        ABC (abstract): Abstract class inherited
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def load_data(self):
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
