<template>
	<v-container class="grey lighten-5">
		<v-row no-gutters>
			<v-col cols="12" md="12">
				<v-card>
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
					<v-data-table
						:headers="headers"
						:items="listadoTrayectos"
						item-key="nombre"
						class="elevation-25"
					>
						<template v-slot:top>
							<v-toolbar flat>
								<v-toolbar-title>Mantenedor Trayectos</v-toolbar-title>
								<v-divider class="mx-4" inset vertical></v-divider>
								<v-spacer></v-spacer>
								<v-dialog v-model="dialog" persistent max-width="900px">
									<template v-slot:activator="{ on, attrs }">
										<v-btn
											color="green darken-4"
											outlined
											class="mb-2"
											v-bind="attrs"
											v-on="on"
											@click="mostrarMensaje = false"
										>
											<v-icon>mdi-account-plus </v-icon>
											Nuevo Trayecto
										</v-btn>
									</template>
									<v-card>
										<v-card-title>
											<span class="headline">{{ formTitle }}</span>
										</v-card-title>
										<v-card-text v-if="editedIndex == -1">
											<b>Instrucciones:</b> <br />Favor ingrese origen y destino. <br />Ingrese el
											tiempo que estará disponible este recorrido (agregando fecha inicio y fecha
											final)<br />Añada la periodicidad que saldran los buses en horas (Minimo 1
											hr)<br />Una vez creado los registros, asigne los buses que realizarán los
											viajes (editando el registro)</v-card-text
										>
										<v-card-text v-if="editedIndex != -1">
											<b>Instrucciones:</b> <br />Solamente se puede editar los campos de Chofer y
											si el destino se encuentra disponible (checkbox)<br />
											Si se desactiva el viaje no aparecerá cuando se requiera comprar boletos al
											igual si no se tiene chofer asignado

											<br />
											PD: Si se elimina el registro, eliminará todos los registros que coincidan con
											Origen y Destino
										</v-card-text>

										<v-card-text>
											<v-container>
												<v-form ref="form" v-model="valid" lazy-validation>
													<v-row>
														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
															<v-select
																v-model="objTrayecto.origen"
																:items="listadoDestinos"
																item-text="comuna.name"
																item-value="comuna.name"
																label="Origen"
																persistent-hint
																single-line
																:rules="origen"
															></v-select>
														</v-col>
														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
															<v-select
																v-model="objTrayecto.destino"
																:items="listadoDestinos"
																item-text="comuna.name"
																item-value="comuna.name"
																label="Destino"
																persistent-hint
																single-line
																:rules="destino"
															></v-select>
														</v-col>
														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
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
																		v-model="objTrayecto.fecha_salida"
																		label="Fecha Inicio Recorrido"
																		prepend-icon="mdi-calendar"
																		readonly
																		v-bind="attrs"
																		v-on="on"
																	></v-text-field>
																</template>
																<v-date-picker
																	locale="es-ES"
																	:min="fecha_minimo_inicio"
																	v-model="objTrayecto.fecha_salida"
																	@input="menu2 = false"
																></v-date-picker>
															</v-menu>
														</v-col>
														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
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
																		locale="es-ES"
																		label="Fecha fin recorrido"
																		prepend-icon="mdi-calendar"
																		readonly
																		v-bind="attrs"
																		v-on="on"
																		v-model="objTrayecto.fecha_llegada"
																	></v-text-field>
																</template>
																<v-date-picker
																	locale="es-ES"
																	:min="cambiarFecha"
																	v-model="objTrayecto.fecha_llegada"
																	@input="menu2 = false"
																></v-date-picker>
															</v-menu>
														</v-col>
														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
															<v-text-field
																v-model="objTrayecto.precio"
																:rules="precio"
																label="Precio"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
															<v-text-field
																v-model="objTrayecto.periodicidad"
																:rules="periodicidad"
																label="Periodicidad (hrs)"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="3" v-if="editedIndex == -1">
															<v-text-field
																v-model="objTrayecto.duracion"
																:rules="duracion"
																label="Duracion Aproximada (hrs)"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="3" v-if="editedIndex != -1">
															<v-select
																v-model="objTrayecto.bus_asignado"
																:items="listadoBuses"
																item-text="patente"
																item-value="id"
																label="Bus Asignado"
																persistent-hint
																return-object
																single-line
																:rules="bus"
															></v-select>
														</v-col>

														<v-col cols="12" sm="6">
															<v-checkbox
																v-if="editedIndex >= 0"
																v-model="objTrayecto.disponible"
																label="¿ Destino Disponible ?"
															></v-checkbox>
														</v-col>
													</v-row>
												</v-form>
											</v-container>
										</v-card-text>

										<v-card-actions>
											<v-spacer></v-spacer>
											<v-btn color="red darken-1" outlined @click="close">
												Cancelar
											</v-btn>
											<v-btn
												v-if="editedIndex < 0"
												color="green darken-4"
												:disabled="!valid"
												outlined
												@click="guardarRegisto"
											>
												Guardar Registro
											</v-btn>
											<v-btn
												v-if="editedIndex >= 0"
												color="orange darken-1"
												:disabled="!valid"
												outlined
												@click="actualizarElemento"
											>
												Actualizar Registro
											</v-btn>
										</v-card-actions>
									</v-card>
								</v-dialog>
								<v-dialog v-model="dialogDelete" max-width="500px">
									<v-card>
										<v-card-title class="headline"
											>¿ Estas seguro de eliminar este registro ?</v-card-title
										>
										<v-card-actions>
											<v-spacer></v-spacer>
											<v-btn color="red darken-1" outlined @click="closeDelete">No</v-btn>
											<v-btn color="green darken-4" outlined @click="deleteItemConfirm">Si</v-btn>
											<v-spacer></v-spacer>
										</v-card-actions>
									</v-card>
								</v-dialog>
							</v-toolbar>
						</template>
						<template v-slot:[`item.actions`]="{ item }">
							<v-icon small class="mr-2" @click="editItem(item)">
								mdi-pencil
							</v-icon>
							<v-icon small @click="deleteItem(item)">
								mdi-delete
							</v-icon>
						</template>
						<template v-slot:no-data>
							No se ha encontrado información
						</template>
						<template v-slot:[`item.fecha_salida`]="{ item }">
							<v-chip color="green darken-1" dark>
								{{ item.fecha_salida }}
							</v-chip>
						</template>
						<template v-slot:[`item.fecha_llegada`]="{ item }">
							<v-chip color="blue darken-1" dark>
								{{ item.fecha_llegada }}
							</v-chip>
						</template>
						<template v-slot:[`item.bus_asignado.patente`]="{ item }">
							<v-chip v-if="item.bus_asignado" color="green darken-1" dark>
								{{ item.bus_asignado.patente }}
							</v-chip>
							<v-chip v-if="!item.bus_asignado" color="red darken-1" dark>
								Favor Asignar un bus
							</v-chip>
						</template>
						<template v-slot:[`item.disponible`]="{ item }">
							<v-chip v-if="item.disponible" color="green darken-1" dark>
								Trayecto Disponible
							</v-chip>
							<v-chip v-if="!item.disponible" color="red darken-1" dark>
								Trayecto deshabilitado
							</v-chip>
						</template>
					</v-data-table>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
	data: () => ({
		menu: '',
		menu2: '',
		/* Formulario - Campos y validaciones*/
		valid: true,
		origen: [(v) => !!v || 'Campo Requerido'],
		destino: [(v) => !!v || 'Campo Requerido'],
		precio: [
			(v) => !!v || 'Campo Requerido',
			(v) => /^[0-9]+$/.test(v) || 'Favor solo ingresar numeros',
		],
		bus: [(v) => !!v || 'Campo Requerido'],
		periodicidad: [
			(v) => !!v || 'Campo Requerido',
			(v) => /^[0-9]+$/.test(v) || 'Favor solo ingresar numeros',
		],
		duracion: [
			(v) => !!v || 'Campo Requerido',
			(v) => /^[0-9]+$/.test(v) || 'Favor solo ingresar numeros',
		],

		dialog: false,
		dialogDelete: false,
		checkbox: true,

		/* Mensajes y alertas */
		mostrarMensaje: false,
		cabecera: '',
		tipo: '',
		icono: '',
		texto: '',

		/* Data tables */
		headers: [
			{ text: 'Origen', value: 'origen', align: 'start' },
			{ text: 'Destino', value: 'destino', align: 'start' },
			{ text: 'Fecha Salida', value: 'fecha_salida' },
			{ text: 'Fecha llegada', value: 'fecha_llegada' },
			{ text: 'Precio', value: 'precio' },
			{ text: 'Bus asignado', value: 'bus_asignado.patente' },
			{ text: 'Disponible', value: 'disponible' },
			{ text: 'Porcentaje Ocupacion', value: 'porcentaje' },
			{ text: 'Actions', value: 'actions', sortable: false },
		],

		/* Listado de arreglos que almacenarán la informacion */
		listadoDestinos: [],
		listadoBuses: [],
		listadoTrayectos: [],
		listadoViejes: [],

		/* Index elemento seleccionado y/o flag para editar elemento */
		editedIndex: -1,

		/* Objetos temporales y por defecto */
		/* Se utilizan estos objs para almacenar los valores de los modals y/o asignar los valores correspondientes */

		fecha_minimo_inicio: '',
		fecha_minimo_final: '',

		objTrayecto: {
			origen: '',
			destino: '',
			precio: 0,
			fecha_salida: '',
			fecha_llegada: '',
			bus_asignado: '',
			disponible: true,
			periodicidad: '',
			duracion: '',
		},

		defaultItem: {
			origen: '',
			destino: '',
			precio: 0,
			fecha_salida: '',
			bus_asignado: '',
			disponible: true,
			periodicidad: '',
			fecha_llegada: '',
		},
	}),

	computed: {
		formTitle() {
			return this.editedIndex === -1 ? 'Nuevo Trayecto' : 'Editar Trayecto';
		},

		cambiarFecha() {
			this.objTrayecto.fecha_llegada = this.objTrayecto.fecha_salida;
			return (this.fecha_minimo_final = this.objTrayecto.fecha_salida);
		},
	},

	watch: {
		dialog(val) {
			val || this.close();
		},
		dialogDelete(val) {
			val || this.closeDelete();
		},
	},

	created() {
		this.traePorcentajeOcupacionTrayecto();

		this.traeDestinos();
		this.obtenerBuses();
		this.traerTrayectos();
		let fecha_actual = moment().format();
		fecha_actual = moment(fecha_actual).add(1, 'day');
		fecha_actual = moment(fecha_actual._d).format();
		this.fecha_minimo_inicio = fecha_actual.substring(0, 10);
	},

	methods: {
		/* Funcion que obtiene las comunas en Chile para la reacion de rutas */
		async traeDestinos() {
			let peticion = await axios.get(
				'https://private-anon-6dc34c8eee-gonzalobulnes.apiary-mock.com/comunas'
			);

			peticion.status == 200
				? (this.listadoDestinos = peticion.data)
				: this.muestraMensaje(
						'error',
						'mdi-cloud-alert',
						'Estimado Usuario, se le informa que ha ocurrido un error al buscar las comunas, favor comunicarse con el administrador'
				  );
		},

		/* Funcion que cierra la ventana modal de las modificaciones / agregar */
		close() {
			this.dialog = false;
			this.$nextTick(() => {
				this.objTrayecto = Object.assign({}, this.defaultItem);
				this.editedIndex = -1;
			});
			this.$refs.form.resetValidation();
			this.traerTrayectos();
		},

		editItem(item) {
			this.mostrarMensaje = false;
			this.editedIndex = this.listadoTrayectos.indexOf(item);
			this.objTrayecto = Object.assign({}, item);
			this.dialog = true;
		},

		muestraMensaje(tipo, icono, texto, cabecera) {
			this.mostrarMensaje = true;
			this.tipo = tipo;
			this.icono = icono;
			this.texto = texto;
			this.cabecera = cabecera;
		},

		async guardarRegisto() {
			/*
				Funcion para almacenar un set de recorridos donde el flujo es el siguiente
				1° Se añanden 23 hrs a la fecha final con la finalidad de darme el ultimo recorrido posible (ya que estos se manejan por hora)
				2° Comparar que la fecha - hora inicio sea menor a la final si es así sigue el proceso
				3° Aumento x cantidad de horas
			*/
			try {
				if (this.$refs.form.validate()) {
					let fecha_inicio_recorrido = moment(this.objTrayecto.fecha_salida);
					let fecha_fin_recorrido = moment(this.objTrayecto.fecha_llegada);
					fecha_fin_recorrido = fecha_fin_recorrido.add(23, 'hours');

					while (fecha_inicio_recorrido.format() <= fecha_fin_recorrido.format()) {
						let fecha_llegada = moment(fecha_inicio_recorrido.format());
						fecha_llegada.add(parseInt(this.objTrayecto.duracion), 'hours');

						let obj = {
							fecha_salida: this.formateoFechas(fecha_inicio_recorrido.format()),
							fecha_llegada: this.formateoFechas(fecha_llegada.format()),
							origen: this.objTrayecto.origen,
							destino: this.objTrayecto.destino,
							precio: this.objTrayecto.precio,
						};
						let peticion = await axios.post('http://localhost:8000/api/trayectos/', obj);
						if (peticion.status != 201) {
							throw new Error('Error !');
							break;
						} else {
							this.muestraMensaje(
								'success',
								'mdi-check-all',
								'Estimado Usuario, se han agregado los trayectos ingresados',
								'Correcto'
							);
						}
						fecha_inicio_recorrido = fecha_inicio_recorrido.add(
							parseInt(this.objTrayecto.periodicidad),
							'hours'
						);
					}

					this.close();
				} else {
					this.$refs.form.validate();
				}
			} catch (error) {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, se le informa que ha ocurrido un error, favor comunicarse con el administrador',
					'Error'
				);
			}
		},

		async obtenerBuses() {
			let peticion = await axios.get('http://localhost:8000/api/buses/');
			peticion.status == 200
				? (this.listadoBuses = peticion.data.filter((bus) => bus.disponible == true))
				: this.muestraMensaje(
						'error',
						'mdi-cloud-alert',
						'Estimado Usuario, se le informa que ha ocurrido un error, favor comunicarse con el administrador',
						'Error'
				  );
		},

		formateoFechas(fecha) {
			let dia = fecha.toString().substring(0, 10);
			let hora = fecha.toString().substring(11, 19);
			let formato = dia + ' ' + hora;
			return formato;
		},

		async traerTrayectos() {
			let peticion = await axios.get('http://localhost:8000/api/trayectos/');
			if (peticion.status == 200) {
				this.listadoTrayectos = [];
				let fecha_actual = moment().format('YYYY-MM-DD HH:mm:ss');
				peticion.data.forEach((trayecto) => {
					let encontrado = this.listadoViejes.find((viaje) => viaje.id == trayecto.id);
					trayecto.porcentaje = encontrado == undefined ? 0 : encontrado.cantidad * 10;
					this.listadoTrayectos.push(trayecto);
				});
				this.listadoTrayectos.sort((a, b) => (a.fecha_salida > b.fecha_salida ? 1 : -1));
			} else {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, se le informa que ha ocurrido un error, favor comunicarse con el administrador',
					'Error'
				);
			}
		},

		deleteItem(item) {
			this.editedIndex = this.listadoTrayectos.indexOf(item);
			this.objTrayecto = Object.assign({}, item);
			this.dialogDelete = true;
		},

		async deleteItemConfirm() {
			try {
				let peticion = await axios.delete(
					`http://localhost:8000/api/trayectos/${this.objTrayecto.id}/`
				);

				if (peticion.status == 204) {
					this.muestraMensaje(
						'success',
						'mdi-check-all',
						'Estimado Usuario, se ha eliminado el registro',
						'Correcto'
					);
				} else {
					throw new Error('Error');
				}
			} catch (error) {
				this.muestraMensaje(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, se le informa que ha ocurrido un error, favor comunicarse con el administrador',
					'Error'
				);
			} finally {
				this.closeDelete();
			}
		},

		closeDelete() {
			this.dialogDelete = false;
			this.$nextTick(() => {
				this.objTrayecto = Object.assign({}, this.defaultItem);
				this.editedIndex = -1;
			});

			this.traerTrayectos();
		},

		async actualizarElemento() {
			if (this.$refs.form.validate()) {
				this.objTrayecto.bus_asignado = this.objTrayecto.bus_asignado.id;
				let peticion = await axios.put(
					`http://localhost:8000/api/trayectos/${this.objTrayecto.id}/`,
					this.objTrayecto
				);

				peticion.status == 200
					? this.muestraMensaje(
							'success',
							'mdi-check-all',
							'Estimado Usuario, se le informa que ha ocurrido un error, favor comunicarse con el administrador',
							'Correcto'
					  )
					: this.muestraMensaje(
							'error',
							'mdi-cloud-alert',
							'Estimado Usuario, se le informa que ha ocurrido un error, favor comunicarse con el administrador',
							'Error'
					  );

				this.close();
			} else {
				this.$refs.form.validate();
			}
		},

		async traePorcentajeOcupacionTrayecto() {
			let peticion = await axios.get('http://localhost:8000/api/viajes/');

			let arreglo = [];
			peticion.data.forEach((viaje) => {
				let encontrado = arreglo.find((elemento) => elemento.id == viaje.trayecto.id);
				if (encontrado == undefined) {
					arreglo.push({ id: viaje.trayecto.id, cantidad: 1 });
				} else {
					encontrado.cantidad++;
				}
			});

			this.listadoViejes = arreglo;
		},
	},
};
</script>
