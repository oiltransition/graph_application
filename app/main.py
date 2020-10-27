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

# Create a dictionary were all dataframes will be stored
dataframe_result_dict = {}

# Generate a df for each item in the YAML file
for analysis_type, value in all_variable_data.items():
    for variable_key, variable_data in value.items():
        # Printing progress
        print(f"> {variable_key}")

        # Set "False" as default
        is_cumulative = False

        # Generate a dataframe based on the analysis type
        if analysis_type == "Single Variable":
            df = input_file_generator.get_dataframe_from_single_variable(variable_data)
        elif analysis_type == "Multivariable":
            df = input_file_generator.get_dataframe_from_multi_variable(variable_data)
        elif analysis_type == "Cumulative Single Variable":
            is_cumulative = True
            df = input_file_generator.get_dataframe_for_cummulative_single_variable(
                variable_data
            )

        # Save the dataframe into the dictionary
        dataframe_result_dict[variable_key] = {
            "variable": variable_data,
            "dataframe": df,
            "is_cumulative": is_cumulative,
        }

# Export dataframe and generate graphs
for data in dataframe_result_dict.values():

    # Get data of importance
    df = data["dataframe"]
    is_cumulative = data["is_cumulative"]
    variable = data["variable"]

    # Export the dataframe to a file
    file_manager.export_dataframe_for_variable(df, variable, is_cumulative)

    # Generate the graph
    path_to_input_file = file_manager.get_input_file_path_for_variable_name(
        variable, is_cumulative
    )
    figure = graphGenerator.get_figure_for_variable(variable, path_to_input_file)
    file_manager.export_figure_for_variable(figure, variable, is_cumulative)

# Print where to find the results
print("All results saved at: {}".format(file_manager.path_to_save_results))
