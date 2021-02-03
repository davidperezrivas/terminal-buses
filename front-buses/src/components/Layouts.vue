<template>
	<v-app>
		<v-app-bar app>
			<v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
			<v-toolbar-title>Turismo Bus</v-toolbar-title>
		</v-app-bar>

		<v-navigation-drawer app v-model="drawer" temporary>
			<v-list-item>
				<v-list-item-content>
					<v-list-item-title class="title">
						Application
					</v-list-item-title>
					<v-list-item-subtitle>
						subtext
					</v-list-item-subtitle>
				</v-list-item-content>
			</v-list-item>
			<v-divider></v-divider>
			<v-list dense nav>
				<v-list-item v-for="item in items" :key="item.title" link :to="item.url">
					<v-list-item-icon>
						<v-icon>{{ item.icon }}</v-icon>
					</v-list-item-icon>

					<v-list-item-content>
						<v-list-item-title>{{ item.title }}</v-list-item-title>
					</v-list-item-content>
				</v-list-item>
			</v-list>
		</v-navigation-drawer>
		<v-main>
			<router-view></router-view>
		</v-main>
	</v-app>
</template>

<script>
export default {
	name: 'Layouts',

	data: () => ({
		items: [
			{ title: 'Administracion', icon: 'mdi-account', url: '/administracion' },
			{ title: 'Mantenedor Pasajeros', icon: 'mdi-account', url: '/pasajeros' },
			{ title: 'Mantenedor Buses', icon: 'mdi-bus', url: '/buses' },
			{ title: 'Mantenedor Trayectos', icon: 'mdi-wallet-travel', url: '/trayectos' },
			{ title: 'Mantenedor Chofer', icon: 'mdi-odnoklassniki', url: '/chofer' },
			{ title: 'Viajes', icon: 'mdi-wallet', url: '/' },
		],
		drawer: false,
	}),
};
</script>
