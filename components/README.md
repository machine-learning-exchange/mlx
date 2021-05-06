# Components

> A pipeline component is a self-contained set of code that performs one step in the ML workflow (pipeline), such as data preprocessing, data transformation, model training, and so on. A component is analogous to a function, in that it has a name, parameters, return values, and a body.

## Create a Component
Components are made up of two sets of code. Client code talks to api endpoints for submitting the job. Runtime code does the actual job specified for the component.

Components must also include a specification file in YAML format. The file includes information for Kubeflow to run the component, such as metadata and input/output specifications.

The last step is to dockerize the component code.

For an in-depth guide, take a look at their [component specification](https://www.kubeflow.org/docs/pipelines/reference/component-spec/).

## Register Pipeline Components
1. Click on the "Components" link in left hand navigation panel
2. Click on "Upload a Component"
3. Select a file to upload (Must be tar.gz or tgz format)
    * This will be the compressed .yaml component specification
4. Enter a name for the component; Otherwise a default will be given

## Use Components in a Pipeline
Components are composed into a pipeline using the Kubeflow Pipelines SDK. Refer to the pipeline 
[documentation](../pipelines/README.md) for usage.

## Sample Components
You can find the sample components in the Machine Learning Exchange catalog
[here](https://github.com/machine-learning-exchange/katalog/tree/main/component-samples)
