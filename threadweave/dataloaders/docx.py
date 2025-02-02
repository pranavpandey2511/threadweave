import os
import tempfile
from tempfile import SpooledTemporaryFile
from typing import IO, BinaryIO, List, Optional, Tuple, Union, cast

from docx import Document as WordDocument
from docx.oxml.shared import qn
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from threadweave.dataloaders.base import BaseDataloader


class DocXDataLoader(BaseDataloader):
    def _verify_data(self):
        pass

    def load_data(self, filepath, *args, **kwargs):
        document = WordDocument(filepath)
        sections = self._section_handler(document.sections)

    def _section_handler(self, sections):
        pass

    def _table_handler(self, table):
        pass
