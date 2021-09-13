/* 
* Copyright 2021 IBM Corporation 
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import Cookies from 'js-cookie';
import { titleCase } from "title-case";

const disableLogin = process.env.REACT_APP_DISABLE_LOGIN === 'true';

type UserInfo = {
  username: string;
  roles: string[];
}

const DEFAULT_USERINFO = {
  username: 'user',
  roles: [disableLogin ? 'admin' : 'user']
};

let gUserInfo: UserInfo;
export function getUserInfo(): UserInfo {
  return gUserInfo || (() => {
    const userinfo = Cookies.get('userinfo');
    if (userinfo === undefined) {
      gUserInfo = DEFAULT_USERINFO;
    } else {
      gUserInfo = JSON.parse(userinfo)
    }
    return gUserInfo;
  })();
}

export function hasRole(user: UserInfo, role: string): boolean {
  return user.roles.indexOf(role) !== -1;
}

export function canShow(adminOnly: boolean, isAdmin: boolean) {
  return !(adminOnly === true && isAdmin === false);
}

export const capitalize = (lower: string) =>
  lower.charAt(0).toUpperCase().concat(lower.slice(1));

export const formatTitle = (title: string) => {
  let newTitle = title;
  // If there are any dashes (-), underscores(_), or periods (.) replace them with spaces
  newTitle = newTitle.replace(/[-_.]/g, " ")
  // Upper case the first letter of the title
  newTitle = titleCase(newTitle)
  return newTitle
}

const addPeriod = (text: string) => text + (!text.endsWith('.') ? '.' : '')

export const firstSentence = (text: string) =>
  addPeriod(text).trim().replace(/(\r\n|\n|\r)/gm, ' ')
    .match(/^.*?[.!?](?:\s|$)/)[0]