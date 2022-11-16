# What is Dataflow

<img align="right" src="https://user-images.githubusercontent.com/426452/202270773-8569adeb-7909-4498-b9f5-185242e5680c.png" width="500" />

It's a very simple minimalistic project to clean and deploy datasets in real time using python. Its ideal for small and mid-sized organizations that want to deploy into production a data-processing solution with very few steps and cheap costs. It supports **batch** and **streaming** processing.

Deploy in heroku in minutes, create pipelines of data with multiple python functions to clean your dataset and save it into CSV, SQL or BigQuery.

# Quick Start:

1. Clone this repo into your computer (or open it on gitpod).
2. Create a new folder inside `./pipelines` with the name of your pipeline.
3. Add your transformations into the recently created folder `./pipelines/<pipeline_name>/`.
4. Configure the project.yml to specify the pipline and transformations in the order you want to execute them. Each pipeline must have at least one source and only one destination. You can have multiple sources if needed.
5. Add new transformation files as you need them, make sure to include `expected_inputs` and `expected_output` as examples. The expected inputs can be an array of dataframes for multiple sources.
6. Update your project.yml file as needed to change the order of the transformations.
7. Validate your transformations running `$ pipenv run validate`.
8. Run your pipline by running `$ pipenv run pipeline --name=<pipeline_slug>`
9. If you need to clean your outputs :`$ pipenv run clear`

## Project.yml

All the project configuration is done in one single file, here is an example with comments:

```yml
name: "Lead Collection"
# You can have as many pipelines as you want
pipelines:
    # Unique name for your pipeline
  - slug: "clean_form_entries"
    # During local development these are CSV files located at te ./sources folder.
    sources:
      # The order is relevant, this sources will be passed as parameters to the run() function in the same order
      - form_entries
      - salutations
    # Ignored during local development, its the datasource to wich the pipeline data will be saved to
    destination: datasource_csv
    # Order is relevant, they will execute one on top of the other.
    transformations:
      - build_hello_world
      - add_salutation
```

## Sources

Dataflow can retrieve or store datasets of information from and into CSV files, SQL Databases and Google BigQuery.

## Pipelines

A pipeline is all the steps needed to clean an incoming source dataset and save it into another dataset.

- One pipeline is comprised with one or many data **transformations**.
- One pipeline has one or more sources of information (in batch or streaming).
- One piepline has one destination dataset.

## Transformations

Each transformation receives one or many dataframes and must return the cleaned version that will be passed into the next transformation or will become the pipeline output (if it was the last transformation in the pipeline).

```py
import pandas as pd
import numpy as np

def run(df, df2, df3...):
    # make some transformations here
    return df
```

## Unit testing your pipeline

The command to run your tests is `pipenv run validate`.  
Each transformation must have two variables: `expected_inputs` and `expected_output`.  

For example, let's say we want to create a transformation that receives a Pandas dataset with two columns (first_name and last_name) and creates a new column called `together` with the combination of the values in the other two. Here is the input and output to properly validate the transformation:

```py
expected_inputs = [[{
    'first_name': 'Hello',
    'last_name': 'World',
}], []]

expected_output = [{
    **expected_inputs[0][0],
    'together': 'Hello World',
}]


def run(df, df2):
    """
    It will create a full name property on the payload
    """
    df['together'] = df['first_name'] + ' ' + df['last_name']

    return df
```

When you run the `pipenv run validate` command, Dataflow will run the transformation function while passing it the specified inputs, then, it perform a deep comparison between the returned dataframe and the expected_output. If both contain similar values the validation will succeed.

## Running your pipeline

Once the pipeline transformations have been validated its time to test run your pipeline as a whole, while working offline dataflow will use the `./sources` folder to simulate the DataSources as CSV files. That means that for this example we must have two CSV files: `./sources/form_entries.csv` and `./sources/salutations.csv`.

When you run the `pipenv run pipeline --name=clean_form_entries` command, dataflow will fetch those two CSV files and pass them as dataframe parameters to the pipeline transformations. 

> Important note: The first dataframe on every transformation should be your cleaning target because it gets passed on from transformation to transformation as a buffer, ideally this first dataframe will become the output of your entire pipeline.

## Streaming data into pipelines

Pipelines also allow streaming chunks of data (one at a time). You can define a csv file that contains a list of each stream as it will come into the pipeline (one at a time). For example:

```
pipenv run pipeline --name=clean_publicsupport_fs_messages --stream=stream_sample.csv
```

Note: `--stream` is the path to a csv file that contains all the streams you want to test, if the CSV contains multiple rows, each of them will be considered a separate stream and the pipeline will run once for each stream.

Dataflow will run each pipeline as many times as streams are found inside the `stream_sample.csv` file.

### Declaring the stream parameter in the transformation

Make sure to specify one last optional paramter called `stream` in the transformation function, the incoming stream of data will be a dictionary with the exact payload received in the HTTP post request.

```py
import pandas as pd
import numpy as np

def run(df, df2, stream=None):
    # ...
    return df
```
