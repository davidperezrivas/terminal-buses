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
						:items="listadoBuses"
						item-key="nombre"
						class="elevation-25"
					>
						<template v-slot:top>
							<v-toolbar flat>
								<v-toolbar-title>Mantenedor Buses</v-toolbar-title>
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
											Nuevo Bus
										</v-btn>
									</template>
									<v-card>
										<v-card-title>
											<span class="headline">{{ formTitle }}</span>
										</v-card-title>

										<v-card-text>
											<v-container>
												<v-form ref="form" v-model="valid" lazy-validation>
													<v-row>
														<v-col cols="12" sm="6">
															<v-text-field
																v-model="objBus.patente"
																:rules="patenteRules"
																label="Patente"
																required
															></v-text-field>
														</v-col>
														<v-col cols="12" sm="6">
															<v-select
																v-model="objBus.chofer_asignado"
																:items="listadoChoferes"
																item-text="nombre"
																item-value="id"
																label="Chofer"
																persistent-hint
																return-object
																single-line
																:rules="choferRules"
															></v-select>
														</v-col>

														<v-col cols="12">
															<v-checkbox
																v-if="editedIndex >= 0"
																v-model="objBus.disponible"
																label="¿ Bus Disponible ?"
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
												@click="guardarBus"
											>
												Guardar Registro
											</v-btn>
											<v-btn
												v-if="editedIndex >= 0"
												color="orange darken-1"
												:disabled="!valid"
												outlined
												@click="actualizarBus"
											>
												Actualizar Registro
											</v-btn>
										</v-card-actions>
									</v-card>
								</v-dialog>
							</v-toolbar>
						</template>
						<template v-slot:[`item.actions`]="{ item }">
							<v-icon small class="mr-2" @click="editItem(item)">
								mdi-pencil
							</v-icon>
						</template>
						<template v-slot:no-data>
							No se ha encontrado información
						</template>
					</v-data-table>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';

export default {
	data: () => ({
		/* Formulario - Campos y validaciones*/
		valid: true,
		patenteRules: [
			(v) => !!v || 'Campo Requerido',
			(v) => (v && v.length <= 10) || 'Campo no debe sobrepasar los 10 caracteres',
			(v) => /^([A-Z]{2,5})-([0-9]{2,3})/.test(v) || 'Favor utilizar formato AAAA 00',
		],

		choferRules: [(v) => !!v || 'Campo Requerido'],

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
			{ text: 'Patente', value: 'patente', align: 'start' },
			{ text: 'Chofer Asignado', value: 'conductor' },
			{ text: 'Disponible', value: 'habilitado' },
			{ text: 'Actions', value: 'actions', sortable: false },
		],
		listadoBuses: [],
		listadoChoferes: [],

		/* Index elemento seleccionado y/o flag para editar elemento */
		editedIndex: -1,

		/* Objetos temporales y por defecto */
		/* Se utilizan estos objs para almacenar los valores de los modals y/o asignar los valores correspondientes */

		objBus: {
			patente: '',
			chofer_asignado: '',
			disponible: true,
		},

		defaultItem: {
			patente: '',
			chofer_asignado: '',
			disponible: true,
		},
	}),

	computed: {
		formTitle() {
			return this.editedIndex === -1 ? 'Nuevo Chofer' : 'Editar Chofer';
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
		this.listarBuses();
		this.listarChoferes();
	},

	methods: {
		/* Funcion que lista todos los buses que estan registrados */
		async listarBuses() {
			let peticion = await axios.get('http://localhost:8000/api/buses/');
			if (peticion.status == 200) {
				let buses = peticion.data.map((bus) => ({
					id: bus.id,
					disponible: bus.disponible,
					habilitado: this.asignaEstado(bus),
					patente: bus.patente,
					chofer_asignado: bus.chofer_asignado,
					conductor: bus.chofer_asignado.nombre + ' ' + bus.chofer_asignado.apellido,
				}));

				this.listadoBuses = buses;
			} else {
				this.muestraMensajeError(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, ha ocurrido un error al buscar el listado de elementos, favor intente más tarde',
					'Error'
				);
			}
		},

		/*
			Funcion que trae todos los choferes registrados que se encuentren habilitados
			OBS: Se deja un try catch por si ocurre algun error en el ciclo
		*/
		async listarChoferes() {
			try {
				let peticion = await axios.get('http://localhost:8000/api/choferes/');
				peticion.status == 200
					? (this.listadoChoferes = peticion.data.filter((chofer) => chofer.disponible == true))
					: this.muestraMensajeError(
							'error',
							'mdi-cloud-alert',
							'Estimado Usuario, ha ocurrido un error favor comunicarse con el administrador',
							'Error'
					  );
			} catch (error) {
				this.muestraMensajeError(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, ha ocurrido un error favor comunicarse con el administrador',
					'Error'
				);
			}
		},

		/*
			Funcion que almacena registros de buses
			OBS: Se deja un try catch por si ocurre algun error en el ciclo
		*/
		async guardarBus() {
			if (this.$refs.form.validate()) {
				let resultado = this.listadoBuses.find((bus) => bus.patente == this.objBus.patente);
				this.objBus.chofer_asignado = this.objBus.chofer_asignado.id;
				if (resultado != undefined) {
					this.muestraMensajeError(
						'error',
						'mdi-cloud-alert',
						'Estimado Usuario, se le informa que el registro ya se encuentra almacenado',
						'Error'
					);
				} else {
					let guardarRegisto = await axios.post('http://localhost:8000/api/buses/', this.objBus);
					if (guardarRegisto.status == 201) {
						this.muestraMensajeError(
							'success',
							'mdi-check-all',
							'Estimado Usuario, se le informa que el registro se ha almacenado correctamente',
							'Correcto'
						);
					} else {
						this.muestraMensajeError(
							'error',
							'mdi-cloud-alert',
							'Estimado Usuario, se le informa que ha ocurrido un error al intentar almacenar el registro, favor intente nuevamente',
							'Error'
						);
					}
				}
				this.close();
			} else {
				this.$refs.form.validate();
			}
		},
		/* Funcion que cierra la ventana modal de las modificaciones / agregar */
		close() {
			this.dialog = false;
			this.$nextTick(() => {
				this.objBus = Object.assign({}, this.defaultItem);
				this.editedIndex = -1;
			});
			this.$refs.form.resetValidation();
			this.listarBuses();
		},

		editItem(item) {
			this.mostrarMensaje = false;
			this.editedIndex = this.listadoBuses.indexOf(item);
			this.objBus = Object.assign({}, item);
			this.dialog = true;
		},

		muestraMensajeError(tipo, icono, texto, cabecera) {
			this.mostrarMensaje = true;
			this.tipo = tipo;
			this.icono = icono;
			this.texto = texto;
			this.cabecera = cabecera;
		},

		async actualizarBus() {
			if (this.$refs.form.validate()) {
				this.objBus.chofer_asignado = this.objBus.chofer_asignado.id;
				let actualizarRegisto = await axios.put(
					`http://localhost:8000/api/buses/${this.objBus.id}/`,
					this.objBus
				);
				actualizarRegisto.status == 200
					? this.muestraMensajeError(
							'success',
							'mdi-check-all',
							'Estimado Usuario, se le informa que el registro se ha actualizado correctamente',
							'Correcto'
					  )
					: this.muestraMensajeError(
							'error',
							'mdi-cloud-alert',
							'Estimado Usuario, se le informa que ha ocurrido un error al intentar actualizar el registro, favor intente nuevamente',
							'Error'
					  );
				this.close();
			} else {
				this.$refs.form.validate();
			}
		},

		asignaEstado(obj) {
			let respuesta = obj.disponible ? 'SI' : 'NO';
			respuesta = obj.chofer_asignado.disponible ? respuesta : 'Chofer no disponible';
			return respuesta;
		},
	},
};
</script>
