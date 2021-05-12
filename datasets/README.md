# Datasets

MLX datasets are reusable datasets that leverage [Datashim](https://github.com/datashim-io/datashim)
for providing data volume to all the other MLX assets.

The dataset definition is based on the [DAX metadata](https://github.com/CODAIT/exchange-metadata-converter)
and it is still evolving with the latest Datashim requirements.
You can visit [exchange-metadata-converter](https://github.com/CODAIT/exchange-metadata-converter)
to understand how the DAX metadata is defined and being converted to the Datashim metadata format.

## Create Dataset Metadata

See the [template](#dataset-metadata-template) below to create the metadata for a dataset. Take a look at these
[samples](https://github.com/CODAIT/exchange-metadata-converter/tree/main/dax-data-set-descriptors)
or the original [template](https://github.com/CODAIT/exchange-metadata-converter/blob/main/dax-data-set-descriptors/lorem_ipsum.yaml)
to better understand the dataset metadata spec.

## Register Datasets

1. Click on the "Dataset" link in left-hand navigation panel
2. Click on "Upload a Dataset"
3. Select a file to upload (Must be `.tar.gz` or `.tgz` format)
    * This will be the compressed `.yaml` specification
4. Enter a name for the dataset; Otherwise the `name` from the `.yaml` spec will be used

## Use Dataset with MLX Assets

Asset integration is work in progress. You can take a look at the
[JFK Airport Temperature Prediction Model notebook](https://github.com/machine-learning-exchange/katalog/blob/main/notebook-samples/src/dlf-notebooks/JFK_Data.ipynb)

## Dataset Metadata Template

```yaml
id: lorem-ipsum-data-set            # Unique data set id (required)
name: Lorem ipsum data set          # User friendly data set name (required)
description: Lorem ipsum            # Data set description (required)
version: 1.0                        # Data set version (required, semver format x.y[.z])
created: 2019-07-16                 # Data set creation date (ISO-8601 formatted)
updated: 2020-08-11                 # Last updated date (ISO-8601 formatted)
format:
  - type: CSV                         # Data set file format (user friendly)
    url: https://en.wikipedia.org/wiki/Comma-separated_values
domain: Lorem Ipsum domain          # application domain, e.g. Natural Language Processing

# Information about the entity that makes the data set available
provider:                           # Information about the repository that makes the data set available
  name: Data Asset eXchange         # Repository provider name
  url: https://.../lorem-ipsum/     # Repository provider URL (preferably data set specific)

# identifies where the data set is stored and how it is stored (REQUIRED)
repository:
  type: HTTP
  url: http://.../loremipsum.tar.gz  # Data set archive download URL
  mime_type: application/x-tar       # Data set archive MIME type (https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
  sha_512: cf83e135...7eefb          # SHA-512 checksum of the data set file
  size: 12M                          # Data set archive size including units (E, P, T, G, M, K) (which isn't necessarily the size of the data file)

# REQUIRED; data set license information
license:
  commercial: false                  # if true, a commercial license (assume false if not set)
  name: CDLA-Sharing                 # License name
  url: https://cdla.io/sharing-1-0/  # Link to public license text

# REQUIRED; describes relevant files in the data set archive
content:
  - pattern: path/lorem-ipsum1.csv    # includes path
    description: l-i training data    # free form text describing the file content
    records: 5000                     # including units (E, P, T, G, M, K), if applicable
    size: 1M                          # size including units (E, P, T, G, M, K), if applicable
    format: CSV                       # file format (user friendly)
    type: file                        # "file" | "regex"
    mime_type: text/csv               # File MIME type (https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
    columns:                          # optional; only applies to column-oriented file formats
      - name: column_name             # 1st column name
        description: column_descr     # 1st column description
        type: str                     # 1st column data type (TODO - need to define values for types)
  - pattern: path/lorem-ipsum2.csv    # includes path
    description: l-i test data        # free form text describing the file content
    records: 3000                     # including units (E, P, T, G, M, K), if applicable
    size: 500K                        # size including units (E, P, T, G, M, K), if applicable
    format: CSV                       # file format (user friendly)
    type: file                        # "file" | "regex"
    mime_type: text/csv               # File MIME type (https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)

# OPTIONAL; Identifies where the data set was obtained from
source:
  name: entity-name                   # Name of the owning entity
  url: https://www.entity-name.org/   # Any valid URL for the entity
  email: somebody@entity-name.org
  authors:                            # OPTIONAL; used to give credit to specific individuals
    - name: John Doe                  # Author name
      url: http://lorem.ipsum/john.d  # Arbitrary link for author
      email: jdoe@entity-name.org     # Contact information for author

# OPTIONAL; but recommended
seo_tags:                             # hints for classification and search
  - lorem ipsum tag 1
  - lorem ipsum tag 2

# OPTIONAL; assets that complement this data set, e.g. notebooks
related_assets:
  - name: lorem ipsum                     # User-friendly asset name
    description: asset description        # OPTIONAL; asset description
    mime_type: asset-mime-type            # OPTIONAL (but recommended); example for Jupyter notebook
    url: https://server/path/to/asset     # Asset URL
  # example 1 (Jupyter notebook)
  - name: lorem ipsum notebook            # A Jupyter notebook that
    description: Clean data notebook      # Notebook description
    mime_type: application/x-ipynb+json   # Jupyter notebook
    url: https://.../lorem-ipsum/nb.ipynb # Path to notebook
  # example 2 (Exported Watson Studio project)
  - name: lorem ipsum WS project           #
    description: WS sample project         # Contains notebooks for cleaning and analysis
    mime_type: application/zip             # ZIP file with proprietary structure
    url: https://github.com/.../p.zip      # Path to ZIP file
  # example 3 (Landing page for Watson Studio Gallery project)
  - name: lorem ipsum WSG project          #
    description: WSG sample project        # Contains notebooks for cleaning and analysis
    mime_type: text/html                   # HTML page
    url: https://dataplatform...           # Path to landing page
  # example 4 (Web page containing data samples and glossary)
  - name: Explore the data set             #
    description: Data preview and glossary #
    mime_type: text/html                   # HTML page
    url: https://dax-cdn...                # Path to data preview and glossary pages
```

## Sample Datasets

You can find the sample datasets in the Machine Learning Exchange catalog
[here](https://github.com/machine-learning-exchange/katalog/tree/main/dataset-samples)
