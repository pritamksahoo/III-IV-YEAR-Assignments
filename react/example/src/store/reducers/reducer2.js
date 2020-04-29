import * as actionTypes from '../actions/actionTypes';

const initialState = {
    username: []
}

const Reducer2 = (state = initialState, action) => {
    console.log("Reducer2")
    switch (action.type) {
        case actionTypes.USER_INPUT:
            return {
                username: [...state.username, action.text]
            }
        default:
            return state
    }
}

export default Reducer2;