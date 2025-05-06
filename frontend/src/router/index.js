import {createRouter, createWebHistory} from 'vue-router';
import CommentsView from '@views/CommentsView.vue';
import CommentDetails from '@views/CommentDetails.vue';

const routes = [
    { path: '/', redirect: '/comments' },
    { path: '/comments', name: 'Comments', component: CommentsView},
    { path: '/comments/:id', name: 'CommentDetails', component: CommentDetails }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
