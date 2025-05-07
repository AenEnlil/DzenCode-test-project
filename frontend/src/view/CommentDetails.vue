<template>
    <div class="comment-details">
        <div v-if="loading">Loading...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else>
            <Comment :comment="comment" />
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import { API_BASE_URL } from '@/config'
    import Comment from '@/components/Comment.vue'
    export default {
        name: 'CommentDetails',
        components: { Comment },
        data() {
            return {
                comment: {},
                replies: [],
                loading: false,
                error: null,
            }
        },
        mounted() {
            this.fetchData()
        },
        methods: {
            async fetchData() {
                this.loading = true
                const id = this.$route.params.id
                try {
                    const commentRes = await axios.get(`${API_BASE_URL}/comments/${id}`)
                    this.comment = commentRes.data
                } catch (error) {
                    console.error(error)
                    this.error = 'Fail while loading comment or replies'
                } finally {
                    this.loading = false
                }
            },

        }
    }
</script>