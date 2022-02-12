"""
At some point, I should probably refactor this into a set of helper functions
to help convert Pandas to LaTeX tables.


"""
import config
import pandas as pd
import numpy as np

df = pd.DataFrame({'categorical': pd.Categorical(['d','e','f']),
                   'xvar': [1, 2, 3],
                   'yvar': np.sin([1, 2, 3]),
                   'zvar': np.cos([1,2,3]),
                   'object': ['a', 'b', 'c']
                  })
df.describe()

columns_for_summary_stats = [
    'xvar',
    'yvar',
    ]

# This maps the column names to their LaTeX descriptions
column_names_map = {
    'xvar':'Longitude',
    'yvar':'Lattitude',
}

escape_coverter = {
    '25%':'25\\%',
    '50%':'50\\%',
    '75%':'75\\%'
}

df = df[columns_for_summary_stats]

# Suppress scientific notation and limit to 3 decimal places
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# Pooled summary stats
describe = (
    df[columns_for_summary_stats].
    describe().T.
    rename(index=column_names_map, columns=escape_coverter)
)
describe['count'] = describe['count'].astype(int)
describe.columns.name = 'Subsample A'
latex_table_string = describe.to_latex(escape=False)

describe.columns.name = 'Subsample B'
latex_table_string2 = describe.to_latex(escape=False)

latex_table_string_split = [
    *latex_table_string.split('\n')[0:-3],
    '\\midrule',
    *latex_table_string2.split('\n')[2:]
]
latex_table_string = '\n'.join(latex_table_string_split)
# print(latex_table_string)
path = config.output_dir / f'example_table.tex'
with open(path, "w") as text_file:
    text_file.write(latex_table_string)
