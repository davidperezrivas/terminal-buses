<template>
	<v-container class="grey lighten-5">
		<v-row no-gutters>
			<v-col cols="12" md="12">
				<v-card>
					<v-alert
						v-if="mostrarMensaje"
						dismissible
						text
						prominent
						:type="tipo"
						:icon="icono"
						border="left"
					>
						{{ texto }}
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
										<v-btn color="green darken-4" outlined class="mb-2" v-bind="attrs" v-on="on">
											<v-icon>mdi-bus </v-icon>
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
																:rules="patente"
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
																data-vv-name="Chofer"
																:rules="chofer"
																required
															></v-select>
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
												color="green darken-4"
												:disabled="!valid"
												outlined
												@click="actualizarRegistro"
											>
												Guardar Cambios
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
							<v-icon small @click="deleteItem(item)">
								mdi-delete
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
		patente: [
			(v) => !!v || 'Campo Requerido',
			(v) => (v && v.length < 10) || 'Campo no debe sobrepasar los 10 caracteres',
		],

		chofer: [(v) => !!v || 'Campo Requerido'],

		/* Modals */
		dialog: false,
		dialogDelete: false,

		/* Habilitado */
		checkbox: true,

		/* Mensajes y alertas */
		mostrarMensaje: false,
		tipo: '',
		icono: '',
		texto: '',

		/* Data tables */
		headers: [
			{ text: 'Patente', value: 'run', align: 'start' },
			{ text: 'Chofer Asignado', value: 'nombre' },
			{ text: 'Actions', value: 'actions', sortable: false },
		],

		/* Arrays elementos a utilizar */
		listadoChoferes: [],
		listadoBuses: [],

		/* Index elemento seleccionado y/o flag para editar elemento */
		editedIndex: -1,

		/* Objetos temporales y por defecto */
		/* Se utilizan estos objs para almacenar los valores de los modals y/o asignar los valores correspondientes */

		objBus: {
			patente: '',
			chofer_asignado: '',
		},

		defaultItem: {
			patente: '',
			chofer_asignado: '',
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
		this.traeBuses();
	},

	methods: {
		async traeListadoChoferes() {
			let choferes = await axios.get('http://localhost:8000/api/choferes/');
			choferes.status == 200
				? (this.listadoChoferes = choferes.data)
				: this.muestraMensajeError(
						'error',
						'mdi-cloud-alert',
						'Ha ocurrido un error al buscar el listado de los choferes'
				  );
		},

		muestraMensajeError(tipo, icono, texto) {
			this.mostrarMensaje = true;
			this.tipo = tipo;
			this.icono = icono;
			this.texto = texto;
		},

		async traeBuses() {
			let buses = await axios.get('http://localhost:8000/api/buses/');
			console.log('elemento almacenar', buses);
			buses.status == 200
				? (this.listadoBuses = buses.data)
				: this.muestraMensajeError(
						'error',
						'mdi-cloud-alert',
						'Ha ocurrido un error al buscar el listado de los buses'
				  );
		},

		editItem(item) {
			this.editedIndex = this.listadoBuses.indexOf(item);
			this.objBus = Object.assign({}, item);
			this.dialog = true;
		},

		deleteItem(item) {
			this.editedIndex = this.listadoBuses.indexOf(item);
			this.objBus = Object.assign({}, item);
			this.dialogDelete = true;
		},

		deleteItemConfirm() {
			this.listadoBuses.splice(this.editedIndex, 1);
			this.closeDelete();
		},

		close() {
			this.dialog = false;
			this.$nextTick(() => {
				this.objBus = Object.assign({}, this.defaultItem);
				this.editedIndex = -1;
			});
			this.$refs.form.resetValidation();
			this.traeBuses();
		},

		closeDelete() {
			this.dialogDelete = false;
			this.$nextTick(() => {
				this.objBus = Object.assign({}, this.defaultItem);
				this.editedIndex = -1;
			});
		},

		async actualizarRegistro() {
			/*
				Funcion utilizada para guardar y actualizar los choferes
				esta funcion se realizará dependiendo del campo iditedIndex
			*/
			try {
				if (this.$refs.form.validate()) {
					this.editedIndex > -1
						? await axios.put('http://localhost:8000/api/choferes/', this.objBus)
						: this.validaRegistrosRepetidos(this.objBus);
					this.close();
				} else {
					this.$refs.form.validate();
				}
			} catch (error) {
				this.muestraMensajeError(
					'error',
					'mdi-cloud-alert',
					'Ha ocurrido un error, favor corroborar los datos ingresados'
				);
				this.close();
			}
		},

		async validaRegistrosRepetidos(registroAlmacenar) {
			const resultado = this.listadoBuses.find((bus) => bus.patente === registroAlmacenar.patente);
			if (typeof resultado === 'undefined') {
				let respuesta = await axios.post('http://localhost:8000/api/buses/', registroAlmacenar);
				respuesta.status == 201
					? this.muestraMensajeError('success', 'mdi-check-all', 'Se ha creado el registro')
					: this.muestraMensajeError(
							'error',
							'mdi-cloud-alert',
							'Ha ocurrido un error, favor intentar nuevamente'
					  );
			} else {
				this.muestraMensajeError(
					'error',
					'mdi-cloud-alert',
					'Patente ya se encuentra registrado en el sistema'
				);
			}
		},
	},
};
</script>
