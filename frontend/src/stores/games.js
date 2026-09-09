import { defineStore } from "pinia";
import {ref} from 'vue'
import * as api from '@/api/client'

export const useGamesStore = defineStore('games', () => {
    const games = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    async function fetchGames() {
        isLoading.value = true
        error.value = null
        try{
            games.value = await api.listGames()
        }catch(err){
            error.value = err.message
        }finally{
            isLoading.value = false
        }
    }

    async function addGame(game){
        const created = await api.createGame(game)
        games.value.push(created)
    }

    async function removeGame(gameId){
        await api.deleteGame(gameId)
        games.value = games.value.filter((g) => g.id !== gameId)
    }

    async function refreshPrice(gameId) {
        const result = await api.refreshPrice(gameId)
        await fetchGames()
        return result
    }
    return {games, isLoading, error, fetchGames, addGame, removeGame, refreshPrice}
})