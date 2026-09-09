<script setup>
const props = defineProps({
    game: {
        type: Object,
        required: true,
    },
})
const emit = defineEmits(['delete','refresh'])
</script>

<template>
    <div class="game-card">
        <h3>{{game.name}}</h3>
        <p class="slug">{{game.slug}}</p>
        <div class="actions">
            <button @click="emit('refresh',game.id)">Atualizar preço</button>
            <button @click="emit('delete',game.id)">Remover</button>
        </div>
    </div>
</template>

<style scoped>

.game-card{
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}

.slug{
    color: #888;
    font-size: 0.85rem;
}
.actions{
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
</style>
            