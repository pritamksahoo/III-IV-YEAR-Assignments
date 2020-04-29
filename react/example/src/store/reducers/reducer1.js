import * as actionTypes from '../actions/actionTypes';

const initialState = {
    prop1: false
}

const Reducer1 = (state = initialState, action) => {
    console.log("Reducer1")
    switch (action.type) {
        case actionTypes.SUCCESS:
            return {
                prop1: true
            }
        case actionTypes.FAILURE:
            return {
                prop1: false
            }
        default:
            return state
    }
}

export default Reducer1;