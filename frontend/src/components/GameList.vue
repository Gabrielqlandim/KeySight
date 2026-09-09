<script setup>
import {onMounted} from 'vue'
import { useGamesStore } from '@/stores/games'
import GameCard from './GameCard.vue'

const store = useGamesStore()

onMounted(() => {
    store.fetchGames()
})

function  handleDelete(gameId) {
    store.removeGame(gameId)
}

async function handleRefresh(gameId) {
    await store.refreshPrice(gameId)
}
</script>
<template>
    <div>
        <p v-if="store.isLoading">Carregando jogos...</p>
        <p v-else-if="store.error">Erro: {{store.error}}</p>
        <p v-else-if="!store.games.length">Nenhum jogo cadastrado ainda.</p>

        <div v-else>
            <GameCard
            v-for="game in store.games"
            :key="game.id"
            :game="game"
            @delete="handleDelete"
            @refresh="handleRefresh"/>

        </div>
    </div>
</template>