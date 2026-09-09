<script setup>
import PriceChart from './PriceChart.vue';
import * as api from '@/api/client';
import {ref, onMounted} from 'vue'


const props = defineProps({
    game: {
        type: Object,
        required: true,
    },
})
const emit = defineEmits(['delete','refresh'])

const offers = ref([])
const history = ref([])

async function loadPriceData() {
    offers.value = await api.listOffers(props.game.id)
    history.value = await api.getPriceHistory(props.game.id)
}

onMounted(loadPriceData)

async function handleRefreshClick() {
    emit('refresh', props.game.id)
    await api.refreshPrice(props.game.id)
    await loadPriceData()
}
</script>

<template>
    <div class="game-card">
        <h3>{{game.name}}</h3>
        <p class="slug">{{game.slug}}</p>

        <ul v-if="offers.length" class="offers">
            <li v-for="offer in offers" :key="offer.id">
                {{ offer.store_name }}: R$ {{ offer.current_price.toFixed(2) }}
            </li>
        </ul>
        <p v-else class="no-offers">Nenhum preço registrado ainda</p>

        <PriceChart v-if="history.length" :history="history"/>

        <div class="actions">
            <button @click="handleRefreshClick">Atualizar preço</button>
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

.offers{
    list-style: none;
    padding: 0;
    font-size: 0.9rem;
}

.no-offers{
    font-size: 0.9rem;
    color: #888;
}
.actions{
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
</style>
            