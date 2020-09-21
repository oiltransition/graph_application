import pandas as pd
import os


class InputFileGenerator:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def __fill_in_missing_values(self, df):
        list_of_years_to_calculate_for = sorted(
            [name for name in list(df.columns) if name.isnumeric()]
        )[1:-1]
        for year in list_of_years_to_calculate_for:
            next5 = str(int(year) + 5)
            prev5 = str(int(year) - 5)
            df[str(year)].fillna((df[next5] + df[prev5]) / 2.0, inplace=True)

    def get_dataframe_from_single_variable(self, variable_name):
        df = pd.read_csv(self.path_to_file)
        final = df[df["Variable"] == variable_name]

        self.__fill_in_missing_values(final)
        return final

    def __perform_calculation_on_scenario(self, dfgroup, variable):
        result = {}
        result["Model"] = list(dfgroup["Model"])[0]
        result["Scenario"] = list(dfgroup["Scenario"])[0]
        result["Scenario Group"] = list(dfgroup["Scenario Group"])[0]
        result["Region"] = list(dfgroup["Region"])[0]
        result["Variable"] = variable["variable_name"]
        result["Unit"] = variable["unit"]

        # Getting the list of years
        list_of_years = list(dfgroup._get_numeric_data().columns)

        # list of index in the dataframe
        indeces = list(dfgroup.index)

        # Determining index of numerator and denominator
        denomitanotor_index = 0
        numerator_index = 0
        if dfgroup.loc[indeces[0]]["Variable"] == variable["denominator"]:
            denomitanotor_index = indeces[0]
            numerator_index = indeces[1]
        else:
            denomitanotor_index = indeces[1]
            numerator_index = indeces[0]

        # Looping through each year and performing the calculation
        for year in list_of_years:
            result[year] = (
                dfgroup.loc[numerator_index][year]
                / dfgroup.loc[denomitanotor_index][year]
            )

        # Creating a dataframe from the dictionary
        return pd.DataFrame([result])

    def __perform_multi_variable_calculation(self, localdf, variable):
        # Dataframes to concatenate
        list_of_dataframes = []

        # Group the main dataframe by "Model"
        group_by_model = localdf.groupby(localdf.Model)

        # Loop through each model and perform the calculation
        for model_name, model in group_by_model:
            # print(model_name)
            model_by_scenario = model.groupby(model.Scenario)

            for scenario_name, scenario in model_by_scenario:
                # print(scenario_name)
                if scenario.shape[0] == 2:
                    result = self.__perform_calculation_on_scenario(scenario, variable)
                    list_of_dataframes.append(result)

        return pd.concat(list_of_dataframes)

    def get_dataframe_from_multi_variable(self, variable):
        df = pd.read_csv(self.path_to_file)
        final = df[
            (df["Variable"] == variable["numerator"])
            | (df["Variable"] == variable["denominator"])
        ]
        self.__fill_in_missing_values(final)
        return self.__perform_multi_variable_calculation(final, variable)
