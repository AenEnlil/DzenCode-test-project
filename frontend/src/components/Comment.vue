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
                 :class="['button-icons', {active: repliesVisible}]"
            ><path d="M280-80q-50 0-85-35t-35-85q0-39 22.5-70t57.5-43v-334q-35-12-57.5-43T160-760q0-50 35-85t85-35q50 0 85 35t35 85q0 39-22.5 70T320-647v7q0 50 35 85t85 35h80q83 0 141.5 58.5T720-320v7q35 12 57.5 43t22.5 70q0 50-35 85t-85 35q-50 0-85-35t-35-85q0-39 22.5-70t57.5-43v-7q0-50-35-85t-85-35h-80q-34 0-64.5-10.5T320-480v167q35 12 57.5 43t22.5 70q0 50-35 85t-85 35Zm0-80q17 0 28.5-11.5T320-200q0-17-11.5-28.5T280-240q-17 0-28.5 11.5T240-200q0 17 11.5 28.5T280-160Zm400 0q17 0 28.5-11.5T720-200q0-17-11.5-28.5T680-240q-17 0-28.5 11.5T640-200q0 17 11.5 28.5T680-160ZM280-720q17 0 28.5-11.5T320-760q0-17-11.5-28.5T280-800q-17 0-28.5 11.5T240-760q0 17 11.5 28.5T280-720Z"/>
            </svg>
            <svg
                 @click="showModalWithForm"
                 xmlns="http://www.w3.org/2000/svg"
                 viewBox="0 -960 960 960"
                 fill="#FFFFFF"
                 class="button-icons modal-icon"
            ><path d="M760-200v-160q0-50-35-85t-85-35H273l144 144-57 56-240-240 240-240 57 56-144 144h367q83 0 141.5 58.5T840-360v160h-80Z"/>
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
    <div v-if="showModal" class="modal-overlay">
        <div class="modal-content">
            <CommentForm :onSubmit="createComment" @cancel="showModal = false"/>
        </div>
    </div>

</template>

<script>
    import axios from 'axios'
    import { API_BASE_URL } from '@/config'
    import { formatDate } from '@/service.js'
    import CommentForm from '@/components/CommentForm.vue'
    export default {
        name: 'Comment',
        props: {
            comment: {
                type: Object,
                required: true
            }
        },
        components: {
            CommentForm
        },
        data() {
            return {
                loading: false,
                repliesLoaded: false,
                offsetQuery: {},
                repliesVisible: true,
                showModal: false,
            }
        },
        methods: {
            async loadReplies(query={}) {
                this.loading = true
                try {
                    const response = await axios.get(`${API_BASE_URL}/comments/${this.comment.id}/replies`,
                                                     {params: query})
                    this.addReplies({data: response.data.results})
                    this.checkIfHasMoreReplies(response.data.next)
                    this.repliesLoaded = true
                } catch(error) {
                    console.error('Error while loading replies')
                } finally {
                    this.loading = false
                }
            },

            addReplies({data, toStart=false}) {
                if (!this.comment.replies) {
                        this.comment.replies = []}
                if (toStart) {
                    if (this.repliesLoaded || !this.comment.has_replies) {
                        this.comment.replies.unshift(...data)
                    }
                }
                else {
                    this.comment.replies.push(...data)
                }
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
            },

            showModalWithForm() {
                this.showModal = true
            },

            async createComment(formData) {
                formData.parent = this.comment.id

                try {
                    const response = await axios.post(API_BASE_URL+'/comments/', formData)
                    this.addReplies({data: [response.data], toStart: true})
                    this.showModal = false
                } catch (error) {
                    if (error.response && error.response.data) {
                        return Promise.reject(error.response.data)
                    }
                    console.log("Error while sending comment", error)
            }
        },

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
        background: #e3eaf0;
        height: 60px;
        gap: 5px;
        display: flex;
        align-items: center;
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
    .button-icons {
        margin-top: 4px;
        height: 16px;
        cursor: pointer;
    }
    .button-icons.active {
        opacity: 1;
        fill: black;
    }

    .modal-icon {
        fill: black;
}

    .button-icons:hover {
        fill: cornflowerblue;
    }

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .modal-content {
        background: white;
        padding: 20px;
        border-radius: 8px;
    }

</style>