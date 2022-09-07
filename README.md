# How use this project

1. Clone into your computer (or gitpod).
2. Add your transformations into the `./transformations/<pipeline>/` folder.
3. Configure the project.yml to specify the piplines and transformations in the order you want to execute them.
4. Add new transofrmation files as you need them, make sure to include `expected_input` and `expected_output` as examples.
5. Update your project.yml file as needed to change the order of the transformations.

# Validate and run:

- Validate your transformations running `$ pipenv run validate`.
- 
- Run your pipline by running `$ pipenv run <pipeline_slug> <dataset_name>`: It will generate a ew csv file inside `./output` directory.

