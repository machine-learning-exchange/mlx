// SPDX-License-Identifier: Apache-2.0

import * as express from 'express';
import * as ratelimit from 'express-rate-limit'
import * as session from 'express-session';
import * as fileStore from 'session-file-store';
import * as passport from "passport";
import * as cookieParser from "cookie-parser";
import { BasicStrategy } from "passport-http";
import { loadUsers, DEFAULT_ADMIN_EMAIL } from "./users";
import { Application, static as StaticHandler } from 'express';
import * as fs from 'fs';
import { randomBytes } from 'crypto';
import * as proxy from 'http-proxy-middleware';
import * as path from 'path';
import * as process from 'process';
import { ClientRequest } from 'http';

const {
  MLX_API_ENDPOINT        = 'mlx-api',
  REACT_APP_BASE_PATH     = '',
  SESSION_SECRET          = randomBytes(64).toString('hex'),
  KUBEFLOW_USERID_HEADER  = 'kubeflow-userid',
  REACT_APP_DISABLE_LOGIN = 'false',
  REACT_APP_RATE_LIMIT    = 100,
} = process.env;

const app = express() as Application;

const apiPrefix = 'apis/v1alpha1';

const staticDir = path.resolve(process.argv[2]);

const port = process.argv[3] || 3000;

const apiServerAddress = `http://${MLX_API_ENDPOINT}`;

const disableLogin = REACT_APP_DISABLE_LOGIN === 'true';

type User = {
  username: string;
  email: string;
  roles: string[];
};

const proxyCheckingMiddleware = [];
// enable login and permission check
if (!disableLogin) {
  initLogin(app);
  proxyCheckingMiddleware.push(checkPermissionMiddleware);
}

if (REACT_APP_BASE_PATH.length !== 0) {
  app.all('/' + apiPrefix + '/*',
      [...proxyCheckingMiddleware, getForwardProxyMiddleware(!disableLogin)]);
}

app.all(REACT_APP_BASE_PATH  + '/' + apiPrefix + '/*',
    [...proxyCheckingMiddleware, getForwardProxyMiddleware(!disableLogin, REACT_APP_BASE_PATH)]);

app.all('/session-validation*', getSessionValidator(!disableLogin));

const staticHandler = StaticHandler(staticDir, {redirect: false})

app.use(REACT_APP_BASE_PATH, (req, res, next) => {
  const staticIndex = req.url.indexOf('/static/')
  if (staticIndex !== -1) {
    req.url = req.url.substring(staticIndex)
  }
  else if (!req.url.endsWith('.js')) {
    req.url = '/'
  }
  StaticHandler(staticDir)(req, res, next);
});

// TODO: This may or may not be needed anymore. Originally there were routing issues that 
// caused routes to incorrectly fail when refreshing the react page.
// These should be fixed now, but should be tested to ensure they are.
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
  max: REACT_APP_RATE_LIMIT
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

  const redirectPath = REACT_APP_BASE_PATH.length === 0 ? '/' : REACT_APP_BASE_PATH;
  app.get([REACT_APP_BASE_PATH + '/login'],
    passport.authenticate('basic'),
    (req, res) => {
      res.cookie('userinfo', JSON.stringify(req.user), {maxAge: 86400000});
      res.redirect(redirectPath);
    }
  );
}

/**
 * get session validator based on `login` flag
 */
function getSessionValidator(login: boolean) :
    (req: express.Request, res: express.Response) => void {

  if (login) {
    return sessionValidator;
  } else {
    /*
     when login is disabled, all requests are treated as admin
     */
    return (req: express.Request, res: express.Response) => {
      res.setHeader(KUBEFLOW_USERID_HEADER, DEFAULT_ADMIN_EMAIL);
      res.status(200);
      res.send();
    }
  }
}

function getForwardProxyMiddleware(login: boolean, rewritePath?: string) :
    (req: express.Request, res: express.Response) => void {

  const proxyOpts: proxy.Options = {
    changeOrigin: true,
    target: apiServerAddress,
  };
  if (login) {
    proxyOpts.onProxyReq = (proxyReq: ClientRequest, req: express.Request) => {
      if (req.user) {
        proxyReq.setHeader(KUBEFLOW_USERID_HEADER, req.user.email);
      }
      console.log('Proxied request: ', proxyReq.path);
    };
  } else {
    proxyOpts.onProxyReq = (proxyReq: ClientRequest, req: express.Request) => {
      proxyReq.setHeader(KUBEFLOW_USERID_HEADER, DEFAULT_ADMIN_EMAIL);
      console.log('Proxied request: ', proxyReq.path);
    };
  }
  if (rewritePath) {
    const pattern = RegExp(`^${rewritePath}`);
    proxyOpts.pathRewrite = (path: string) : string => {
      return path.replace(pattern, '');
    }
  }
  return proxy(proxyOpts);
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
