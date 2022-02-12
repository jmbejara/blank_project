import config
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

sns.set()
a = np.array([1,2,3])
plt.plot(a)

filename = config.output_dir / 'example_plot.png'
plt.savefig(filename);
