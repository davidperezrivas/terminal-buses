import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home,
	},
	{
		path: '/about',
		name: 'About',
		component: () => import('../views/About.vue'),
	},
	{
		path: '/grid',
		name: 'grid',
		component: () => import('../views/Grid.vue'),
	},
	{
		path: '/botones',
		name: 'botones',
		component: () => import('../views/Botones.vue'),
	},
	{
		path: '/buses',
		name: 'buses',
		component: () => import('../views/Buses.vue'),
	},
	{
		path: '/chofer',
		name: 'chofer',
		component: () => import('../views/Chofer.vue'),
	},
	{
		path: '/pasajeros',
		name: 'pasajeros',
		component: () => import('../views/Pasajeros.vue'),
	},
	{
		path: '/trayectos',
		name: 'trayectos',
		component: () => import('../views/Trayectos.vue'),
	},
	{
		path: '/viajes',
		name: 'viajes',
		component: () => import('../views/Viajes.vue'),
	},
];

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
});

export default router;
