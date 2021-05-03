# Notebook Run using Elyra's kfp-notebook package

[kfp-notebook](https://github.com/elyra-ai/kfp-notebook) is an operator that enables running jupyter notebooks on top of kubeflow pipelines. This sample (`kfp-notebook.py`) creates a notebook operator then compiles, uploads, and runs the notebook on kubeflow pipelines (with tekton backend). The notebook operator works by pulling all runtime dependencies from Cloud Object Storage (COS) during pipeline execution and writes all output back to COS upon successful completion of the notebook. Thus, all runtime dependencies, including the notebook to be run, must be stored in COS prior to the pipeline execution. The notebook operator simply stores all the information needed to fetch assets during runtime.

## Requirements
1. Package notebook and related dependencies (e.g. data files used at runtime) into a tar.gz file.
2. Upload `notebook.tar.gz` to an object storage bucket.
3. Host `dataset-requirements.txt` on an external URL (optional).
4. Update the credentials in `kfp_notebook.py`
5. Have Kubeflow 1.2 with Tekton backend running.

## Usage
```shell
# Compress notebook and runtime dependencies
tar -czvf notebook.tar.gz notebook_files

# IF notebook relies on a requirements.txt
# Add the (optional) requirements_url parameter to NotebookOp
notebook_op = NotebookOp(name=op_name,
                         notebook='notebook.ipynb',
                         ..
                         requirements_url="public_url")

# Run the script
python kfp_notebook.py
```

# NotebookOp Parameter Definitions

The notebook pipeline is created using [kfp-notebook](https://github.com/elyra-ai/kfp-notebook), so see their documentation for additional information on the NotebookOp.

**name**: Name of the operation

**notebook**: Name of notebook stored inside the tar.gz file

**cos_endpoint**: COS endpoint to pull the tar.gz file from

**cos_bucket**: COS bucket to pull the tar.gz file from

**cos_directory**: COS path to the tar.gz file (leave empty for no bucket prefix)

**cos_dependencies_archive**: Name of the tar.gz file

**requirements_url** (Optional): Python requirements.txt hosted on a publicly available URL.

**pipeline_outputs**: output files of the pipeline run (not relevant on mlx)

**pipeline_inputs**: input files of the pipelinerun (not relevant on mlx)

**image**: base image to run the notebook