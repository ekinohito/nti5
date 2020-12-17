import {SET_GAMES} from "../actions";

const initialState = {
    user: null,
    games: [],
    authModalIsOpen: false
}

const rootReducer = (state=initialState, action) => {
    switch (action.type) {
        case SET_GAMES:
            return {
                ...state,
                games: action.payload
            }
        default:
            return state
    }
}

export default rootReducer;
