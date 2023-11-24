import csv
import pathlib
import math
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from errors_and_validation import UserInputValidator


class InputManager:
    def __init__(self, parameter_input):
        self.parameter_input = parameter_input

    def get_parameter_inputs(self):
        # Logic to retrieve a parameter dictionary from either an input.json file or a dictionary passed directly to
        # SolarPanelSim
        if isinstance(self.parameter_input, str):
            with open(self.parameter_input) as f:
                parameter_dict = json.load(f)
        if isinstance(self.parameter_input, dict):
            parameter_dict = self.parameter_input

        # Get validated input parameters from UserInputValidator (which also splits the overall parameter_dict down into
        # its constituent orbit, propagation and panel parameters dictionaries)
        orbit_creation_parameters, propagation_parameters, panel_parameters = UserInputValidator(parameter_dict).validate_input()

        # Convert initial and final datetime objects to Orekit AbsoluteDates
        utc = TimeScalesFactory.getUTC()
        initial_date_orekit = AbsoluteDate(
            propagation_parameters['initial_date'].year,
            propagation_parameters['initial_date'].month,
            propagation_parameters['initial_date'].day,
            propagation_parameters['initial_date'].hour,
            propagation_parameters['initial_date'].minute,
            float(propagation_parameters['initial_date'].second),
            utc
        )
        final_date_orekit = AbsoluteDate(
            propagation_parameters['final_date'].year,
            propagation_parameters['final_date'].month,
            propagation_parameters['final_date'].day,
            propagation_parameters['final_date'].hour,
            propagation_parameters['final_date'].minute,
            float(propagation_parameters['final_date'].second),
            utc
        )
        propagation_parameters['initial_date'] = initial_date_orekit
        propagation_parameters['final_date'] = final_date_orekit

        # Put initial date in orbit creation parameters. It isn't there originally
        # to prevent the user having to repeat the same date twice in the json input
        # but Orekit needs it for the Keplerian orbit.
        orbit_creation_parameters['initial_date'] = propagation_parameters['initial_date']

        return orbit_creation_parameters, propagation_parameters, panel_parameters


class OutputManager:
    def __init__(self, results, orbit):
        self.results = results

        # We need a filename for both csv and plotting outputs so build it here for DRY
        self.filename = (f"a{orbit.getA()}_"
                         f"e{round(orbit.getE(), 3)}_"
                         f"i{math.degrees(orbit.getI())}_"
                         f"RAAN{math.degrees(orbit.getRightAscensionOfAscendingNode())}_"
                         f"omega{math.degrees(orbit.getPerigeeArgument())}")
        self.filename = self.filename.replace('.', 'p')

    def write_to_csv(self):
        header = ['date', 'power']
        pathlib.Path('./csv_results').mkdir(parents=True, exist_ok=True)
        with open(f"csv_results/{self.filename}.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(self.results)

    def plot_power_output(self):
        plot_title = self.filename.replace('p', '.')
        plot_title = plot_title.replace('_', ' ')
        fig, ax = plt.subplots()
        dates = [entry['date'] for entry in self.results]
        power = [entry['power'] for entry in self.results]
        locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(dates, power)
        ax.set_xlabel('Date (UTC)')
        ax.set_ylabel('Panel power output (W)')
        for label in ax.get_xticklabels():
            label.set_rotation(90)
        plt.title(plot_title)
        plt.tight_layout()
        pathlib.Path('./plot_results').mkdir(parents=True, exist_ok=True)
        fig.savefig(f"./plot_results/{self.filename}.png", transparent=False, dpi=80)
        plt.show()

