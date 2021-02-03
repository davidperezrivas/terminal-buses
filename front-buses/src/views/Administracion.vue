<template> </template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
	data: () => ({}),
	computed: {},
	created() {},
	methods: {
		muestraMensaje(tipo, icono, texto, cabecera) {
			this.mostrarMensaje = true;
			this.tipo = tipo;
			this.icono = icono;
			this.texto = texto;
			this.cabecera = cabecera;
		},

		async traeViajes() {
			try {
				let peticion = await axios.get('http://localhost:8000/api/viajes/');
				if (peticion.status == 200) {
					this.viajesAlmacenados = peticion.data;
				} else {
					throw new Exception('Error listar viajes');
				}
			} catch (error) {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, se le informa que ha ocurrido un error: ' + error.message,
					'Error'
				);
			}
		},
	},
};
</script>
