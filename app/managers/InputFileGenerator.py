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

    def __drop_unwanted_years(self, df, wanted_start_year, wanted_end_year):
        list_of_columns_to_erase = []

        # Determine the column names (years) to erase
        for column_name in list(df):
            if column_name.isnumeric() and int(column_name) not in list(
                range(wanted_start_year, wanted_end_year + 1)
            ):
                list_of_columns_to_erase.append(column_name)

        # Erase the unwanted column names (years)
        df.drop(columns=list_of_columns_to_erase, inplace=True)

    def get_dataframe_from_single_variable(self, variable):
        variable_name = variable["variable_name"]
        start_year = variable["start_year"]
        end_year = variable["end_year"]

        df = pd.read_csv(self.path_to_file)
        final = df[df["Variable"] == variable_name]

        self.__fill_in_missing_values(final)
        self.__drop_unwanted_years(final, start_year, end_year)
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
        start_year = variable["start_year"]
        end_year = variable["end_year"]

        df = pd.read_csv(self.path_to_file)
        final = df[
            (df["Variable"] == variable["numerator"])
            | (df["Variable"] == variable["denominator"])
        ]

        self.__fill_in_missing_values(final)
        self.__drop_unwanted_years(final, start_year, end_year)
        return self.__perform_multi_variable_calculation(final, variable)

    def __get_dict_to_store_cumulative_data(self, df):

        # Dictionary to hold all the cumulative information
        cumulative_results = {}

        # Add the columns names that the df has
        for column_name in list(df):
            cumulative_results[column_name] = []

        return cumulative_results

    def __get_dataframe_from_dictionary(self, dictionary):
        return pd.DataFrame(dictionary)

    def _perform_cumulative_analysis(self, df):
        # Get the dictionary where all cumulative data will be stored
        cumulative_result = self.__get_dict_to_store_cumulative_data(df)

        # Create a list with only columns with numeric value
        list_of_column_with_year_values = [i for i in list(df) if i.isnumeric()]

        # Loop over each row and generate the cumulative data
        for index_of_current_row, row in df.iterrows():
            cumulative_result["Model"].append(row["Model"])
            cumulative_result["Scenario"].append(row["Scenario"])
            cumulative_result["Scenario Group"].append(row["Scenario Group"])
            cumulative_result["Region"].append(row["Region"])
            cumulative_result["Variable"].append(row["Variable"])
            cumulative_result["Unit"].append(row["Unit"])

            # Calculate the cumulative amount for each year
            for index_of_current_year, current_year in enumerate(
                list_of_column_with_year_values
            ):

                # Gather info necessary to calculate cumulative
                original_amount_of_current_year = row[current_year]

                # If the current year is the first one of the list, cumulative is the same as the regular amount
                if index_of_current_year == 0:
                    cumulative_result[current_year].append(
                        original_amount_of_current_year
                    )
                    continue

                # Gather more necessary info
                previous_year = list_of_column_with_year_values[
                    index_of_current_year - 1
                ]
                cumulative_amount_of_prev_year = cumulative_result[previous_year][-1]
                original_amount_of_prev_year = df.at[
                    index_of_current_row, previous_year
                ]

                # Perform the calculation
                cumulative_of_current_year = (
                    cumulative_amount_of_prev_year
                    + original_amount_of_current_year
                    + (
                        (
                            (
                                original_amount_of_prev_year
                                + original_amount_of_current_year
                            )
                            / 2
                        )
                        * 4
                    )
                )

                # Save the cumulative of the current year
                cumulative_result[current_year].append(cumulative_of_current_year)

        # Generate a dataframe from the dictionary with the data
        df_cumulative = self.__get_dataframe_from_dictionary(cumulative_result)

        # Asset the new dataframe has the same dimensions as the original dataframe
        assert len(df) == len(df_cumulative)

        return df_cumulative

    def get_dataframe_for_cummulative_single_variable(self, variable):

        # Get a dataframe with the single variable data
        df = self.get_dataframe_from_single_variable(variable)

        # Perform cumulative operation
        return self._perform_cumulative_analysis(df)
