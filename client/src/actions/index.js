export const SET_GAMES = 'SET_GAMES';

const setGames = games => {
    return {
        type: SET_GAMES,
        payload: games
    }
}

const API_URL = 'http://localhost:3010';

export const fetchGames = () => dispatch => {
    fetch(`${API_URL}/games`)
        .then(res => res.json())
        .then(data => dispatch(setGames(data)));
}
