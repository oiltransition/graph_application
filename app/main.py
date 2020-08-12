import argparse
import os
import sys
from managers.InputFileGenerator import InputFileGenerator
from managers.FileManager import FileManager
from managers.GraphGenerator import GraphGenerator

# Creating objects
file_manager = FileManager()
input_file_generator = InputFileGenerator(file_manager.input_file_location)
graphGenerator = GraphGenerator()

# Ensuring the input file is present in the project
if not file_manager.is_input_file_available():
    raise FileNotFoundError(file_manager.input_file_location)

# Ensuring the data file is present in the project
if not file_manager.is_data_file_available():
    raise FileNotFoundError(file_manager.data_file_location)

# Getting the dictionary with all in data to be analyzed
all_variable_data = file_manager.get_variable_data()
single_variable_data = all_variable_data["Single Variable"]
multi_variable_data = all_variable_data["Multivariable"]

# Single variable Analysis
for key in single_variable_data.keys():
    variable = single_variable_data[key]
    
    # Generating and saving the input file to then be used for generating the graph
    df = input_file_generator.get_dataframe_from_single_variable(variable["variable_name"])
    file_manager.export_dataframe_for_variable(df,variable)
    
    # Generating the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(variable)
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.export_figure_for_variable(figure, variable)

# Multivariable Analysis
for key in multi_variable_data.keys():
    variable = multi_variable_data[key]
    
    # Generating and saving the input file to then be used for generating the graph
    df = input_file_generator.get_dataframe_from_multi_variable(variable)
    file_manager.export_dataframe_for_variable(df,variable)

    # Generating the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(variable)
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.export_figure_for_variable(figure, variable)

# Printing where to find the results
print("All results saved at: {}".format(file_manager.path_to_save_results))
    