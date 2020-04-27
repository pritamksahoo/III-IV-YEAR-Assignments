import * as actionTypes from '../actions/actionTypes';

const initialState = {
    prop1: false
}

const rootReducer = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.SUCCESS:
            return {
                ...state,
                prop1: true
            }
        case actionTypes.FAILURE:
            return {
                ...state,
                prop1: false
            }
        default:
            return state
    }
}

export default rootReducer;