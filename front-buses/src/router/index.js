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
	{
		path: '/administracion',
		name: 'administracion',
		component: () => import('../views/Administracion.vue'),
	},
];

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
});

export default router;
