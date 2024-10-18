---
date: {{pipeline_specs.source_last_modified_date}}
tags: {{dataframe_specs.data_sources | join(', ')}}
category: {{topic_tags | join(', ')}}
---

# Chart: {{chart_name}}
{{short_description_chart}}

```{raw} html
<iframe src="../_static/{{pipeline_id}}_{{chart_id}}.html" height="500px" width="100%"></iframe>
```
[Full Screen Chart](../download_chart/{{pipeline_id}}_{{chart_id}}.html)
