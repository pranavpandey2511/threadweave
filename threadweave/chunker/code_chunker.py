from __future__ import annotations
from tree_sitter import Node
import os
from enum import Enum
import subprocess
from docarray.array import DocList

from typing import Dict
from threadweave.chunker.base import Chunker, Span
from tree_sitter import Parser, Language
from dataclasses import dataclass
from threadweave.chunker.utils import read_file_content
from threadweave.document.chunk.schema import CodeChunk
from threadweave.document.base import Document, Page, Metadata, Chunk


extension_to_language = {
    "mjs": "tsx",
    "py": "python",
    "rs": "rust",
    "go": "go",
    "java": "java",
    "cpp": "cpp",
}


import os

import re
class ProgrammingLanguage(str, Enum):

    """
    Enumeration for all programming languages that are supported
    """

    PYTHON = "python"
    MOJO = "mojo"
    RST = "rst"
    RUBY = "ruby"
    GO = "go"
    CPP = "cpp"
    JAVA = "java"
    JS = "js"
    TS = "ts"
    PHP = "php"
    PROTO = "proto"
    RUST = "rust"
    SCALA = "scala"
    SQL = "sql"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    MARKDOWN = "markdown"
    LATEX = "latex"
    HTML = "html"
    CSHARP = "csharp"
import subprocess


def count_length_without_whitespace(s: str):
    string_without_whitespace = re.sub(r"\s", "", s)
    return len(string_without_whitespace)


class CodeChunker(Chunker):
    def __init__(
        self, content_dict: Dict, max_chunk_size: int = 20, coalesce: int = 5
    ):
        self.parser = None
        self.language = None
        self.content_dict = content_dict
        self.max_chunk_size = max_chunk_size
        self.coalesce = coalesce
        self.chunks = DocList()


    def chunker(
        self, tree, source_code_bytes, max_chunk_size=512 * 3, coalesce=50
    ):
        # Recursively form chunks with a maximum chunk size of max_chunk_size
        # https://github.com/sweepai/sweep/blob/b267b613d4c706eaf959fe6789f11e9a856521d1/sweepai/utils/utils.py#L81
        def chunker_helper(node, source_code_bytes, start_position=0):
            chunks = []
            current_chunk = Span(start=start_position, end=start_position)
            for child in node.children:
                child_span = Span(start=child.start_byte, end=child.end_byte)
                if len(child_span) > max_chunk_size:
                    chunks.append(current_chunk)
                    chunks.extend(
                        chunker_helper(
                            child, source_code_bytes, child.start_byte
                        )
                    )
                    current_chunk = Span(start=child.end_byte, end=child.end_byte)
                elif len(current_chunk) + len(child_span) > max_chunk_size:
                    chunks.append(current_chunk)
                    current_chunk = child_span
                else:
                    current_chunk += child_span
            if len(current_chunk) > 0:
                chunks.append(current_chunk)
            return chunks

        chunks = chunker_helper(tree.root_node, source_code_bytes)

        # removing gaps
        for prev, curr in zip(chunks[:-1], chunks[1:]):
            prev.end = curr.start

        # combining small chunks with bigger ones
        new_chunks = []
        i = 0
        current_chunk = Span(start=0, end=0)
        while i < len(chunks):
            current_chunk += chunks[i]
            if count_length_without_whitespace(
                source_code_bytes[
                    current_chunk.start : current_chunk.end
                ].decode("utf-8")
            ) > coalesce and "\n" in source_code_bytes[
                current_chunk.start : current_chunk.end
            ].decode(
                "utf-8"
            ):
                new_chunks.append(current_chunk)
                current_chunk = Span(start=chunks[i].end, end=chunks[i].end)
            i += 1
        if len(current_chunk) > 0:
            new_chunks.append(current_chunk)

        line_chunks = [
            Span(start=
                self._get_line_number(
                    chunk.start, source_code=source_code_bytes
                ),
                end=self._get_line_number(chunk.end, source_code=source_code_bytes),
            )
            for chunk in new_chunks
        ]
        line_chunks = [chunk for chunk in line_chunks if len(chunk) > 0]

        return line_chunks

    def _get_line_number(self, index: int, source_code: str) -> int:
        # optimized, use binary search
        lines = source_code.splitlines(keepends=True)
        left, right = 0, len(lines)
        total_chars = 0
        while left < right:
            mid = (left + right) // 2
            if total_chars + len(lines[mid]) > index:
                right = mid
            else:
                total_chars += len(lines[mid])
                left = mid + 1
        return left

    def create_chunks(self):
        # Get the file extension
        file_list = self.content_dict.keys()
        ext_list = [os.path.splitext(file)[1][len(".") :] for file in file_list]
        ext_list = set(extension_to_language.keys()).intersection(set(ext_list))
        unique_file_extensions = ext_list 

        # Get the language
        languages = [
            extension_to_language[ext] for ext in unique_file_extensions
        ]

        try:
            print("Trying to load languages from library")
            languages_dict = {
                lang: Language(f"/tmp/{lang}.so", lang) for lang in languages
            }
        except:
            print("Building languages from source")

            for lang in languages:
                subprocess.run(
                    f"git clone https://github.com/tree-sitter/tree-sitter-{lang} cache/tree-sitter-{lang}",
                    shell=True,
                )

                Language.build_library(
                    f"cache/build/{lang}.so", [f"cache/tree-sitter-{lang}"]
                )
                subprocess.run(
                    f"cp cache/build/{lang}.so /tmp/{lang}.so", shell=True
                )  # copying for executability

            languages_dict = {
                lang: Language(f"/tmp/{lang}.so", lang) for lang in languages
            }

        parser = Parser()
        for lang in languages:
            parser.set_language(languages_dict[lang])

        
        self.pages = DocList()
        all_chunks = DocList()
        meta_data = Metadata()
        document  = Document(metadata=meta_data, pages=None)
        

        for ids, (file, content) in enumerate(self.content_dict):
            self.chunks = DocList()

            # file_content = read_file_content(file)
            code_byte = bytes(content, "utf8")

            tree = parser.parse(code_byte)
            spans = self.chunker(
                tree,
                code_byte,
                max_chunk_size=self.max_chunk_size,
                coalesce=self.coalesce,
            )

            for span in spans:
                chunk=CodeChunk(content=span.extract(content))
                all_chunks.append(chnk)
                self.chunks.append(
                    chnk
                )

            self.pages.append(
                Page(page_info=file, doc_id=str(ids), chunks=self.chunks)
            )

        document.chunks = all_chunks
        document.pages = self.pages
        return document
