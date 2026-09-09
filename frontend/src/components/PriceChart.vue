<script setup>
import {Line} from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, } from 'chart.js';
import { computed } from 'vue';
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
    history:{
        type: Array,
        required: true,
    },
})

const chartData = computed(() => ({
    labels: props.history.map((point) =>
    new Date(point.recorded_at).toLocaleDateString('pt-BR'),
    ),
    datasets:[
        {
            label: 'Preço (R$)',
            data: props.history.map((point) => point.price),
            borderColor: '#42b883',
            tension: 0.2,
        },
    ],
}))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
}
</script>

<template>
    <div style="height: 250px">
        <Line :data="chartData" :options="chartOptions"/>
    </div>
</template>