import new_master.Roads_speed_buffer as rsb
import random
import json
import pandas as pd

def test_load_next_slice():
    generate_random_json()
    speeds_file_path = "speeds.json"
    chunk_size = 200
    rsb1 = rsb.Roads_speed_buffer(speeds_file_path,chunk_size)
    rsb1.load_next_slice()
    return

def generate_random_json():
    content = {}
    for i in range(10):
        content[i] = random.randint(0,100)
        with open('speeds.json', 'w') as outfile:
            json.dump(content[i], outfile)


generate_random_json()
with open('../new_master/simulation_results.json') as file:
    chunks = pd.read_json(file, lines=True, chunksize = 10)
    for c in chunks:
        print(c)