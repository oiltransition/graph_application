import argparse
import os
import sys
from managers.InputFileGenerator import InputFileGenerator
from managers.FileManager import FileManager
from managers.GraphGenerator import GraphGenerator

# Create objects
file_manager = FileManager()
input_file_generator = InputFileGenerator(file_manager.input_file_location)
graphGenerator = GraphGenerator()

# Ensure the input file is present in the project
if not file_manager.is_input_file_available():
    raise FileNotFoundError(file_manager.input_file_location)

# Ensure the data file is present in the project
if not file_manager.is_data_file_available():
    raise FileNotFoundError(file_manager.data_file_location)

# Get the dictionary with all in data to be analyzed
all_variable_data = file_manager.get_variable_data()
single_variable_data = all_variable_data["Single Variable"]
multi_variable_data = all_variable_data["Multivariable"]
cummulative_single_variable_data = all_variable_data["Cumulative Single Variable"]

# Single variable Analysis
for key in single_variable_data.keys():
    variable = single_variable_data[key]

    # Generate and save the input file to then be used for generating the graph
    df = input_file_generator.get_dataframe_from_single_variable(variable)
    file_manager.export_dataframe_for_variable(df, variable)

    # Generate the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(variable)
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.export_figure_for_variable(figure, variable)

# Multivariable Analysis
for key in multi_variable_data.keys():
    variable = multi_variable_data[key]

    # Generate and save the input file to then be used for generating the graph
    df = input_file_generator.get_dataframe_from_multi_variable(variable)
    file_manager.export_dataframe_for_variable(df, variable)

    # Generate the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(variable)
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.export_figure_for_variable(figure, variable)

# Cumulative - Single Variable Analysis
for key in cummulative_single_variable_data.keys():
    # To differentiate cumulative from non-cumulative, we need to pass allow rename files with the "cumulative" keyword.

    # Generate and save the input file to then be used for generating the graph

    # Generate the graph

    pass

# Print where to find the results
print("All results saved at: {}".format(file_manager.path_to_save_results))
