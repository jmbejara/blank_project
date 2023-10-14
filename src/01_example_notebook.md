---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.7
---

# Example Notebook

This notebook is designed demonstrate a number of goals:

  - The notebook is part of the automated analytical pipeline, as it is run programmatically by the build system, as in the dodo.py file.
  - It is tracked by version control via Git. To avoid large files and the problems associated with non-text files, the notebook is stripped of its output. 
  - In order to avoid re-running the notebook every time it changes (it changes often, even by the act of opening it) and to only rerun it if meaningful changes have been made, the build system only looks for changes in the plaintext version of the notebook. That is, the notebook is converted to markdown via [JupyText](https://github.com/mwouts/jupytext). Then, DoIt looks for changes to the markdown version. If it detects a difference, then the notebook is re-run.
  - Since we want to use Jupyter Notebooks for exploratory reports, we want to keep fully-computed versions of the notebook (with the output intact). However, earlier I said that I strip the notebook of its output before committing to version control. Well, to keep the output, every time PyDoit runs the notebook, it outputs an HTML version of the freshly run notebook and saves that HTML report in the `output` directory. That way, you will be able to view the finished report at any time without having to open Jupyter.

```python
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv("../relative.env")

OUTPUT_DIR = os.getenv('OUTPUT_DIR')
```

```python
import numpy as np
from matplotlib import pyplot as plt
```

```python
x = np.linspace(0, 8 * np.pi, 1000)
y = np.sin(x)
plt.plot(x, y)
filepath = Path(OUTPUT_DIR) / 'sine_graph.png'
plt.savefig(filepath)
```

```python

```
