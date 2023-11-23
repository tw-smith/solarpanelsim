import csv
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_file_name(orbit, extension):
    filename = (f"a{orbit.getA()}_"
                  f"e{round(orbit.getE(), 4)}_"
                  f"i{math.degrees(orbit.getI())}_"
                  f"RAAN{math.degrees(orbit.getRightAscensionOfAscendingNode())}_"
                  f"omega{math.degrees(orbit.getPerigeeArgument())}")
    filename = filename.replace('.', 'p')
    return filename + extension

def plot_power_output(results, orbit): #TODO make more generic so we could plot things like angles vs time etc
    #TODO DRY with generate file name function
    plot_title = (f"a: {orbit.getA()} "
                  f"e: {round(orbit.getE(), 4)} "
                  f"i: {math.degrees(orbit.getI())} "
                  f"RAAN: {math.degrees(orbit.getRightAscensionOfAscendingNode())} "
                  f"omega: {math.degrees(orbit.getPerigeeArgument())}")
    filename = generate_file_name(orbit, '.png')
    fig, ax = plt.subplots()
    dates = [entry['date'] for entry in results]
    power = [entry['power'] for entry in results]
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
    fig.savefig(f"./plot_results/{filename}", transparent=False, dpi=80)


def write_to_csv(results, orbit):
    csv_title = generate_file_name(orbit, '.csv_results')
    header = ['date', 'power']
    with open(f"csv_results/{csv_title}", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)
