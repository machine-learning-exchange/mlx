# Import Data and AI Assets

## Import a Catalog of Assets

To _import a catalog of assets_ you must be logged in as an `admin`. To log in, append `/login` to the
MLX URL in your browser's address bar:

    http://<cluster_node_ip>/login

Then expand the :gear: **Settings** at the bottom of the left-hand side navigation bar, and click on
**MLX Settings**. At the top of the center screen, click on the **Choose Catalog** button under
the **Bulk Imports** sections. 

Find and select the [JSON file](/bootstrapper/catalog_upload.json) that describes your catalog 
and the import should begin. A progress bar will indicate the upload progress.

If an asset from your Catalog did not get imported, make sure that all the metadata provided in the
Catalog upload file is correct (API Key, Asset URL, etc.). If it is correct, ensure that the 
asset you are trying to import does not share a name/ID with another asset.

![Catalog Import Screenshot](/docs/images/CatalogImport.png)


## Register Assets Individually

Once you are loggen in as `admin` user you can also register assets one at a time.
Navigate to the desired asset category using the left-hand navigation menu. If a
catalog of assets was already imported you should see a grid of _"featured"_ assets
otherwise the center frame of the MLX UI will appear blank.
Click on the **"Register ..."** button in the top banner of the MLX UI. In the 
registration dialog you can either upload a local *.yaml file or provide the URL
to the YAML file on GitHub. The YAML file must contain the required metadata
based on the type of asset as described here:
- [Datasets](/datasets/README.md)
- [Models](/models/README.md)
- [Notebooks](/notebooks/README.md)
- [Pipelines](/pipelines/README.md)
- [Pipeline Components](/components/README.md)

The name should be in title case without periods (`.`), dashes (`-`), or underscores (`_`).
If you don't provide a name in the dialog, the `name` in the asset YAML file will
be used. Finally, click "Upload".

## Uploading Assets from Enterprise GitHub or Private GitHub Repositories

In order to enable uploading assets from Enterprise GitHub (usually behind a 
corporate firewall) or from a private GitHub repository, the MLX API server can
be configured with a "read-only" GitHub API access token. Similarly, the MLX UI
server can be configured with a "read-only" GitHub API access token to enable
the MLX UI to display Markdown files (`README.md`) from Enterprise GitHub or from
a private GitHub repository. You can find more details in the
[MLX Setup Instructions](mlx-setup.md#configuring-access-to-private-github-repositories-or-github-enterprise).
