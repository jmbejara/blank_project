from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv("../.env")

OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR'))

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

sns.set()
a = np.array([1,2,3])
plt.plot(a)

filename = OUTPUT_DIR / 'example_plot.png'
plt.savefig(filename);
