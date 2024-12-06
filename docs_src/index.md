# {{pipeline_specs.pipeline_name}}

Last updated: {sub-ref}`today` 


## Table of Contents

```{toctree}
:maxdepth: 1
:caption: Notebooks 📖
notebooks/01_example_notebook_interactive.ipynb
notebooks/02_example_with_dependencies.ipynb
notebooks/03_public_repo_summary_charts.ipynb
```

```{toctree}
:maxdepth: 1
:caption: Pipeline Charts 📈
charts.md
```

```{toctree}
:maxdepth: 1
:caption: Pipeline Dataframes 📊
{{dataframe_file_list | sort | join("\n")}}
```


```{toctree}
:maxdepth: 1
:caption: Appendix 💡
myst_markdown_demos.md
notebooks.md
apidocs/index
```


## Pipeline Specs
{% for pipeline_id, pipeline_specs in specs.items() %}
  {% include "docs_src/_templates/pipeline_specs.md" with context %}
{% endfor %}


## Module Documentation

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`

{{readme_text}}