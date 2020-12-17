import { fetch } from 'whatwg-fetch'

export const apiRequest = (url, method='GET', authorized=false, body= null) => {
    let headers = {};

    if (body)
        headers = {
            ...headers,
            'Content-Type': 'application/json',
        }

    if (authorized)
        headers = {
            ...headers,
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }

    return fetch('http://localhost:3010' + url, {
        method,
        headers,
        body: body ? JSON.stringify(body): null
    });
}