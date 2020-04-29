import Reducer1 from './reducer1';
import Reducer2 from './reducer2';
import AuthReducer from './authReducer';

import { combineReducers } from 'redux';

const rootReducer = combineReducers({
    Reducer1,
    Reducer2,
    AuthReducer
})

export default rootReducer;