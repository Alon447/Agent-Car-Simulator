import json


def save_results_to_JSON(graph_name, results):
    """
    Save simulation results to a JSON file.

    Args:
    results (dict): Dictionary containing simulation results.

    Returns:
    None
    """
    # self.simulation_results.append(results)
    json_name = f'simulation_results_{graph_name}'
    with open(f'../Results/{json_name}.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)
    return json_name


def read_results_from_JSON(graph_name):
    """
    Read simulation results from a JSON file.

    Returns:
    dict: Dictionary containing the loaded simulation results.
    """
    with open(f'../Results/simulation_results_{graph_name}.json', 'r') as infile:
        new_simulation_results = json.load(infile)
    return new_simulation_results