<template>
    <div v-if="loading">Loading...</div>
    <div v-else class="comment">
        <div class="comment-header">
            <p>{{comment.id}}</p>
            <strong> {{comment.username}} </strong>
            <p>{{ formatDate(comment.created_at) }}</p>
            <svg v-if="comment.replies && comment.replies.length"
                 @click="toggleReplies"
                 xmlns="http://www.w3.org/2000/svg"
                 viewBox="0 -960 960 960"
                 fill="#FFFFFF"
                 :class="['toggle-icon', {active: repliesVisible}]"
            ><path d="M280-80q-50 0-85-35t-35-85q0-39 22.5-70t57.5-43v-334q-35-12-57.5-43T160-760q0-50 35-85t85-35q50 0 85 35t35 85q0 39-22.5 70T320-647v7q0 50 35 85t85 35h80q83 0 141.5 58.5T720-320v7q35 12 57.5 43t22.5 70q0 50-35 85t-85 35q-50 0-85-35t-35-85q0-39 22.5-70t57.5-43v-7q0-50-35-85t-85-35h-80q-34 0-64.5-10.5T320-480v167q35 12 57.5 43t22.5 70q0 50-35 85t-85 35Zm0-80q17 0 28.5-11.5T320-200q0-17-11.5-28.5T280-240q-17 0-28.5 11.5T240-200q0 17 11.5 28.5T280-160Zm400 0q17 0 28.5-11.5T720-200q0-17-11.5-28.5T680-240q-17 0-28.5 11.5T640-200q0 17 11.5 28.5T680-160ZM280-720q17 0 28.5-11.5T320-760q0-17-11.5-28.5T280-800q-17 0-28.5 11.5T240-760q0 17 11.5 28.5T280-720Z"/>
            </svg>
        </div>
        <div class="comment-body">
            <p> {{comment.text}} </p>
        </div>
        <div v-if="repliesVisible">
            <div v-if="comment.replies && comment.replies.length" class="replies">
                <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
            </div>
        </div>
        <div v-if="comment.has_replies && !loading" class="load-replies">
            <button @click="loadReplies(offsetQuery)">Show replies</button>
        </div>
    </div>

</template>

<script>
    import axios from 'axios'
    import { API_BASE_URL } from '@/config'
     import { formatDate } from '@/service.js'
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
                offsetQuery: {},
                repliesVisible: true
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

            formatDate,

            checkIfHasMoreReplies(linkToNextPage) {
                if (linkToNextPage) {
                    const parsedUrl = new URL(linkToNextPage);
                    const offset_value = parsedUrl.searchParams.get('offset')
                    this.offsetQuery = {offset: offset_value}
                } else {
                    this.comment.has_replies = false
                }

            },

            toggleReplies() {
                this.repliesVisible = !this.repliesVisible
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
    .toggle-icon {
        margin-top: 4px;
        height: 16px;
        cursor: pointer;
    }
    .toggle-icon.active {
        opacity: 1;
        fill: black;
    }
</style>