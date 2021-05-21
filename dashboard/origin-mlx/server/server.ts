// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import * as express from 'express';
import * as ratelimit from 'express-rate-limit'
import * as session from 'express-session';
import * as fileStore from 'session-file-store';
import * as passport from "passport";
import * as cookieParser from "cookie-parser";
import { BasicStrategy } from "passport-http";
import { loadUsers } from "./users";
import { Application, static as StaticHandler } from 'express';
import * as fs from 'fs';
import { randomBytes } from 'crypto';
import * as proxy from 'http-proxy-middleware';
import * as path from 'path';
import * as process from 'process';

const {
  MLX_API_ENDPOINT        = 'mlx-api',
  REACT_APP_BASE_PATH     = '',
  SESSION_SECRET          = randomBytes(64).toString('hex'),
  KUBEFLOW_USERID_HEADER  = 'kubeflow-userid',
} = process.env;

const app = express() as Application;

const apiPrefix = 'apis/v1alpha1';

const staticDir = path.resolve(process.argv[2]);

const port = process.argv[3] || 3000;

const apiServerAddress = `http://${MLX_API_ENDPOINT}`;

type User = {
  username: string;
  email: string;
  roles: string[];
};

// enable session
initLogin(app);

if (REACT_APP_BASE_PATH.length !== 0) {
  app.all('/' + apiPrefix + '/*', checkPermissionMiddleware, proxy({
    changeOrigin: true,
    onProxyReq: proxyReq => {
      console.log('Proxied request: ', (proxyReq as any).path);
    },
    target: apiServerAddress,
  }));
}

app.all(REACT_APP_BASE_PATH  + '/' + apiPrefix + '/*',
    checkPermissionMiddleware, proxy({

  changeOrigin: true,
  onProxyReq: proxyReq => {
    console.log('Proxied request: ', (proxyReq as any).path);
  },
  pathRewrite: (path) =>
    path.startsWith(REACT_APP_BASE_PATH) ? path.substr(REACT_APP_BASE_PATH.length, path.length) : path,
  target: apiServerAddress,
}));

app.all('/session-validation*', sessionValidator);

const staticHandler = StaticHandler(staticDir, {redirect: false})

app.use(REACT_APP_BASE_PATH, StaticHandler(staticDir, {redirect: true}));
app.use(REACT_APP_BASE_PATH + '/pipelines/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/components/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/models/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/operators/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/notebooks/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/inferenceservices/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/upload/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/settings', staticHandler);
app.use(REACT_APP_BASE_PATH + '/delete/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/kiali/', staticHandler);
app.use(REACT_APP_BASE_PATH + '/experiments/', staticHandler);

if (REACT_APP_BASE_PATH.length !== 0) {
  app.use('/', staticHandler);
  app.use('/pipelines/', staticHandler);
  app.use('/components/', staticHandler);
  app.use('/models/', staticHandler);
  app.use('/operators/', staticHandler);
  app.use('/notebooks/', staticHandler);
  app.use('/upload/', staticHandler);
  app.use('/inferenceservices/', staticHandler);
  app.use('/settings', staticHandler);
  app.use('/delete/', staticHandler);
  app.use('/kiali/', staticHandler);
  app.use('/experiments/', staticHandler);
}

var limiter = new ratelimit({
  windowMs: 1*60*1000, // 1 minute
  max: 5
});

app.get('*', limiter, (req, res) => {
  // TODO: look into caching this file to speed up multiple requests.
  res.sendFile(path.resolve(staticDir, 'index.html'));
});

app.listen(port, () => {
  console.log('Server listening at http://localhost:' + port);
});

function initLogin(app: express.Application) {
  const users = loadUsers();

  passport.serializeUser<User, string>((user: User, done) => {
    done(undefined, user.username);
  });
  passport.deserializeUser<User, string>((username: string, done) => {
    done(undefined, {
      username: username,
      email: users[username].email,
      roles: users[username].roles
    });
  });

  passport.use(new BasicStrategy(
    (userid: string, password: string, done: (err: Error, user?: User|boolean) => any) => {
      if (users[userid] === undefined || users[userid].password !== password) {
        return done(null, false);
      }
      return done(null, {
          username: userid,
          email: users[userid].email,
          roles: users[userid].roles
      });
    }
  ));

  const storeFunc = fileStore(session);
  // Register related middlewares
  app.use(cookieParser());
  const sessOption : session.SessionOptions = {
    secret: SESSION_SECRET,
    saveUninitialized: true,
    cookie: {secure: 'auto', maxAge: 86400000},
    store: new storeFunc({}),
    resave: false
  }
  app.use(session(sessOption));
  app.use(passport.initialize())
  app.use(passport.session())

  app.get([REACT_APP_BASE_PATH + '/login'],
    passport.authenticate('basic'),
    (req, res) => {
      res.cookie('userinfo', JSON.stringify(req.user), {maxAge: 86400000});
      res.redirect(REACT_APP_BASE_PATH);
    }
  );
}

/**
 * Validate the request to see if the request contains a valid user information.
 * This is used as a ext authz for the custom action of istio authorizationpolicy
 */
function sessionValidator (req: express.Request, res: express.Response) {
  if (req.user === undefined ) {
    res.sendStatus(403);
    return;
  }
  res.setHeader(KUBEFLOW_USERID_HEADER, req.user.email);
  res.status(200);
  res.send();
};

/**
 * Reject all non-GET requests if there is no valid login
 * session.
 */
function checkPermissionMiddleware(
    req: express.Request,
    res: express.Response,
    next: express.NextFunction) {

  if (req.method !== 'GET' && req.user === undefined ) {
    res.sendStatus(403);
    return;
  }
  next();
}
