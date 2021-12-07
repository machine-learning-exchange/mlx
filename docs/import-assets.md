# Import Data and AI Assets in MLX Catalog

To _import a catalog of assets_ you must be logged in as an `admin`. To log in, append `/login` to the
MLX URL in your browser's address bar:

    http://mlx-ui-url/login

Then expand the :gear: **Settings** at the bottom of the left-hand side navigation bar, and click on
**MLX Settings**. At the top of the center screen, click on the **Choose Catalog** button under
the **Bulk Imports** sections. 

Find and select the [JSON file](/bootstrapper/catalog_upload.json) that describes your catalog 
and the import should begin. A progress bar will indicate the upload progress.

If an asset from your Catalog did not get imported, make sure that all the metadata provided in the
Catalog upload file is correct (API Key, Asset URL, etc.). If it is correct, ensure that the 
asset you are trying to import does not share a name/ID with another asset.

![Catalog Import Screenshot](/docs/images/CatalogImport.png)
