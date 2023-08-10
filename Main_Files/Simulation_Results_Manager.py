import json

class Simulation_Results_Manager:
    """
    Manages saving and reading simulation results to/from a JSON file.

    Attributes:
    graph_name (str): name of the graphml file.
    simulation_results (list): List of simulation result dictionaries.

    Methods:
    save_results_to_JSON(results): Saves simulation results to a JSON file.
    read_results_from_JSON(): Reads simulation results from a JSON file.

    """
    def __init__(self, graph_name):
        self.graph_name = graph_name
        self.simulation_results = []


    def save_results_to_JSON(self, results):
        """
        Save simulation results to a JSON file.

        Args:
        results (dict): Dictionary containing simulation results.

        Returns:
        None
        """
        self.simulation_results.append(results)
        with open(f'../Results/simulation_results_{self.graph_name}.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)

    def read_results_from_JSON(self):
        """
        Read simulation results from a JSON file.

        Returns:
        dict: Dictionary containing the loaded simulation results.
        """
        with open(f'../Results/simulation_results_{self.graph_name}.json', 'r') as infile:
            new_simulation_results = json.load(infile)
        return new_simulation_results