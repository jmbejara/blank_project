| Pipeline Name                   | {{pipeline_specs.pipeline_name}}                       |
|---------------------------------|--------------------------------------------------------|
| Pipeline ID                     | [{{pipeline_id}}]({{pipeline_page_link}})              |
| Lead Pipeline Developer         | {{pipeline_specs.lead_pipeline_developer}}             |
| Contributors                    | {{pipeline_specs.contributors | join(', ')}}           |
| Bitbucket Repo URL              | {{pipeline_specs.bitbucket_repo_URL}}                  |
| Production Directory            | {{pipeline_specs.pipeline_prod_directory}}             |
| Development Directory           | {{pipeline_specs.pipeline_dev_directory}}              |
| Date of Last Code Update        | {{pipeline_specs.source_last_modified_date}}           |
| Runs on Unix/Linux, Windows, or Other? |{{pipeline_specs.runs_on_grid_or_windows_or_other}}|

In addition to the `requirements.txt` and `r_requirements.txt`, the pipeline code relies
on first loading modules using the following command:
```
{{pipeline_specs.software_modules_command}}
```