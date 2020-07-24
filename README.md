## About
This application creates a set of graphs based on the scenario data available at [IAMC 1.5°C Scenario Explorer hosted by IIASA](https://data.ene.iiasa.ac.at/iamc-1.5c-explorer/#/login?redirect=/workspaces)

## How to run the code
From the terminal/command line, navigate to the directory containing the `main.py` file and run the command `python main.py`

Ensure your environment has the dependencies specified at the `requirements.txt` file installed.

## How it works
The `input_file.csv` contains the raw data necessary for generating graphs. While the `Data.yaml` specifies the graphs attributes; e.g., x-axis values, y-axis values, title, legend, etc.

For proper functionality of the application, ensure these two files are located under the same directory as the `main.py` file.

For further details about about the `input_file.csv` please view the section [Input CSV File in Details](#input-csv-file-in-details).

For further details about about the `Data.yaml` please view the section [Data File in Details](#data-file-in-details).

## Input CSV File in Details
Coming soon 

## Data File in Details
Coming soon

## Screenshots
Below are some examples of the graphs this application can generate.

![CO2 Intensity](/screenshots/co2_intensity.png)

![Carbon Sequestration|CCS](/screenshots/carbon_seq_ccs.png)

![Emissions CO2](/screenshots/emissions_co2.png)

![Final Energy](/screenshots/final_energy.png)
