from typing import List, Union, Optional, Dict
from threadweave.dataloaders.base import BaseDataloader
import os
import requests

class CodeLoader(BaseDataloader):
    def __init__(self, source_path):
        self.source_path = source_path
        self.path_type = self._determine_path_type()

    def _determine_path_type(self):
        if self.source_path.startswith("https://github.com/"):
            return "github"
        else:
            return "local"

    def _read_local_directory(self):
        file_contents = {}
        for root, _, files in os.walk(self.source_path):
            for file in files:
                if file == ".DS_Store":
                    continue
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    relative_path = os.path.relpath(filepath, self.source_path)
                    file_contents[relative_path] = f.read()

        return file_contents

    def _verify_data(self):
        return super()._verify_data()

    def _fetch_github_directory(self, api_url):
        response = requests.get(api_url)
        response_json = response.json()

        file_contents = {}
        for item in response_json:
            if item['type'] == 'file':
                content = requests.get(item['download_url']).text
                file_contents[item['path']] = content
            elif item['type'] == 'dir':
                file_contents.update(self._fetch_github_directory(item['url']))
        return file_contents

    def load_data(self)-> Dict:
        #TODO Check for private repos and expect auth token
        #TODO Expand to use websites other than github as well
        if self.path_type == "local":
            return self._read_local_directory()
        elif self.path_type == "github":
            # Extract the user and repo from the GitHub URL
            parts = self.source_path.split("https://github.com/")[-1].split("/")
            user, repo = parts[0], parts[1]
            # Construct the API URL to fetch the directory content
            api_url = f"https://api.github.com/repos/{user}/{repo}/contents/"
            return self._fetch_github_directory(api_url)
        else:
            raise ValueError("Invalid path type")

# Example usage:
source_path_local = "/Users/test_code_chunker"
source_path_github = "https://github.com/user/project_xxx"

loader = CodeLoader(source_path_local)
print(loader.load_data())
