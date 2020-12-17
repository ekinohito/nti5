import {CLOSE_ALL_MODALS, SET_AUTH_MODAL_IS_OPEN, SET_GAMES, SET_USER} from "../actions";

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
        case SET_AUTH_MODAL_IS_OPEN:
            return {
                ...state,
                authModalIsOpen: action.payload
            }
        case CLOSE_ALL_MODALS:
            return {
                ...state,
                authModalIsOpen: false
            }
        case SET_USER:
            return {
                ...state,
                user: action.payload
            }
        default:
            return state
    }
}

export default rootReducer;
