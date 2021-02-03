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
							<!-- Boton habilitado  -->
							<v-btn v-if="!pasaSteps1" color="green darken-1" outlined @click="buscaTrayectos()">
								Continuar
							</v-btn>
							<!-- Boton deshabilitad -->
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

							<v-btn color="red darken-1" outlined @click="volverStep(2)">
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

							<v-btn color="red darken-1" outlined @click="volverStep(3)">
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 4 - 7  -->

						<v-stepper-content step="4">
							<v-card class="mb-12">
								<v-row>
									<v-col v-for="viaje in viajeIda" :key="viaje.numero" cols="12" md="4">
										<v-btn
											class="ma-2"
											:color="viaje.color"
											:disabled="viaje.disabled"
											@click="almacenarAsientosIda(viaje)"
										>
											{{ viaje.numero }}
											<v-icon dark right>
												mdi-sofa
											</v-icon>
										</v-btn>
									</v-col>
								</v-row>
							</v-card>

							<v-btn
								color="green darken-1"
								outlined
								v-if="this.objViaje.asientosSeleccionadosIda.length != this.objViaje.num_pasajes"
								disabled
							>
								Continuar
							</v-btn>

							<v-btn
								v-if="this.objViaje.asientosSeleccionadosIda.length == this.objViaje.num_pasajes"
								color="green darken-1"
								outlined
								@click="steps = 5"
							>
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined @click="volverStep(4)">
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 5 - 7  -->

						<v-stepper-content step="5">
							<v-card class="mb-12">
								<v-row>
									<v-col v-for="viaje in viajeVuelta" :key="viaje.numero" cols="12" md="4">
										<v-btn
											class="ma-2"
											:color="viaje.color"
											:disabled="viaje.disabled"
											@click="almacenarAsientosVuelta(viaje)"
										>
											{{ viaje.numero }}
											<v-icon dark right>
												mdi-sofa
											</v-icon>
										</v-btn>
									</v-col>
								</v-row>
							</v-card>

							<v-btn
								color="green darken-1"
								outlined
								v-if="this.objViaje.asientosSeleccionadosVuelta.length != this.objViaje.num_pasajes"
								disabled
							>
								Continuar
							</v-btn>

							<v-btn
								v-if="this.objViaje.asientosSeleccionadosVuelta.length == this.objViaje.num_pasajes"
								color="green darken-1"
								outlined
								@click="steps = 6"
							>
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined @click="volverStep(5)">
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 6 - 7  -->

						<v-stepper-content step="6">
							<v-card class="mb-12">
								<v-form ref="form" lazy-validation>
									<v-row>
										<v-col cols="12" sm="3">
											<v-text-field
												label="Nombre"
												required
												v-model="objViaje.usuario.nombre"
												:rules="objRules.nombreRules"
											></v-text-field>
										</v-col>
										<v-col cols="12" sm="3">
											<v-text-field
												label="Apellido"
												v-model="objViaje.usuario.apellido"
												:rules="objRules.apellidoRules"
												required
											></v-text-field>
										</v-col>
										<v-col cols="12" sm="3">
											<v-text-field
												label="run"
												v-model="objViaje.usuario.run"
												:rules="objRules.rutRules"
												required
											></v-text-field>
										</v-col>
										<v-col cols="12" sm="3">
											<v-text-field
												label="Email"
												v-model="objViaje.usuario.email"
												:rules="objRules.emailRules"
												required
											></v-text-field>
										</v-col>
										<v-col cols="12" sm="3">
											<v-text-field
												label="Telefono"
												v-model="objViaje.usuario.telefono"
												:rules="objRules.telefonoRules"
												required
											></v-text-field>
										</v-col>
									</v-row>
								</v-form>
							</v-card>

							<v-btn color="green darken-1" outlined @click="almacenaOBuscaUsuario()">
								Continuar
							</v-btn>

							<v-btn color="red darken-1" outlined @click="volverStep(6)">
								Volver
							</v-btn>
						</v-stepper-content>

						<!-- Etapa 7 - 7  -->

						<v-stepper-content step="7">
							<v-card class="mb-12"> El monto a pagar es de {{ totalViaje }} </v-card>

							<v-btn color="green darken-1" outlined @click="realizarPago()">
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

		totalViaje: 0,

		viajeIda: [],
		viajeVuelta: [],

		objRules: {
			nombreRules: [
				(v) => !!v || 'Campo Requerido',
				(v) => (v && v.length < 50) || 'Campo no debe sobrepasar los 50 caracteres',
			],
			apellidoRules: [
				(v) => !!v || 'Campo Requerido',
				(v) => (v && v.length < 50) || 'Campo no debe sobrepasar los 50 caracteres',
			],
			rutRules: [
				(v) => !!v || 'Campo Requerido',
				(v) => /^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(v) || 'Ingrese Rut sin punto y con guion',
			],

			emailRules: [
				(v) => !!v || 'Campo Requerido',
				(v) => /.+@.+\..+/.test(v) || 'Ingrese Email Valido',
			],
			telefonoRules: [
				(v) => !!v || 'Campo Requerido',
				(v) => /^[0-9]+$/.test(v) || 'Favor ingresar solo números',
			],
		},

		asientos: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
		objViaje: {
			origen: '',
			destino: '',
			num_pasajes: '',
			fecha_salida: '',
			fecha_regreso: '',
			asientosSeleccionadosIda: [],
			asientosSeleccionadosVuelta: [],
			usuario: {
				id: '',
				nombre: '',
				apellido: '',
				run: '',
				telefono: '',
				email: '',
			},
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
			console.log(trayecto);

			this.objViaje.trayectoIda = trayecto.id;
			this.steps = 3;
			this.viajeIda = [];

			let viajes = this.viajesAlmacenados
				.filter((viaje) => viaje.trayecto.id == trayecto.id)
				.map((viaje) => viaje.num_asiento);

			for (let index = 1; index <= 10; index++) {
				let obj = {
					numero: index,
					disabled: viajes.indexOf(index) > -1 && viajes.length != 0 ? true : false,
					color: 'info',
				};
				console.log(obj);
				this.viajeIda.push(obj);
			}
		},

		añadirTrayectoRegreso(trayecto) {
			this.objViaje.trayectoRegreso = trayecto.id;
			this.steps = 4;
			let viajes = this.viajesAlmacenados
				.filter((viaje) => viaje.trayecto == trayecto.id)
				.map((viaje) => viaje.num_asiento);
			this.viajeVuelta = [];
			for (let index = 1; index <= 10; index++) {
				let obj = {
					numero: index,
					disabled: viajes.indexOf(index) > -1 ? true : false,
					color: 'info',
				};
				this.viajeVuelta.push(obj);
			}
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

		almacenarAsientosIda(viaje) {
			if (this.objViaje.asientosSeleccionadosIda.length < this.objViaje.num_pasajes) {
				this.objViaje.asientosSeleccionadosIda.push(viaje.numero);

				this.viajeIda.forEach((viajeIda) => {
					if (viajeIda.numero == viaje.numero) {
						viaje.color = 'warning';
					}
				});
			} else {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario ya ha seleccionado los asientos solicitados',
					'Error'
				);
			}
		},

		almacenarAsientosVuelta(viaje) {
			if (this.objViaje.asientosSeleccionadosVuelta.length < this.objViaje.num_pasajes) {
				this.objViaje.asientosSeleccionadosVuelta.push(viaje.numero);

				this.viajeVuelta.forEach((viajeVuelta) => {
					if (viajeVuelta.numero == viaje.numero) {
						viaje.color = 'warning';
					}
				});
			} else {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario ya ha seleccionado los asientos solicitados',
					'Error'
				);
			}
		},

		volverStep(num) {
			if (num == 4) {
				this.viajeIda.forEach((viaje) => (viaje.color = 'info'));
				this.objViaje.asientosSeleccionadosIda = [];
			}

			if (num == 5) {
				this.viajeVuelta.forEach((viaje) => (viaje.color = 'info'));
				this.objViaje.asientosSeleccionadosVuelta = [];
			}

			this.steps = num - 1;
		},

		async almacenaOBuscaUsuario() {
			try {
				this.calcularTotalAPagar();
				if (this.$refs.form.validate()) {
					let peticion = await axios.get('http://localhost:8000/api/pasajeros/');
					if (peticion.status == 200) {
						let pasajeros = peticion.data;

						let pasajeroEncontrado = pasajeros.find(
							(pasajero) => pasajero.run == this.objViaje.usuario.run
						);

						if (pasajeroEncontrado == undefined) {
							let peticion = await axios.post(
								'http://localhost:8000/api/pasajeros/',
								this.objViaje.usuario
							);
							if (peticion.status == 201) {
								this.objViaje.usuario.id = peticion.data.id;
							}
						} else {
							this.objViaje.usuario.id = pasajeroEncontrado.id;
							if (!this.validaValoresPasajeros(pasajeroEncontrado)) {
								await axios.put(
									`http://localhost:8000/api/pasajeros/${pasajeroEncontrado.id}/`,
									this.objViaje.usuario
								);
							}
						}
					}
					this.steps = 7;
				} else {
					this.$refs.form.validate();
				}
			} catch (error) {
				console.log(error);
			}
		},

		validaValoresPasajeros(encontrado) {
			let run = this.objViaje.usuario.run;
			let nombre = this.objViaje.usuario.nombre;
			let apellido = this.objViaje.usuario.apellido;
			let email = this.objViaje.usuario.email;
			let telefono = this.objViaje.usuario.telefono;

			if (
				encontrado.run == run &&
				encontrado.nombre == nombre &&
				encontrado.apellido == apellido &&
				encontrado.email == email &&
				encontrado.telefono == telefono
			) {
				return true;
			}

			return false;
		},

		async calcularTotalAPagar() {
			let peticionIda = await axios.get(
				`http://localhost:8000/api/trayectos/${this.objViaje.trayectoIda}/`
			);
			let peticionVuelta = await axios.get(
				`http://localhost:8000/api/trayectos/${this.objViaje.trayectoRegreso}/`
			);
			let precioIda = peticionIda.data.precio * this.objViaje.num_pasajes;
			let precioVuelta = peticionVuelta.data.precio * this.objViaje.num_pasajes;

			this.totalViaje = precioIda + precioVuelta;
		},

		async realizarPago() {
			for (let index = 0; index < this.objViaje.asientosSeleccionadosIda.length; index++) {
				let asientoIda = this.objViaje.asientosSeleccionadosIda[index];
				let asientoRegreso = this.objViaje.asientosSeleccionadosVuelta[index];

				let objIda = {
					pasajero: this.objViaje.usuario.id,
					trayecto: this.objViaje.trayectoIda,
					num_asiento: asientoIda,
				};

				let objRegreso = {
					pasajero: this.objViaje.usuario.id,
					trayecto: this.objViaje.trayectoRegreso,
					num_asiento: asientoRegreso,
				};

				await axios.post('http://localhost:8000/api/viajes/', objIda);

				await axios.post('http://localhost:8000/api/viajes/', objRegreso);
			}
		},
	},
};
</script>
