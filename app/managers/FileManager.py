import os
import yaml
import plotly

class FileManager:

    def __init__(self):
        # Creating the directory to save files at
        main_path = os.path.expanduser('~')
        self.path_to_save_results = os.path.join(main_path, "shell_results")
        if not os.path.exists(self.path_to_save_results):
            os.mkdir(self.path_to_save_results)
    
    def __get_filename_from_variable_name(self, variable_name, extension):
        return variable_name.lower().replace(" ","_")+extension

    def save_dataframe_to_csv(self, df, variable_name):
        filename = self.__get_filename_from_variable_name(variable_name, ".csv")
        path = "{}/{}".format(self.path_to_save_results, filename)
        df.to_csv(index = False, path_or_buf=path)

    def save_figure_for_variable_name(self, fig, variable_name):
        filename = self.__get_filename_from_variable_name(variable_name, ".html")
        path = "{}/{}".format(self.path_to_save_results, filename)
        plotly.offline.plot(fig, filename=path)

    def get_input_file_path_for_variable_name(self, variable_name):
        filename = self.__get_filename_from_variable_name(variable_name, ".csv")
        return "{}/{}".format(self.path_to_save_results, filename)

    def get_variable_data(self):
        with open("Data.yaml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data
