const API_URL = 'http://localhost:3010';

async function getGames(setItems) {
    fetch(`${API_URL}/games`, {
        "credentials": "omit",
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/json,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        },
        "method": "GET",
        "mode": "cors"
    })
        .then(res => res.json())
        .then(data => setItems(data));
}

export default getGames;
