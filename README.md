# How use this project

1. Clone into your computer (or gitpod).
2. Add your transformations into the `./transformations/<pipeline>/` folder.
3. Configure the project.yml to specify the pipline and transformations in the order you want to execute them. Each pipeline must have at least one source and only one destination. You can have multiple sources if needed.
4. Add new transformation files as you need them, make sure to include `expected_inputs` and `expected_output` as examples. The expected inputs can be an array of dataframes for multiple sources.
5. Update your project.yml file as needed to change the order of the transformations.
6. Validate your transformations running `$ pipenv run validate`.
7. Run your pipline by running `$ pipenv run pipeline --name=<pipeline_slug>`
8. If you need to clean your outputs :`$ pipenv run clear`

## Transformations

```py
import pandas as pd
import numpy as np

def run(df):
    # ...
    return df
```


## Streaming data

Pipelines also allow string chunks of data. For example:

```
pipenv run pipeline --name=clean_publicsupport_fs_messages --stream=stream_sample.csv
```

Note: `--stream` is the path to a csv file that contains all the streams you want to test, if the CSV contains multiple rows, each of them will be considered a separate stream and the pipeline will run once for each stream.

### Fining the stream parameter in the transformation

Make sure to specify the stream optional paramter in the transformation function:

```py
import pandas as pd
import numpy as np

def run(df, stream=None):
    # ...
    return df
```
