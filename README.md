# What is Dataflow

Its a very simple minimalistic project to clean and deploy datasets in real time using python. Its ideal for small and mid-sized comapnies that want to deploy into production a solution with very few steps and cheap costs.

Deploy in heroku in minutes, create pipelines of data with multiple python functions to clean your dataset and save it into CSV, SQL or BigQuery.

<p align="center">
    <img src="https://user-images.githubusercontent.com/426452/202270773-8569adeb-7909-4498-b9f5-185242e5680c.png" width="500" />
</p>

# How use this project

1. Clone into your computer (or gitpod).
2. Add your transformations into the `./transformations/<pipeline>/` folder.
3. Configure the project.yml to specify the pipline and transformations in the order you want to execute them. Each pipeline must have at least one source and only one destination. You can have multiple sources if needed.
4. Add new transformation files as you need them, make sure to include `expected_inputs` and `expected_output` as examples. The expected inputs can be an array of dataframes for multiple sources.
5. Update your project.yml file as needed to change the order of the transformations.
6. Validate your transformations running `$ pipenv run validate`.
7. Run your pipline by running `$ pipenv run pipeline --name=<pipeline_slug>`
8. If you need to clean your outputs :`$ pipenv run clear`

## Sources

Dataflow can retrieve or store datasets of information from and into CSV files, SQL Databases and Google BigQuery.

## Pipelines

A pipeline is all the steps needed to clean an incoming source dataset and save it into another dataset.

- One pipeline is comprised with one or many data **transformations**.
- One pipeline has one or more sources of information (in batch or streaming).
- One piepline has one destination dataset.

## Transformations

```py
import pandas as pd
import numpy as np

def run(df):
    # ...
    return df
```


## Streaming data into pipelines

Pipelines also allow streaming chunks of data (one at a time). You can define a csv file that contains a list of each stream as it will come into the pipeline (one at a time). For example:

```
pipenv run pipeline --name=clean_publicsupport_fs_messages --stream=stream_sample.csv
```

Note: `--stream` is the path to a csv file that contains all the streams you want to test, if the CSV contains multiple rows, each of them will be considered a separate stream and the pipeline will run once for each stream.

Dataflow will run each pipeline as many times as streams are found inside the `stream_sample.csv` file.

### Declaring the stream parameter in the transformation

Make sure to specify the stream optional paramter in the transformation function:

```py
import pandas as pd
import numpy as np

def run(df, stream=None):
    # ...
    return df
```
