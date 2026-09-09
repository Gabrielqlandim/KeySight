const API_BASE_URL = 'http://localhost:8000'

async function request(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`,{
        headers: {'Content-Type': 'application/json'},
        ...options,
    })

    if (!response.ok){
        const body = await response.json().catch(()=> null)
        throw new Error(body?.detail || `Erro ${response.status}`)
    }
    if(response.status === 204)
        return null

    return response.json()
}

export function listGames(){
    return request('/games')
}

export function createGame(game){
    return request('/games', {method: 'POST', body: JSON.stringify(game),})
}

export function deleteGame(gameId){
    return request(`/games/${gameId}`, {method: 'DELETE'})
}

export function refreshPrice(gameId){
    return request(`/game/${gameId}/refresh-price`, {method: 'POST'})
}