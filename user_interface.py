import csv
import pathlib
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class OutputManager:
    def __init__(self, results, orbit):
        self.results = results
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

    def plot_power_output(self): #TODO make more generic so we could plot things like angles vs time etc
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
        plt.show()
        pathlib.Path('./plot_results').mkdir(parents=True, exist_ok=True)
        fig.savefig(f"./plot_results/{self.filename}.png", transparent=False, dpi=80)
