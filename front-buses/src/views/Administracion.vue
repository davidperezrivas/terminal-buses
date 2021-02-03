<template>
	<v-card>
		<v-card-title>
			<v-text-field
				v-model="search"
				append-icon="mdi-magnify"
				label="Search"
				single-line
				hide-details
			></v-text-field>
		</v-card-title>
		<v-data-table :headers="headers" :items="listadoViajes" :search="search"></v-data-table>
	</v-card>
</template>

<script>
import axios from 'axios';

export default {
	data: () => ({
		search: '',
		listadoViajes: [],
		headers: [
			{ text: 'Origen', value: 'origen' },
			{ text: 'Destino', value: 'origen' },
			{ text: 'Fecha Salida', value: 'origen' },
			{ text: 'Fecha Salida', value: 'origen' },
			{ text: '% Ocupacion', value: 'origen' },
		],
	}),
	computed: {},
	created() {},
	methods: {},
};
</script>
