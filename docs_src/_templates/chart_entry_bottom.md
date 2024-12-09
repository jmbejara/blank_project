
| Chart Name             | {{chart_name}}                                             |
|------------------------|------------------------------------------------------------|
| Chart ID               | {{chart_id}}                                               |
| Topic Tags             | {{topic_tags | join(', ')}}                                |
| Data Series Start Date | {{data_series_start_date}}                                 |
| Data Frequency         | {{data_frequency}}                                         |
| Observation Period     | {{observation_period}}                                     |
| Lag in Data Release    | {{lag_in_data_release}}                                    |
| Data Release Date(s)   | {{data_release_dates}}                                     |
| Seasonal Adjustment    | {{seasonal_adjustment}}                                    |
| Units                  | {{units}}                                                  |
| Data Series            | {{data_series}}                                            |
| HTML Chart             | [HTML](../download_chart/{{pipeline_id}}_{{chart_id}}.html)    |

## Data

{% include "docs_src/_templates/dataframe_specs.md" %}

## Pipeline

{% include "docs_src/_templates/pipeline_specs.md" %}
