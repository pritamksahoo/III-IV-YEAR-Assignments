import * as actionTypes from '../actions/actionTypes';

const initialState = {
    isAuthenticated: false,
    user: null
}

const AuthReducer = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.LOG_IN:
            return {
                ...state,
                isAuthenticated: true,
                user: action.user
            }

        case actionTypes.LOG_OUT:
            // console.log("action", action.user, state.user)
            if (state.user === action.user) {
                return {
                    ...state,
                    isAuthenticated: false,
                    user: null
                }
            } else {
                return state
            }

        default:
            return state
    }
}

export {AuthReducer};