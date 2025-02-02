from typing import List, Union, Optional, Dict
from enum import Enum
from pathlib import Path
import uuid
import fitz
import os
from unidecode import unidecode
from datetime import datetime
import logging

from threadweave.dataloaders.chunkers.token_chunker import (
    chunk_text_by_token_limit,
)
from .base import BaseDataloader
from docarray.array import DocList, DocVec
from threadweave.document.base import Document, Page, Metadata
from threadweave.document.chunk.schema import (
    TextChunk,
    ImageChunk,
    FigureCaptionChunk,
)
from utils import num_tokens_from_string, is_valid_url

logger = logging.getLogger(__name__)


class Chunking(Enum):
    STRUCTURED = 1
    SENTENCES = 2
    FIXED_SIZE = 3


class PyPDFLoader(BaseDataloader):
    def __init__(
        self,
        file_path: Union[str, Path],
        include_metadata: bool = True,
        extra_info: Optional[Dict] = None,
        *,
        token_limit=512,
        **kwargs,
    ):
        if not isinstance(file_path, (str, Path)):
            raise TypeError("file_path must be a string or Path.")

        self.file_path = file_path
        self.include_metadata = include_metadata
        self.extra_info = extra_info if extra_info else {}

        self.summary = ""
        self.pages = DocList()
        self.sections = DocList()
        self.token_limit = token_limit

        try:
            self.doc = fitz.open(str(file_path))
        except Exception as e:
            raise Exception(f"Failed to open {file_path}: {str(e)}")

        self.metadata = Metadata(
            path=file_path,
            version=kwargs.get("version", "0.0.1"),
            total_pages=self.doc.page_count,
            date_created=datetime.now(),
            data_modified=datetime.now(),
            date_processed=datetime.now(),
        )

    def load_and_split(self) -> Document:
        self.pdf_metadata = self.doc.metadata

        for page_number, page in enumerate(self.doc):
            page_content = []
            output = page.get_text("blocks")
            previous_block_id = 0
            for block in output:
                # The first four entries are the block’s bbox coordinates, block_type is 1 for an image block, 0 for text.
                # block_no is the block sequence number. Multiple text lines are joined via line breaks.
                x0, y0, x1, y1, block_data, block_num, block_type = block
                coordinates = x0, y0, x1, y1
                if block_type != 0:  # Not text
                    continue

                text_block = unidecode(block_data)

                # Get number of tokens in the content
                num_tokens = num_tokens_from_string(text_block)
                text_chunks = chunk_text_by_token_limit(
                    text_block, self.token_limit
                )

                for chunk in text_chunks:
                    self.sections.append(TextChunk(content=chunk))
            self.pages.append(
                Page(page_number=page_number), sections=self.sections
            )

        return {
            str(self.file_path): Document(
                metadata=self.metadata,
            )
        }


class PdfDataLoader(BaseDataloader):
    def __init__(
        self,
        path: Union[str, List[str], Path, List[Path]],
        recursive: bool = True,
        include_metadata: bool = True,
        *,
        exclude: List[str] = [],
        chunking=Chunking.STRUCTURED,
        **kwargs,
    ) -> None:
        self.path = path if isinstance(path, list) else [path]
        self.recursive = recursive
        self.include_metadata = include_metadata
        self.exclude = exclude

        pdf_files = self._get_pdf_files()
        self.loaders = {
            str(file_path): PyPDFLoader(file_path, include_metadata)
            for file_path in pdf_files
        }

    def _get_pdf_files(self) -> List[Union[str, Path]]:
        pdf_files = []
        for file_path in self.path:
            path = Path(file_path)
            if self._check_dir(file_path):
                if self.recursive:
                    pdf_files.extend([str(p) for p in path.rglob("*.pdf")])
                else:
                    pdf_files.extend([str(p) for p in path.glob("*.pdf")])
            elif path.is_file() and path.suffix == ".pdf":
                pdf_files.append(str(path))

        return [file for file in pdf_files if file not in self.exclude]

    def load_data(self) -> Dict:
        output = {}
        for file_path, loader in self.loaders.items():
            output.update(loader.load_and_split())
        self._verify_data(output)

        return output

    def _verify_data(self, data: Dict) -> bool:
        for file_path, content in data.items():
            if os.path.exists(file_path):
                if not any(content):
                    raise ValueError("No pages found in the PDF file")
                continue
            else:
                raise ValueError(f"File doesn't exist {file_path}")
        return True

    @staticmethod
    def _check_dir(path: str) -> bool:
        path = Path(path)
        return path.is_dir()


def main():
    documents = PdfDataLoader()


if __name__ == "__main__":
    main()
