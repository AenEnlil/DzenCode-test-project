<template>
    <div v-if="loading">Loading...</div>
    <div v-else class="comment">
        <div class="comment-body">
            <strong> {{comment.username}} </strong>
            <p> {{comment.text}} </p>
            <p>{{replies}}</p>
        </div>
        <div v-if="comment.replies && comment.replies.length" class="replies">
            <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
        </div>
        <div v-if="!repliesLoaded && !loading" class="load-replies">
            <button @click="loadReplies">Show replies</button>
        </div>
    </div>

</template>

<script>
    import axios from 'axios'
    import { API_BASE_URL } from '@/config'
    export default {
        name: 'Comment',
        props: {
            comment: {
                type: Object,
                required: true
            },
            replies: Object
        },
        data() {
            return {
                loading: false,
                repliesLoaded: false
            }
        },
        methods: {
            async loadReplies() {
                this.loading = true
                try {
                    const response = await axios.get(`${API_BASE_URL}/comments/${this.comment.id}/replies`)
                    if (!this.comment.replies) {
                        this.comment.replies = []}
                    this.comment.replies.push(...response.data.results);
                    this.repliesLoaded = true
                } catch(error) {
                    console.log(error)
                    console.error('Error while loading replies')
                } finally {
                    this.loading = false
                }
            }
        }
    }
</script>

<style>
    .comment {
        border-left: 2px solid #ddd;
        margin-left: 1rem;
        padding-left: 1rem;
        margin-top: 1rem;
    }
    .comment-body {
        background: #f9f9f9;
        padding: 0.5rem;
        border-radius: 4px;
    }
    .replies {
        margin-top: 0.5rem;
    }
    .load-replies button {
        margin-top: 0.5rem;
        font-size: 0.9rem;
        cursor: pointer
    }
</style>