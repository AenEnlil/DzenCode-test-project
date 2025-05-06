import {createRouter, createWebHistory} from 'vue-router';
import CommentsView from '@views/CommentsView.vue';

const routes = [
    { path: '/comments', name: 'Comments', component: CommentsView}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
