# MLX UI (w/ React)

## React Design Principles
The key feature of React is composition of components. React works by having pages use components to add functionality which themselves use components to add functionality.

![LandingPage](/docs/images/LandingPage.png)

Image 1: The Landing Page divided into some of its components.

![MLX UI Diagram](/docs/images/mlx-ui-diagram.png)

Image 2: MLX UI structure


React Props vs. State:

A components props and state are variables which dictate the changeable content of a component. For example, take a parent component that is a webpage and take a child component which represents a Button. The parent could ask for two Buttons with the text="Press" on one and text="Click" on the other. "Press" and "Click" would be the value of the variable props.text and should not be changed inside of the Button component. The state of these Buttons could be something like "clickNum" which defines how many times the button has been clicked. 
Props - Parameters passed from the parent component. Props should not be changed inside the child component. If a prop is changed in a parent component then the child component will be recreated.
State - Variables that dictate the current condition of the component. State can be changed inside the component. If a state variable is changed in a component then the component will be recreated.


Lifecycle Methods:

Each component has several “lifecycle methods” that you can override to run code at particular times in the process. Putting functions in different lifecycle methods will cause the function to be run at a specific point in a component's lifecycle. An example of this is running a function after a component is being unmounted (removed or refreshed).

## Startup

General Startup Instructions: https://github.com/machine-learning-exchange/mlx/tree/main/dashboard/origin-mlx

### Starting the MLX UI locally

To run this app, you'll need a current version of Node.js installed.

1. First, clone this repo:
```Bash
git clone https://github.com/machine-learning-exchange/mlx.git
```

2. Next, install the dependencies by running this command from within the newly created directory:
```Bash
npm install
```

3. Start the app with the following command:
```Bash
npm start
```

4. The app should now be accessible in your web browser at:
```
http://localhost:3000
```

### Starting the MLX UI locally with Docker API
```
git clone https://github.com/machine-learning-exchange/mlx.git
cd mlx/
cd dashboard/origin-mlx/
rm -rf package-lock.json 
npm install
export REACT_APP_API="localhost:8080"
export REACT_APP_RUN="false"
export REACT_APP_UPLOAD="true"
export REACT_APP_DISABLE_LOGIN="true"
npm start
```

### Building an MLX UI Image

```
cd dashboard/origin-mlx
docker build -t <your docker user-id>/<repo name>:<tag name> -f Dockerfile .
docker push <your docker user-id>/<repo name>:<tag name>
```

### Change the UI image on a cluster deployment
Change the image in /manifests/base/mlx-deployments/mlx-ui.yaml under the container with the name mlx-ui at spec.template.spec.containers
```
kubectl delete -f /manifests/base/mlx-deployments/mlx-ui.yaml
kubectl apply -f /manifests/base/mlx-deployments/mlx-ui.yaml
```

## UI File Structure
 
The folders which contain the pieces of the MLX UI:

![LandingPage](/docs/images/ui-folder-tree.png)



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
