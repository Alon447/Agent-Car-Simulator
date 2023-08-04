import json

from fontTools.misc.py23 import xrange


class Roads_speed_buffer:
    def __init__(self, speeds_file_path,chunk_size):
        self.speeds_file_path = speeds_file_path
        self.current_slice = {}
        self.next_slice = {}
        self.chunk_size = chunk_size


    def load_next_slice(self):
        with open(self.speeds_file_path) as infile:
            o = json.load(infile)
            for i in range(0, len(o), self.chunk_size):
                print(o[i:(i + self.chunk_size)])