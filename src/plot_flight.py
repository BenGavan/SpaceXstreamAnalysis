import numpy as np
import matplotlib.pyplot as plt


def plot_flight():
    print('plotting flight')

    datafilepath = '../data/data.csv'
    outplotpath = '../plt/plot.png'
    data = np.genfromtxt(datafilepath, delimiter=',', skip_header=1)

    times = data[:, 0]
    booster_speed = data[:, 1]
    booster_altitude = data[:, 2]
    ship_speed = data[:, 3]
    ship_altitude = data[:, 4]

    nrows = 1
    ncols = 2
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*5, nrows*3))

    ax01 = ax[0].twinx()
    ax[0].scatter(times, booster_speed, s=1, c='cornflowerblue')
    ax01.scatter(times, booster_altitude, s=1, c='orange')
    ax[0].set_title('Booster')
    ax[0].set_xlabel('time (s)')
    ax[0].set_ylabel('speed (km/s)')
    ax01.set_ylabel('altitude (km)')

    ax11 = ax[1].twinx()
    ax[1].scatter(times, ship_speed, s=1, c='cornflowerblue')
    ax11.scatter(times, ship_altitude, s=1, c='orange')
    ax[1].set_title('Ship')
    ax[1].set_xlabel('time (s)')
    ax[1].set_ylabel('speed (km/s)')
    ax11.set_ylabel('altitude (km)')

    fig.tight_layout()
    fig.savefig(outplotpath, dpi=500)
    plt.close(fig)


if __name__ == '__main__':
    plot_flight()