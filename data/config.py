import json
import os


class JSONStructure:
    def __init__(self, file_path):
        self.file = file_path
        self._load_file()

    def _load_file(self):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            raise FileNotFoundError(f"File {self.file} not found")

    def __getitem__(self, item):
        return self.data.get(item)

    def get(self, item, default=None):
        return self.data.get(item, default)

config = JSONStructure(file_path="data/config.json")
messages = JSONStructure(file_path="data/messages.json")
