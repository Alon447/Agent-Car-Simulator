import json

import pandas as pd
from matplotlib import pyplot as plt


class Simulation_Results_Manager:
    def __init__(self):
        self.simulation_results = []


    def save_results_to_JSON(self, results, simulation_id):
        self.simulation_results.append(results)
        with open('simulation_results.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)

    def read_results_from_JSON(self):
        with open('simulation_results.json', 'r') as infile:
            new_simulation_results = json.load(infile)
        # Convert the simulation results to a DataFrame
        results_df = pd.DataFrame(new_simulation_results)
        return new_simulation_results

SRM = Simulation_Results_Manager()
SRM.read_results_from_JSON()