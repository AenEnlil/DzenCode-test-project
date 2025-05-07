<template>
    <div v-if="loading">Loading...</div>
    <div v-else class="comment">
        <div class="comment-header">
            <p>{{comment.id}}</p>
            <strong> {{comment.username}} </strong>
            <p>{{comment.created_at}}</p>
        </div>
        <div class="comment-body">
            <p> {{comment.text}} </p>
        </div>
        <div v-if="comment.replies && comment.replies.length" class="replies">
            <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
        </div>
        <div v-if="comment.has_replies && !loading" class="load-replies">
            <button @click="loadReplies(offsetQuery)">Show replies</button>
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
            }
        },
        data() {
            return {
                loading: false,
                repliesLoaded: false,
                offsetQuery: {}
            }
        },
        methods: {
            async loadReplies(query={}) {
                this.loading = true
                try {
                    const response = await axios.get(`${API_BASE_URL}/comments/${this.comment.id}/replies`,
                                                     {params: query})
                    this.addReplies(response.data.results)
                    this.checkIfHasMoreReplies(response.data.next)
                    this.repliesLoaded = true
                } catch(error) {
                    console.error('Error while loading replies')
                } finally {
                    this.loading = false
                }
            },

            addReplies(data) {
                if (!this.comment.replies) {
                        this.comment.replies = []}
                this.comment.replies.push(...data);
            },

            checkIfHasMoreReplies(linkToNextPage) {
                if (linkToNextPage) {
                    const parsedUrl = new URL(linkToNextPage);
                    const offset_value = parsedUrl.searchParams.get('offset')
                    this.offsetQuery = {offset: offset_value}
                } else {
                    this.comment.has_replies = false
                }

            }

        }
    }
</script>

<style>
    .comment {
        width: 1000px;
        border-left: 2px solid #ddd;
        margin-left: 1rem;
        padding-left: 1rem;
        margin-top: 1rem;
    }
    .comment-header {
        background: grey;
        gap: 5px;
        display: flex;
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