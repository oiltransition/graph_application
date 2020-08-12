import os
import yaml
import plotly

'''
This class is responsible for handling file operations such as:
- Opening 
- Exporting
- Determining existances
'''
class FileManager:

    def __init__(self):
        # Creating the directory where files will be saved to
        main_path = os.path.expanduser('~')
        self.path_to_save_results = os.path.join(main_path, "shell_results")
        if not os.path.exists(self.path_to_save_results):
            os.mkdir(self.path_to_save_results)

        # Setting the location of the Data.yaml file and input_file.csv file
        pwd = os.getcwd()
        self.data_file_location =  os.path.join(pwd, "Data.yaml")
        self.input_file_location = os.path.join(pwd, "input_file.csv")
    
    '''
    Generates the name to be used for naming the file containing
    data or graph of a given variable.
    '''
    def __get_filename_from_variable_name(self, variable_name, extension):
        return variable_name.lower().replace(" ","_")+extension

    '''
    Provides the complete path of where a file is going to be exported to.
    '''
    def __get_export_file_path_for_variable(self, variable, extension):
        variable_name = variable["variable_name"]
        filename = self.__get_filename_from_variable_name(variable_name, extension)
        return "{}/{}".format(self.path_to_save_results, filename)

    def export_dataframe_for_variable(self, df, variable):
        path_to_export_file = self.__get_export_file_path_for_variable(variable, ".csv")
        df.to_csv(index = False, path_or_buf=path_to_export_file)

    def export_figure_for_variable(self, fig, variable):
        path_to_export_file = self.__get_export_file_path_for_variable(variable, ".html")
        plotly.offline.plot(fig, filename=path_to_export_file)

    '''
    Provides the location of the file containing the data used for 
    generating the graph of a given variable.
    '''
    def get_input_file_path_for_variable_name(self, variable):
        variable_name = variable["variable_name"]
        filename = self.__get_filename_from_variable_name(variable_name, ".csv")
        return "{}/{}".format(self.path_to_save_results, filename)

    def get_variable_data(self):
        with open("Data.yaml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data

    def is_data_file_available(self):
        return os.path.isfile(self.data_file_location)

    def is_input_file_available(self):
        return os.path.isfile(self.input_file_location)