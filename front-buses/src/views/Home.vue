<template>
	<v-container class="grey lighten-5">
		<v-row no-gutters>
			<v-col cols="12">
				<!-- Segmento Alerts -->
				<v-alert v-if="mostrarMensaje" text prominent :type="tipo" :icon="icono" border="left">
					<h3 class="headline">
						{{ cabecera }}
					</h3>
					<div>
						{{ texto }}
					</div>

					<v-divider class="my-4" :class="tipo" style="opacity: 0.22"></v-divider>

					<v-row align="center" no-gutters>
						<v-col class="grow"> </v-col>
						<v-spacer></v-spacer>
						<v-col class="shrink">
							<v-btn :color="tipo" outlined @click="mostrarMensaje = !mostrarMensaje">
								Entiendo
							</v-btn>
						</v-col>
					</v-row>
				</v-alert>

				<!-- Segmento Cabecera de las etapas -->
				<v-stepper v-model="steps">
					<v-stepper-header>
						<v-stepper-step :complete="steps > 1" step="1">
							Destinos
						</v-stepper-step>
						<v-divider></v-divider>
						<v-stepper-step :complete="steps > 2" step="2">
							Trayectos Ida
						</v-stepper-step>

						<v-divider></v-divider>

						<v-stepper-step :complete="steps > 2" step="3">
							Trayectos Vuelta
						</v-stepper-step>

						<v-divider></v-divider>

						<v-stepper-step step="4" :complete="steps > 4">
							Asientos Ida
						</v-stepper-step>

						<v-divider></v-divider>
						<v-stepper-step step="5" :complete="steps > 5">
							Asientos Vuelta
						</v-stepper-step>

						<v-divider></v-divider>

						<v-stepper-step step="6" :complete="steps > 6">
							Datos Personales
						</v-stepper-step>

						<v-divider></v-divider>

						<v-stepper-step step="7" :complete="steps > 7">
							Pago
						</v-stepper-step>
					</v-stepper-header>

					<!-- Etapa 1 - 7  -->
					<v-stepper-items>
						<v-stepper-content step="1">
							<v-card class="mb-12">
								<v-container>
									<v-form ref="form" lazy-validation>
										<v-row no-gutters>
											<v-col cols="12" md="6">
												<v-autocomplete
													v-model="objViaje.origen"
													:items="ciudades"
													item-text="comuna.name"
													item-value="comuna.name"
													label="Origen"
													persistent-hint
													prepend-icon="mdi-city"
												>
												</v-autocomplete>
											</v-col>
											<v-col cols="12" md="6">
												<v-autocomplete
													v-model="objViaje.destino"
													:items="ciudades"
													item-text="comuna.name"
													item-value="comuna.name"
													label="Destino"
													persistent-hint
													prepend-icon="mdi-city"
												>
												</v-autocomplete>
											</v-col>
											<v-col cols="12" md="6">
												<v-menu
													v-model="menu"
													:close-on-content-click="false"
													:nudge-right="40"
													transition="scale-transition"
													offset-y
													min-width="auto"
												>
													<template v-slot:activator="{ on, attrs }">
														<v-text-field
															v-model="objViaje.fecha_salida"
															label="Fecha Salida"
															prepend-icon="mdi-calendar"
															readonly
															v-bind="attrs"
															v-on="on"
														></v-text-field>
													</template>
													<v-date-picker
														locale="es-ES"
														:min="fecha_min"
														v-model="objViaje.fecha_salida"
														@input="menu = false"
													></v-date-picker>
												</v-menu>
											</v-col>
											<v-col cols="12" md="6">
												<v-menu
													v-model="menu2"
													:close-on-content-click="false"
													:nudge-right="40"
													transition="scale-transition"
													offset-y
													min-width="auto"
												>
													<template v-slot:activator="{ on, attrs }">
														<v-text-field
															v-model="objViaje.fecha_regreso"
															label="Fecha Vuelta"
															prepend-icon="mdi-calendar"
															readonly
															v-bind="attrs"
															v-on="on"
														></v-text-field>
													</template>
													<v-date-picker
														:min="objViaje.fecha_salida"
														locale="es-ES"
														v-model="objViaje.fecha_regreso"
														@input="menu2 = false"
													></v-date-picker>
												</v-menu>
											</v-col>

											<v-col cols="12">
												<v-select
													label="Cantidad Pasajes"
													:items="asientos"
													v-model="objViaje.num_pasajes"
												></v-select>
											</v-col>
										</v-row>
									</v-form>
								</v-container>
							</v-card>

							<v-btn v-if="!pasaSteps1" color="green darken-1" outlined @click="buscaTrayectos()">
								Continuar
							</v-btn>

							<v-btn v-if="pasaSteps1" color="green darken-1" outlined disabled>
								Continuar
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 2 - 7  -->

						<v-stepper-content step="2">
							<v-card class="mb-12 mx-auto">
								<v-list three-line>
									<template v-for="trayecto in trayectosIda">
										<v-list-item :key="trayecto.id">
											<v-list-item-avatar>
												<v-img></v-img>
											</v-list-item-avatar>

											<v-list-item-content>
												<v-list-item-title>
													{{ trayecto.origen }} - {{ trayecto.destino }}
												</v-list-item-title>
												<v-list-item-subtitle
													>Fecha Salida: {{ trayecto.fecha_salida }} - Fecha Llegada:
													{{ trayecto.fecha_llegada }}</v-list-item-subtitle
												>
											</v-list-item-content>

											<v-btn
												color="green darken-1"
												outlined
												@click="añadirTrayectoOrigen(trayecto)"
											>
												Elegir Viaje
											</v-btn>
										</v-list-item>
									</template>
								</v-list>
							</v-card>

							<v-btn color="red darken-1" outlined>
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 3 - 7  -->

						<v-stepper-content step="3">
							<v-card class="mb-12">
								<v-list three-line>
									<template v-for="trayecto in trayectosVuelta">
										<v-list-item :key="trayecto.id">
											<v-list-item-avatar>
												<v-img></v-img>
											</v-list-item-avatar>

											<v-list-item-content>
												<v-list-item-title>
													{{ trayecto.origen }} - {{ trayecto.destino }}
												</v-list-item-title>
												<v-list-item-subtitle
													>Fecha Salida: {{ trayecto.fecha_salida }} - Fecha Llegada:
													{{ trayecto.fecha_llegada }}</v-list-item-subtitle
												>
											</v-list-item-content>

											<v-btn
												color="green darken-1"
												outlined
												@click="añadirTrayectoRegreso(trayecto)"
											>
												Elegir Viaje
											</v-btn>
										</v-list-item>
									</template>
								</v-list>
							</v-card>

							<v-btn color="green darken-1" outlined @click="steps = 4">
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined>
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 4 - 7  -->

						<v-stepper-content step="4">
							<v-card class="mb-12">
								<v-row>
									<v-col v-for="n in 10" :key="n" cols="12" md="4">
										<v-btn class="ma-2" color="info">
											{{ n }}
											<v-icon dark right>
												mdi-sofa
											</v-icon>
										</v-btn>
									</v-col>
								</v-row>
							</v-card>

							<v-btn color="green darken-1" outlined @click="steps = 5">
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined>
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 5 - 7  -->

						<v-stepper-content step="5">
							<v-card class="mb-12">
								<v-row>
									<v-col v-for="n in 10" :key="n" cols="12" md="4">
										<v-btn class="ma-2" color="info" disabled>
											{{ n }}
											<v-icon dark right>
												mdi-sofa
											</v-icon>
										</v-btn>
									</v-col>
								</v-row>
							</v-card>

							<v-btn color="green darken-1" outlined @click="steps = 6">
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined>
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 6 - 7  -->

						<v-stepper-content step="6">
							<v-card class="mb-12"></v-card>

							<v-btn color="green darken-1" outlined @click="steps = 7">
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined>
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 7 - 7  -->

						<v-stepper-content step="7">
							<v-card class="mb-12"></v-card>

							<v-btn color="green darken-1" outlined>
								Pagar
							</v-btn>

							<v-btn color="red darken-1" outlined>
								Volver
							</v-btn>
						</v-stepper-content>
					</v-stepper-items>
				</v-stepper>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
	data: () => ({
		/* Mensajes y alertas */
		mostrarMensaje: false,
		cabecera: '',
		tipo: '',
		icono: '',
		texto: '',

		steps: 1,
		menu2: '',
		menu: '',
		fecha_min: '',
		trayectosIda: [],
		trayectosVuelta: [],
		viajesAlmacenados: [],

		viajeIda: [],
		viajeVuelta: [],

		asientos: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
		objViaje: {
			origen: '',
			destino: '',
			num_pasajes: '',
			fecha_salida: '',
			fecha_regreso: '',
		},
		ciudades: [],
	}),
	computed: {
		cambiarFecha() {
			this.objViaje.fecha_regreso = this.objViaje.fecha_salida;
			return (this.fecha_minimo_final = this.objTrayecto.fecha_salida);
		},

		pasaSteps1() {
			let camposVacios = true;

			let origen = this.objViaje.origen;
			let destino = this.objViaje.destino;
			let num_pasajes = this.objViaje.num_pasajes;
			let fecha_salida = this.objViaje.fecha_salida;
			let fecha_regreso = this.objViaje.fecha_regreso;
			if (
				origen != '' &&
				destino != '' &&
				num_pasajes != '' &&
				fecha_salida != '' &&
				fecha_regreso != ''
			) {
				camposVacios = false;
			}

			return camposVacios;
		},
	},
	created() {
		this.inicializarOrigenDestino();
		this.inicializarFechaMinima();
		this.traeViajes();
	},
	methods: {
		async inicializarOrigenDestino() {
			let peticion = await axios.get(
				'https://private-anon-6dc34c8eee-gonzalobulnes.apiary-mock.com/comunas'
			);
			peticion.status == 200
				? (this.ciudades = peticion.data)
				: this.muestraMensaje(
						'error',
						'mdi-cloud-alert',
						'Estimado Usuario, se le informa que ha ocurrido un error al buscar las comunas, favor comunicarse con el administrador'
				  );
		},

		inicializarFechaMinima() {
			let fecha_actual = moment().format();
			this.fecha_min = fecha_actual.substring(0, 10);
		},

		async buscaTrayectos() {
			try {
				this.steps = 1;

				let trayectos = [];

				let peticion = await axios.get('http://localhost:8000/api/trayectos/');
				if (peticion.status == 200) {
					trayectos = peticion.data;
				} else {
					throw new Error('Error mientras se encontraban los posibles');
				}

				this.trayectosIda = this.traeTrayectosFiltrados(
					trayectos,
					this.objViaje.fecha_salida,
					this.objViaje.origen,
					this.objViaje.destino
				);

				this.trayectosVuelta = this.traeTrayectosFiltrados(
					trayectos,
					this.objViaje.fecha_salida,
					this.objViaje.destino,
					this.objViaje.origen
				);

				if (this.trayectosIda.length == 0 || this.trayectosVuelta.length == 0) {
					throw new Error('No se encontraron viajes con los datos ingresados');
				}

				this.steps = 2;
			} catch (error) {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, se le informa que ha ocurrido un error: ' + error.message,
					'Error'
				);
			}
		},

		muestraMensaje(tipo, icono, texto, cabecera) {
			this.mostrarMensaje = true;
			this.tipo = tipo;
			this.icono = icono;
			this.texto = texto;
			this.cabecera = cabecera;
		},

		traeTrayectosFiltrados(trayectos, fecha_salida, origen, destino) {
			let salida = trayectos
				.filter((trayecto) => trayecto.fecha_salida.substring(0, 10) == fecha_salida)
				.filter((trayecto) => trayecto.disponible == true)
				.filter((trayecto) => trayecto.origen == origen)
				.filter((trayecto) => trayecto.destino == destino);

			return salida;
		},

		añadirTrayectoOrigen(trayecto) {
			this.steps = 3;
			this.viajeIda = this.viajesAlmacenados.filter((viaje) => viaje.trayecto_id == trayecto.id);
			console.log(viajeIda);
		},

		añadirTrayectoRegreso(trayecto) {
			this.steps = 4;
			this.viajeVuelta = this.viajesAlmacenados.filter((viaje) => viaje.trayecto_id == trayecto.id);
			console.log(this.viajeVuelta);
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
