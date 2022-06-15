# base image
FROM node:16-slim

# create app directory
RUN mkdir -p /workspace

# set working directory
WORKDIR /workspace

# envrionment variables
ENV PORT=3000

# install and cache app dependencies
COPY . /workspace

RUN npm install --silent --only=prod

# install and build UI backend
RUN cd server && npm install && npm run build

# make sure non-root user can modify workspace folder
#RUN chgrp -R 0 /workspace && chmod -R g=u /workspace
RUN chown -R node /workspace

# change user
USER node

# mark as production build
ENV NODE_ENV=production

# run build on container startup in order to build in environment variables
#  - https://create-react-app.dev/docs/adding-custom-environment-variables/
# TODO: find a better solution, i.e.
#  - https://www.tutorialworks.com/openshift-deploy-react-app/
#  - https://javaadpatel.com/building-and-deploying-react-containers/
CMD ["sh", "-c", "npm run build && node server/dist/server.js build/ $PORT"]


