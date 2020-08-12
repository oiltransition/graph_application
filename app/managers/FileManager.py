import os
import yaml
import plotly

class FileManager:

    def __init__(self):
        # Creating the directory where files will be saved to
        main_path = os.path.expanduser('~')
        self.path_to_save_results = os.path.join(main_path, "shell_results")
        if not os.path.exists(self.path_to_save_results):
            os.mkdir(self.path_to_save_results)
    
    '''
    This method generates the name to be used for naming the file containing
    data or graph of a given variable.
    '''
    def __get_filename_for_variable(self, variable_name, extension):
        return variable_name.lower().replace(" ","_")+extension

    def export_dataframe_to_csv(self, df, variable_name):
        filename = self.__get_filename_for_variable(variable_name, ".csv")
        path_to_export_file = "{}/{}".format(self.path_to_save_results, filename)
        df.to_csv(index = False, path_or_buf=path_to_export_file)

    def save_figure_for_variable(self, fig, variable_name):
        filename = self.__get_filename_for_variable(variable_name, ".html")
        path = "{}/{}".format(self.path_to_save_results, filename)
        plotly.offline.plot(fig, filename=path)

    def get_input_file_path_for_variable_name(self, variable_name):
        filename = self.__get_filename_for_variable(variable_name, ".csv")
        return "{}/{}".format(self.path_to_save_results, filename)

    def get_variable_data(self):
        with open("Data.yaml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data
