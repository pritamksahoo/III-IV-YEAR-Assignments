import * as actionTypes from './actionTypes'

export const success = {
    type: actionTypes.SUCCESS
}

export const failure = {
    type: actionTypes.FAILURE
}

export const userInput = (text) => {
    return {
        type: actionTypes.USER_INPUT,
        text
    }
}

export const login_success = () => {
    return {
        type: actionTypes.LOGIN_SUCCESS
    }
}

export const login_failure = () => {
    return {
        type: actionTypes.LOGIN_FAILURE
    }
}