import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class GraphGenerator:

    def __getNameColorAndLines(self, df, scale):
        all_lines = []
        color_for_lines = []
        name_for_lines = []
        for index, row in df.iterrows():
            line = {}
            for key,value in row.items():
                if key.isnumeric():
                    line[key] = value/scale
            all_lines.append(line)

            if row["Scenario Group"] == "High Overshoot 1.5 C":
                color_for_lines.append("red")
                name_for_lines.append("High Overshoot 1.5 C")
            elif row["Scenario Group"] == "Low Overshoot 1.5 C":
                color_for_lines.append("green")
                name_for_lines.append("Low Overshoot 1.5 C")
            else:
                color_for_lines.append("blue")
                name_for_lines.append("Below 1.5 C")

        assert len(color_for_lines) == len(all_lines)
        assert len(name_for_lines) == len(all_lines)
        
        return name_for_lines,color_for_lines,all_lines

    def __getAverageForEachGroup(self, df, scale):
        group_by_group = df.groupby(df["Scenario Group"])
        averages_per_group = {}

        for group_name, group in group_by_group:
            list_of_years = [value for value in group.columns.values if value.isnumeric()]
            result_average = {}
            for year in list_of_years:
                values_in_year = list(group[year])
                average_for_year = sum(values_in_year)/len(values_in_year)
                result_average[year] = average_for_year/scale
            averages_per_group[group_name] = result_average
            
        return averages_per_group

    def get_figure_for_variable(self, variable, path_to_input_file):
        df = pd.read_csv(path_to_input_file)
        title = variable["graph_title"]
        xaxis_title = variable["x_axis_title"]
        yaxis_title = variable["y_axis_title"]
        scale = variable["scale"]

        # Getting the data necessary for the graph
        name,color,all_lines = self.__getNameColorAndLines(df, scale)
        averages_per_group = self.__getAverageForEachGroup(df, scale)
        
        # Creating and showing the graph
        fig = go.Figure()

        # Plotting all lines
        for index, line in enumerate(all_lines):
            x_axis = list(line.keys())
            y_axis = list(line.values())

            fig.add_trace(go.Scatter(
                            x=x_axis,
                            y=y_axis,
                            mode='lines',
                            line_color= color[index],
                            name = name[index],
                            showlegend=False,
                            opacity=0.10))

        # Plotting the averages
        for group_name in averages_per_group.keys():
            data = averages_per_group[group_name]
            x_axis = list(data.keys())
            y_axis = list(data.values())

            if group_name == "High Overshoot 1.5 C":
                color = "red"
            elif group_name == "Low Overshoot 1.5 C":
                color = "green"
            else:
                color = "blue"

            fig.add_trace(go.Scatter(
                            x=x_axis,
                            y=y_axis,
                            mode='lines',
                            line_color= color,
                            name = group_name,
                            opacity=1))
            
        
        fig.update_layout(xaxis_title = xaxis_title,
                    yaxis_title= yaxis_title,
                    title_text= title,
                    plot_bgcolor= 'rgb(255, 255, 255)',
                    paper_bgcolor = 'rgb(255, 255, 255)')
        
        return fig