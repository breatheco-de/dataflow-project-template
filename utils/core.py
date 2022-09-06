import os
import sys
import yaml
from importlib import import_module
from deepdiff import DeepDiff


def scan_pipelines(slug=None):
    transformations = []


def load_pipelines_from_project(slug=None):
    queues = []
    project = None
    with open('project.yml', 'r') as file:
        project = yaml.safe_load(file)

    if "pipelines" not in project:
        raise Exception("Project.yml is missing pipelines property")

    if not isinstance(project['pipelines'], list):
        raise Exception("Property 'piplines' on project.yml must be a list")

    if slug is not None:
        for p in project['pipelines']:
            if p['slug'] == slug:
                return [p]
        raise Exception(f"No pipeline with slug {slug} was found")

    return project["pipelines"]


def get_params():
    pipeline = None
    source = None
    try:
        pipeline = sys.argv[1]
        source = sys.argv[2]
    except IndexError:
        pass

    return pipeline, source

def scan_for_pipelines():
    piplines = []
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/../transformations'
    files = os.listdir(dir_path)
    for f in files:
        if os.path.isdir(dir_path+"/"+f): 
            piplines.append(f)

    return piplines

def scan_pipeline_transformations(pipeline_name):
    transformations = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(dir_path + '/../transformations/' + pipeline_name)
    for file_name in files:
        if '.py' not in file_name:
            continue
        if file_name in ['__init__.py']:
            continue
        transformations.append(file_name[0:-3])

    return transformations

def get_transformation(pipeline_name, transformation):
    try:
        mod = import_module('transformations.' +
                            pipeline_name + '.' + transformation)
    except ModuleNotFoundError as e:
        raise Exception(f'Transformation does not exist:' +
                        pipeline_name + '.' + transformation+". Please check that you file names match your project.yml pipeline transformations")
    except ImportError as e:
        raise Exception(f'Error importing transformations.' +
                        pipeline_name + '.' + transformation)
    try:
        expected_input = getattr(mod, 'expected_input')
    except AttributeError:
        raise Exception(
            f'Error importing the the expected_input')

    try:
        expected_output = getattr(mod, 'expected_output')
    except AttributeError:
        raise Exception(
            f'Error importing the expected_output')

    try:
        run = getattr(mod, 'run')
    except AttributeError:
        raise Exception(
            f'Missing the run function')

    return run, expected_input, expected_output


class MockDataset(object):
    def table(entity_name):
        return None


class MockBigQuery(object):
    def dataset():
        return MockDataset()

    def insert_rows_json(**args):
        return []


def delete_folder(folder):
    import os
    import shutil
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
