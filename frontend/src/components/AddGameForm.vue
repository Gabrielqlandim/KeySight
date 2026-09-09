<script setup>
import {ref} from 'vue'
import {useGamesStore} from '@/stores/games'

const store = useGamesStore()
const name = ref('')
const slug = ref('')

async function handleSubmit() {
    if(!name.value || !slug.value)
        return
    await store.addGame({
        name: name.value,
        slug: slug.value,
        image_url: null,
    })

    name.value=''
    slug.value=''
}
</script>

<template>
    <form class="add-game-form" @submit.prevent="handleSubmit">
        <input v-model="name" type="text" placeholder="Nome do jogo"/>
        <input v-model="slug" type="text" placeholder="slug-do-jogo"/>
        <button type="Submit">Adicionar</button>
    </form>
</template>

<style scoped>
.add-game-form{
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}
</style>