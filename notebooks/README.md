# Notebooks

The Jupyter notebook is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text. A Jupyter notebook should have a self-contained set of code that can be executed using the Jupyter notebook server runtime.

## Create Notebooks
The Jupyter notebooks on MLX should be a self-contained set of code that can be executed on a vanilla Python 3.6 runtime. Then, the notebooks need to be uploaded to GitHub repository.

To register the notebook, we need to create a specification file in YAML format. The file includes information for MLX to view and run the notebook, such as GitHub source and metadata specifications. The [template](template.yaml) has all the details on how to create a notebook specification file.

## Register Notebooks
1. Click on the "Notebooks" link in left hand navigation panel
2. Click on "Upload a Notebook"
3. Select a file to upload (Must be tar.gz or tgz format)
    - This will be the compressed .yaml notebook specification
4. Enter a name for the notebook; Otherwise a default will be given

## How to use Notebooks to Drive Pipelines
// TODO

## How to use Notebooks Within a Pipeline Step
// TODO

## Sample Notebooks

You can find the sample notebooks in the Machine Learning Exchange catalog
[here](https://github.com/machine-learning-exchange/katalog/tree/main/notebook-samples)
