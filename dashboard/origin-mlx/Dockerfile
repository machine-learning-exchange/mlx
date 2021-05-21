# base image
FROM node:14

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

# start app
ENV NODE_ENV=production
CMD ["sh", "-c", "npm run build && mv build/ proc/ && node server/dist/server.js proc/ $PORT"]
