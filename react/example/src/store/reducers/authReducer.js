import * as actionTypes from '../actions/actionTypes';

const initialState = {
    isAuthenticated: false
}

const AuthReducer = (state = initialState, action) => {
    // console.log("Reducer1")
    switch (action.type) {
        case actionTypes.LOGIN_SUCCESS:
            return {
                isAuthenticated: true
            }
        case actionTypes.LOGIN_FAILURE:
            return {
                isAuthenticated: false
            }
        default:
            return state
    }
}

export default AuthReducer;