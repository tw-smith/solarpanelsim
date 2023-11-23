import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_power_output(results): #TODO make more generic so we could plot things like angles vs time etc
    fig, ax = plt.subplots()
    dates = [entry['date'] for entry in results]
    power = [entry['power'] for entry in results]
    locater = mdates.AutoDateLocator(minticks=3, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locater)
    ax.xaxis.set_major_locator(locater)
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(dates, power)
    ax.set_xlabel('Date (UTC)')
    ax.set_ylabel('Panel power output (W)')
    for label in ax.get_xticklabels():
        label.set_rotation(90)
    plt.tight_layout()
    plt.show()
    # TODO add plot title with orbital parameters etc?
    # TODO save in folder


def write_to_csv(results):
    header = ['date', 'power']
    with open('results.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)
    # TODO add orbital params to title of csv
    # TODO save in subfolder
