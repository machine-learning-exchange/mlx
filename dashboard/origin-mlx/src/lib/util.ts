/* 
*  Copyright 2021 IBM Corporation 
* 
*  Licensed under the Apache License, Version 2.0 (the "License"); 
*  you may not use this file except in compliance with the License. 
*  You may obtain a copy of the License at 
* 
*      http://www.apache.org/licenses/LICENSE-2.0 
* 
*  Unless required by applicable law or agreed to in writing, software 
*  distributed under the License is distributed on an "AS IS" BASIS, 
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
*  See the License for the specific language governing permissions and 
*  limitations under the License. 
*/ 
import Cookies from 'js-cookie';

type UserInfo = {
  username: string;
  roles: string[];
}

const DEFAULT_USERINFO = {
  username: 'user',
  roles: ['user']
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

const addPeriod = (text: string) => text + (!text.endsWith('.') ? '.' : '')

export const firstSentence = (text: string) =>
  addPeriod(text).trim().replace(/(\r\n|\n|\r)/gm, ' ')
    .match(/^.*?[.!?](?:\s|$)/)[0]