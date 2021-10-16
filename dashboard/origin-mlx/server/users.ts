// SPDX-License-Identifier: Apache-2.0

import {existsSync} from 'fs';

/**
 * Represent all of the users and their information, including
 * password and roles.
 */
export type Users = {
    [name: string]: UserInfo
};

/**
 * User information
 */
type UserInfo = {
    password: string; // password
    email: string;    // email
    roles: string[]; // roles for the user
};

const DEFAULT_USER_CONFIG = '/workspace/models/admin.json';
export const DEFAULT_ADMIN_EMAIL = 'mlx@ibm.com';

export function loadUsers(): Users {
    if (existsSync(DEFAULT_USER_CONFIG)) {
        return require(DEFAULT_USER_CONFIG);
    }
    // return default settings if config file doesn't exist
    return {"admin": {"password": "passw0rd", "email": DEFAULT_ADMIN_EMAIL, "roles": ["admin"]}};
}

