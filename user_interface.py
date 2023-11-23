import csv
import matplotlib.pyplot as plt


def plot_power_output(results): #TODO make more generic so we could plot things like angles vs time etc
    fig, ax = plt.subplots()
    dates = [entry['date'] for entry in results]
    power = [entry['power'] for entry in results]
    ax.plot(dates, power)
    plt.show()


def write_to_csv(results):
    header = ['date', 'power']
    with open('results.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)
