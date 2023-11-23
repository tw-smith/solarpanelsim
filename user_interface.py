import matplotlib.pyplot as plt



def plot_power_output(dates, power): #TODO make more generic so we could plot things like angles vs time etc
    fig, ax = plt.subplots()
    ax.plot(dates, power)
    plt.show()
