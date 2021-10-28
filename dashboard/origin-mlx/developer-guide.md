# MLX UI (w/ React)
## UI File Structure
 
The folders which contain the pieces of the MLX UI:

<img width="222" alt="Screen Shot 2021-10-21 at 8 30 21 AM" src="https://user-images.githubusercontent.com/32145094/139307391-2b1c6af8-e977-4e07-aeb3-df4cd1411e6d.png">



- **components/** - Small items which get used inside of pages. For example, the sidebar is used in all the pages, but is not a page itself. The major components are listed below.
  - **Button/**
  - **Detail/** - The Detail folder contains the specific implementations of each asset type for the MetaDetailPage. The ComponentDetail, for example, has a MetadataView, RunView, and two SourceCodeDisplays. The ComponentDetail file represents the content of the MetaDetailPage for the Component assets.
  - **RunView/** - Contains the displays which dictate what parameters the user must fill out when attempting to run any of the assets
  - **Sidebar/**
  - **Tooltip/**


  - There are other components other than those which make up their own folder. Some of the important ones are listed below.
  - Hero - The “Hero Bar” is the bar at the top of the page with mostly navigational items.
  - MarkdownViewer - A display which shows the contents of a markdown file
  - PageFooter - The content that gets displayed at the bottom of every page
  - SecretMenu - The menu which is only available for admins that provides admin’s with extra functionality

- **icons/**
Icons are typically an .svg wrapped in a react component.

- **images/**
.png files used in UI

- **lib/**
lib/ is divided into two folders api/ and stores/
api/ - Contains all the functions which calls to the MLX API.
stores/ - Contains all the functions which add to and view the MLX UI data store 

- **mock/**
Some mock assets for each asset type (no longer in use).

- **pages/**
Each file in pages/ is a page that can be visited in the MLX UI

- **styles/**
Most (>90%) of styling is contained in css files in styles/

## Developing for the MLX UI


MLX UI Starting Points
src/App.tsx controls all the routing inside the react application. If a new route needs to be added it will be added here. If it is not clear what file represents the page at a given url, trace the routes in App.tsx to find the route associated with that url and that route will show the component that is being used.


src/styles/ contains most (>90%) of the page styling in css. If the style needs to be changed first check the component file for styling and if the css is not inline then check in src/styles/.


src/lib/api/ contains all of the calls to the MLX API. If some API call is going wrong, it will likely be an issue in this folder.
