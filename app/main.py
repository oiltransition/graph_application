import argparse
import os
import sys
from InputFileGenerator import InputFileGenerator
from FileManager import FileManager
from GraphGenerator import GraphGenerator

# Generating the path to the input file
pwd = os.getcwd()
complete_filepath =  os.path.join(pwd, "input_file.csv")

# Ensuring the file is present in the project
if not os.path.isfile(complete_filepath):
    print("The input file not found")
    sys.exit()

# Creating the objects we need
input_file_generator = InputFileGenerator(complete_filepath)
file_manager = FileManager()
graphGenerator = GraphGenerator()

# Getting the dictionary with all in data to be analyzed
all_variable_data = file_manager.get_variable_data()
single_variable_data = all_variable_data["Single Variable"]
multi_variable_data = all_variable_data["Multivariable"]

# For each single variable data, generate the input file
for key in single_variable_data.keys():
    variable = single_variable_data[key]
    
    # Generating and saving the input file
    df = input_file_generator.get_dataframe_from_single_variable(variable["variable_name"])
    file_manager.save_dataframe_to_csv(df,variable["variable_name"])
    
    # Generating the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(variable["variable_name"])
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.save_figure_for_variable_name(figure, variable["variable_name"])

# For each multivariable data, generate the input file
for key in multi_variable_data.keys():
    variable = multi_variable_data[key]
    
    # Generating and saving the input file
    df = input_file_generator.get_dataframe_from_multi_variable(variable)
    file_manager.save_dataframe_to_csv(df,variable["variable_name"])

    # Generating the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(variable["variable_name"])
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.save_figure_for_variable_name(figure, variable["variable_name"])

# Printing where to find the results
print("All results saved at: {}".format(file_manager.path_to_save_results))
    