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
						:items="listadoChoferes"
						item-key="nombre"
						class="elevation-25"
					>
						<template v-slot:top>
							<v-toolbar flat>
								<v-toolbar-title>Mantenedor Chofer</v-toolbar-title>
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
											Nuevo Chofer
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
														<v-col cols="12" sm="6" md="4">
															<v-text-field
																v-model="objChofer.nombre"
																:rules="nombreRules"
																label="Nombre"
																required
															></v-text-field>
														</v-col>
														<v-col cols="12" sm="6" md="4">
															<v-text-field
																v-model="objChofer.apellido"
																:rules="apellidoRules"
																label="Apellido"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="4">
															<v-text-field
																v-model="objChofer.run"
																:rules="rutRules"
																label="Rut"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="4">
															<v-text-field
																v-model="objChofer.email"
																:rules="emailRules"
																label="Email"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="4">
															<v-text-field
																v-model="objChofer.direccion"
																:rules="direccionRules"
																label="Direccion"
																required
															></v-text-field>
														</v-col>

														<v-col cols="12" sm="6" md="4">
															<v-text-field
																v-model="objChofer.telefono"
																:rules="telefonoRules"
																label="Telefono"
																required
															></v-text-field>
														</v-col>
														<v-col cols="12">
															<v-checkbox
																v-if="editedIndex >= 0"
																v-model="objChofer.disponible"
																label="¿Chofer Disponible?"
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
												@click="crearChofer"
											>
												Guardar Registro
											</v-btn>
											<v-btn
												v-if="editedIndex >= 0"
												color="orange darken-1"
												:disabled="!valid"
												outlined
												@click="actualizarChofer"
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
		direccionRules: [(v) => !!v || 'Campo Requerido'],
		telefonoRules: [
			(v) => !!v || 'Campo Requerido',
			(v) => /^[0-9]+/.test(v) || 'Favor ingresar solo números',
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
			{ text: 'RUN', value: 'run', align: 'start' },
			{ text: 'Nombre', value: 'nombre' },
			{ text: 'Apellido', value: 'apellido' },
			{ text: 'Email', value: 'email' },
			{ text: 'Direccion', value: 'direccion' },
			{ text: 'Telefono', value: 'telefono' },
			{ text: 'Disponible', value: 'habilitado' },
			{ text: 'Actions', value: 'actions', sortable: false },
		],
		listadoChoferes: [],

		/* Index elemento seleccionado y/o flag para editar elemento */
		editedIndex: -1,

		/* Objetos temporales y por defecto */
		/* Se utilizan estos objs para almacenar los valores de los modals y/o asignar los valores correspondientes */

		objChofer: {
			run: '',
			nombre: '',
			apellido: '',
			email: '',
			direccion: '',
			telefono: '',
			disponible: true,
		},

		defaultItem: {
			run: '',
			nombre: '',
			apellido: '',
			email: '',
			direccion: '',
			telefono: '',
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
		this.traeListadoChoferes();
	},

	methods: {
		/* Funcion que me trae de la api todos los choferes */
		async traeListadoChoferes() {
			let choferes = await axios.get('http://localhost:8000/api/choferes/');
			if (choferes.status == 200) {
				choferes.data.forEach((chofer) => {
					chofer.disponible ? (chofer.habilitado = 'Si') : (chofer.habilitado = 'No');
				});

				this.listadoChoferes = choferes.data;
			} else {
				this.muestraMensajeError(
					'error',
					'mdi-cloud-alert',
					'Estimado Usuario, ha ocurrido un error al buscar el listado de elementos, favor intente más tarde',
					'Error'
				);
			}
		},

		/* Funcion que cierra la ventana modal de las modificaciones / agregar */
		close() {
			this.dialog = false;
			this.$nextTick(() => {
				this.objChofer = Object.assign({}, this.defaultItem);
				this.editedIndex = -1;
			});
			this.$refs.form.resetValidation();
			this.traeListadoChoferes();
		},

		async crearChofer() {
			/* Funcion para almacenar un registro */
			if (this.$refs.form.validate()) {
				// Si el registro pasa validacion procederemos a revisar si el run se encuentra en los registros
				const resultado = this.listadoChoferes.find((chofer) => chofer.run === this.objChofer.run);
				if (resultado != undefined) {
					this.muestraMensajeError(
						'error',
						'mdi-cloud-alert',
						'Estimado Usuario, se le informa que el registro ya se encuentra almacenado',
						'Error'
					);
				} else {
					let guardarRegisto = await axios.post(
						'http://localhost:8000/api/choferes/',
						this.objChofer
					);

					guardarRegisto.status == 201
						? this.muestraMensajeError(
								'success',
								'mdi-check-all',
								'Estimado Usuario, se le informa que el registro se ha almacenado correctamente',
								'Correcto'
						  )
						: this.muestraMensajeError(
								'error',
								'mdi-cloud-alert',
								'Estimado Usuario, se le informa que ha ocurrido un error al intentar almacenar el registro, favor intente nuevamente',
								'Error'
						  );
				}

				this.close();
			} else {
				this.$refs.form.validate();
			}
		},

		async actualizarChofer() {
			if (this.$refs.form.validate()) {
				let actualizarRegisto = await axios.put(
					`http://localhost:8000/api/choferes/${this.objChofer.id}/`,
					this.objChofer
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

		editItem(item) {
			this.mostrarMensaje = false;
			this.editedIndex = this.listadoChoferes.indexOf(item);
			this.objChofer = Object.assign({}, item);
			this.dialog = true;
		},

		muestraMensajeError(tipo, icono, texto, cabecera) {
			this.mostrarMensaje = true;
			this.tipo = tipo;
			this.icono = icono;
			this.texto = texto;
			this.cabecera = cabecera;
		},
	},
};
</script>
