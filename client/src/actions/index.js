import {apiRequest} from "../http";

export const SET_GAMES = 'SET_GAMES';
export const CLOSE_ALL_MODALS = 'CLOSE_ALL_MODALS';
export const SET_AUTH_MODAL_IS_OPEN = 'SET_AUTH_MODAL_IS_OPEN';
export const SET_USER = 'SET_USER';

export const closeAllModals = () => {
    return {
        type: CLOSE_ALL_MODALS
    }
}

export const setAuthModalIsOpen = (isOpen) => {
    return {
        type: SET_AUTH_MODAL_IS_OPEN,
        payload: isOpen
    }
}

export const setUser = (user) => {
    return {
        type: SET_USER,
        payload: user
    }
}

export const fetchUser = () => dispatch => {
    apiRequest('/user', 'GET', true)
        .then(res => res.json())
        .then(user => dispatch(setUser(user)))
}

const setGames = games => {
    return {
        type: SET_GAMES,
        payload: games
    }
}

export const fetchGames = () => dispatch => {
    apiRequest('/games')
        .then(res => res.json())
        .then(data => dispatch(setGames(data)));
}
