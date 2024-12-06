| Dataframe Name                 | {{dataframe_specs.dataframe_name}}                                                   |
|--------------------------------|--------------------------------------------------------------------------------------|
| Dataframe ID                   | [{{pipeline_id}}_{{dataframe_id}}]({{link_to_dataframe_docs}})                       |
| Data Sources                   | {{dataframe_specs.data_sources | join(', ')}}                                        |
| Data Providers                 | {{dataframe_specs.data_providers | join(', ')}}                                      |
| Links to Providers             | {{dataframe_specs.links_to_data_providers | join(', ')}}                             |
| Topic Tags                     | {{dataframe_specs.topic_tags | join(', ')}}                                          |
| Type of Data Access            | {{dataframe_specs.type_of_data_access}}                                              |
| Data License                   | {{dataframe_specs.data_license}}                                                     |
| License Expiration Date        | {{dataframe_specs.license_expiration_date}}                                          |
| Contact Provider Before Use?   | {{dataframe_specs.need_to_contact_provider}}                                         |
| Provider Contact Information   | {{dataframe_specs.provider_contact_info}}                                            |
| Restrictions on Use of Data    | {{dataframe_specs.restriction_on_use}}                                               |
| How is data pulled?            | {{dataframe_specs.how_is_pulled}}                                                    |
| Data available up to (min)     | {{most_recent_data_min}}                                                             |
| Data available up to (max)     | {{most_recent_data_max}}                                                             |
| Download Data as Parquet       | [Parquet](../download_dataframe/{{pipeline_id}}_{{dataframe_id}}.parquet)            |
| Download Data as Excel         | [Excel](../download_dataframe/{{pipeline_id}}_{{dataframe_id}}.xlsx)                 |
| Linked Charts                  | {% if dataframe_specs.linked_charts %} {% for chart_id in dataframe_specs.linked_charts %} [{{pipeline_id}}_{{chart_id}}](../charts/{{pipeline_id}}_{{chart_id}}.md)<br> {% endfor %} {% else %} None {% endif %} |
