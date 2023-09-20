from tree_sitter import Node
import os
from enum import Enum
import subprocess

from fastchain.chunker.schema import Chunker
from tree_sitter import Parser, Language
from dataclasses import dataclass

@dataclass
class Span:
    start: int
    end: int

    def extract(self, s: str) -> str:
        return "\n".join(s.splitlines()[self.start:self.end])

    def __add__(self, other):
        if isinstance(other, int):
            return Span(self.start + other, self.end + other)
        elif isinstance(other, Span):
            return Span(self.start, other.end)
        else:
            raise NotImplementedError()

    def __len__(self):
        return self.end - self.start

class ProgrammingLanguage(str, Enum):
    """
    Enumeration for all programming languages that are supported"""

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
import subprocess
from dataclasses import dataclass
import traceback

from tree_sitter import Node

def chunker(tree, source_code_bytes, max_chunk_size=512 * 3, coalesce=50):
    # Recursively form chunks with a maximum chunk size of max_chunk_size
    def chunker_helper(node, source_code_bytes, start_position=0):
        chunks = []
        current_chunk = Span(start_position, start_position)
        for child in node.children:
            child_span = Span(child.start_byte, child.end_byte)
            if len(child_span) > max_chunk_size:
                chunks.append(current_chunk)
                chunks.extend(chunker_helper(child, source_code_bytes, child.start_byte))
                current_chunk = Span(child.end_byte, child.end_byte)
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
    current_chunk = Span(0, 0)
    while i < len(chunks):
        current_chunk += chunks[i]
        if count_length_without_whitespace(
                source_code_bytes[current_chunk.start:current_chunk.end].decode("utf-8")) > coalesce \
                and "\n" in source_code_bytes[current_chunk.start:current_chunk.end].decode("utf-8"):
            new_chunks.append(current_chunk)
            current_chunk = Span(chunks[i].end, chunks[i].end)
        i += 1
    if len(current_chunk) > 0:
        new_chunks.append(current_chunk)

    line_chunks = [Span(get_line_number(chunk.start, source_code=source_code_bytes),
                        get_line_number(chunk.end, source_code=source_code_bytes)) for chunk in new_chunks]
    line_chunks = [chunk for chunk in line_chunks if len(chunk) > 0]

    return line_chunks
@dataclass
class Span:
    start: int
    end: int

    def extract(self, s: str) -> str:
        return "\n".join(s.splitlines()[self.start:self.end])

    def __add__(self, other):
        if isinstance(other, int):
            return Span(self.start + other, self.end + other)
        elif isinstance(other, Span):
            return Span(self.start, other.end)
        else:
            raise NotImplementedError()

    def __len__(self):
        return self.end - self.start


def get_line_number(index: int, source_code: str) -> int:
    # unoptimized, use binary search
    lines = source_code.splitlines(keepends=True)
    total_chars = 0
    line_number = 0
    while total_chars <= index:
        if line_number == len(lines):
            return line_number
        total_chars += len(lines[line_number])
        line_number += 1
    return line_number - 1


def chunker(tree, source_code_bytes, max_chunk_size=512 * 3, coalesce=50):
    # Recursively form chunks with a maximum chunk size of max_chunk_size
    def chunker_helper(node, source_code_bytes, start_position=0):
        chunks = []
        current_chunk = Span(start_position, start_position)
        for child in node.children:
            child_span = Span(child.start_byte, child.end_byte)
            if len(child_span) > max_chunk_size:
                chunks.append(current_chunk)
                chunks.extend(chunker_helper(child, source_code_bytes, child.start_byte))
                current_chunk = Span(child.end_byte, child.end_byte)
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
    current_chunk = Span(0, 0)
    while i < len(chunks):
        current_chunk += chunks[i]
        if count_length_without_whitespace(
                source_code_bytes[current_chunk.start:current_chunk.end].decode("utf-8")) > coalesce \
                and "\n" in source_code_bytes[current_chunk.start:current_chunk.end].decode("utf-8"):
            new_chunks.append(current_chunk)
            current_chunk = Span(chunks[i].end, chunks[i].end)
        i += 1
    if len(current_chunk) > 0:
        new_chunks.append(current_chunk)

    line_chunks = [Span(get_line_number(chunk.start, source_code=source_code_bytes),
                        get_line_number(chunk.end, source_code=source_code_bytes)) for chunk in new_chunks]
    line_chunks = [chunk for chunk in line_chunks if len(chunk) > 0]

    return line_chunks


def count_length_without_whitespace(s: str):
    string_without_whitespace = re.sub(r'\s', '', s)
    return len(string_without_whitespace)

def chunker(tree, source_code_bytes, max_chunk_size=512 * 3, coalesce=50):
    # Recursively form chunks with a maximum chunk size of max_chunk_size
    def chunker_helper(node, source_code_bytes, start_position=0):
        chunks = []
        current_chunk = Span(start_position, start_position)
        for child in node.children:
            child_span = Span(child.start_byte, child.end_byte)
            if len(child_span) > max_chunk_size:
                chunks.append(current_chunk)
                chunks.extend(chunker_helper(child, source_code_bytes, child.start_byte))
                current_chunk = Span(child.end_byte, child.end_byte)
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
    current_chunk = Span(0, 0)
    while i < len(chunks):
        current_chunk += chunks[i]
        if count_length_without_whitespace(
                source_code_bytes[current_chunk.start:current_chunk.end].decode("utf-8")) > coalesce \
                and "\n" in source_code_bytes[current_chunk.start:current_chunk.end].decode("utf-8"):
            new_chunks.append(current_chunk)
            current_chunk = Span(chunks[i].end, chunks[i].end)
        i += 1
    if len(current_chunk) > 0:
        new_chunks.append(current_chunk)

    line_chunks = [Span(get_line_number(chunk.start, source_code=source_code_bytes),
                        get_line_number(chunk.end, source_code=source_code_bytes)) for chunk in new_chunks]
    line_chunks = [chunk for chunk in line_chunks if len(chunk) > 0]

    return line_chunks


class CodeChunker(Chunker):
    def __init__(self, directory_path: str):
        self.parser = None
        self.language = None
        self.directory_path: str = directory_path
    

    def get_files_from_directory(self):
        """
        Get all files from a directory
        """
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                yield os.path.join(root, file)


    def create_chunks(self):
        # Get the file extension
        file_list = self.get_files_from_directory()

        ext_list = [os.path.splitext(file)[1][len("."):] for file in file_list]
        unique_file_extensions = set(ext_list)

        # Get the language
        languages = [extension_to_language[ext] for ext in unique_file_extensions]

        # library_path = 'build/my-languages.so'

        try:
            print("Trying to load languages from library")
            languages_dict = {lang: Language(f"/tmp/{lang}.so", lang) for lang in languages}
        except:  
            print("Building languages from source")

            for lang in languages:
                subprocess.run(
                f"git clone https://github.com/tree-sitter/tree-sitter-{lang} cache/tree-sitter-{lang}",
                shell=True)

                Language.build_library(f'cache/build/{lang}.so', [f"cache/tree-sitter-{lang}"])
                subprocess.run(f"cp cache/build/{lang}.so /tmp/{lang}.so", shell=True)  # copying for executability

            languages_dict = {lang: Language(f"/tmp/{lang}.so", lang) for lang in languages}

        parser = Parser()
        parser.set_language(languages_dict[languages[0]])        
        
        code_byte = bytes("""
                def xyz():
                    if bar:
                        baz()
                def foo(x):
                    print(x)
                    return x
                """, "utf8")
        tree = parser.parse(code_byte)
            
        spans = chunker(tree, code_byte, max_chunk_size=10, coalesce=10)
        for s in spans:
            print(s.extract("""
                def xyz():
                    if bar:
                        baz()
                def foo(x):
                    print(x)
                    return x
                """))
            print("---")

        return True



if __name__ == "__main__":
    chunkern = CodeChunker(directory_path="/Users/aquibkhan/Desktop/fastchain/fastchain/tests/")
    print(chunkern.create_chunks())