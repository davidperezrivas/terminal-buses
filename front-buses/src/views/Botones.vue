<template>
	<v-container class="grey lighten-5">
		<v-row no-gutters>
			<v-col cols="12" md="6">
				<v-btn>Texto</v-btn>
				<v-btn color="primary" outlined>Texto</v-btn>

				<v-btn class="mx-2" fab dark color="primary">
					<v-icon dark>
						mdi-minus
					</v-icon>
				</v-btn>

				<v-btn icon text>
					<v-icon dark>
						mdi-minus
					</v-icon>
				</v-btn>

				<v-btn color="blue-grey" class="ma-2 white--text" @click="loader = 'loading3'">
					Upload
					<v-icon right dark>
						mdi-cloud-upload
					</v-icon>
				</v-btn>
			</v-col>
		</v-row>
	</v-container>
</template>
