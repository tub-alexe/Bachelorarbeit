


import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/

sector = ["PW < 100°C", "PW 100-500°C","PW 500-1000°C","PW > 1000°C"]

Ernährung = np.array([34, 41.8, 0, 0])
Papier = np.array([10.8, 39.8, 0, 0])
Chemie = np.array([55.5, 86.3, 184.3, 45.4])
Glas = np.array([4.6, 7.1, 106.4, 220.3])
Metall = np.array([3.3, 10.4, 122.5, 480.5])

width = 0.5

plt.rc('font', **{'size': 20})
plt.rcParams["figure.figsize"] = (20, 12)

plt.bar(sector, Ernährung, width, color='firebrick', label='Ernährungsgewerbe')
plt.bar(sector, Papier, width, bottom=Ernährung, color='orange', label='Papiergewerbe')
plt.bar(sector, Chemie, width, bottom=Ernährung+Papier, color='khaki', label='Chemische Industrie')
plt.bar(sector, Glas, width, bottom=Ernährung+Papier+Chemie, color='palegreen', label='Glasgewerbe, Keramik, Verarbeitung von Steinen und Erden')
plt.bar(sector, Metall, width, bottom=Ernährung+Papier+Chemie+Glas, color='forestgreen', label='Metallerzeugung und -bearbeitung')

plt.legend(loc="upper left")
plt.ylabel('Prozesswärmebedarf [PJ/a]')
plt.savefig('Prozesswärme Grafik.svg')
plt.show()
