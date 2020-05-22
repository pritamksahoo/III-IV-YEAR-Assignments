import * as actionTypes from  './actionTypes';

export const login = (username) => {
    return {
        type: actionTypes.LOG_IN,
        user: username
    }
}

export const logout = (username) => {
    return {
        type: actionTypes.LOG_OUT,
        user: username
    }
}