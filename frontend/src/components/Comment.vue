<template>
    <div v-if="loading"><Loader /></div>
    <div v-else class="comment">
        <div class="comment-header">
            <p>{{comment.id}}</p>
            <p class="username"> {{comment.username}} </p>
            <svg v-if="comment.replies && comment.replies.length"
                 @click="toggleReplies"
                 xmlns="http://www.w3.org/2000/svg"
                 viewBox="0 -960 960 960"
                 fill="black"
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
            <div class="date-container">
                <p>{{ formatDate(comment.created_at) }}</p>
            </div>
        </div>
        <div class="comment-body">
            <p v-html='comment.text'></p>
            <div class="files" v-if="comment.image || comment.file">
                <div v-if="!imageLoaded" class="image-placeholder"> Loading...</div>
                    <img v-show="imageLoaded" :src="comment.image" alt="preview" class='thumb' @load="onImageLoad" @error="onImageError" @click="openPreview(comment.image)"></img>
                <div v-if="comment.file" class="file-preview" alt="" @click="openPreview(comment.file)">📎 {{ getFileName(comment.file) }}</div>
            </div>
            <FilePreviewModal :visible="showFileModal" :file="currentFileUrl" @close="closeFileModal" />
        </div>
        <div v-if="repliesVisible">
            <div v-if="comment.replies && comment.replies.length" class="replies">
                <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
            </div>
        </div>
        <div v-if="comment.has_replies && !loading" class="load-replies">
            <button class="replies-button" @click="loadReplies(offsetQuery)">Show replies</button>
        </div>
    </div>
    <div v-if="showModal" class="modal-overlay">
        <div class="modal-content">
            <CommentForm :onSubmit="createComment" :parent="comment.id" @cancel="showModal = false"/>
        </div>
    </div>

</template>

<script>
    import api from '@/services/api.js'
    import { WS_BASE_URL } from '@/config'
    import { subscribeWS, unsubscribeWS } from '@/services/websocket.js'
    import { formatDate } from '@/services/utils.js'
    import CommentForm from '@/components/CommentForm.vue'
    import Loader from '@/components/Loader.vue'
    import FilePreviewModal from '@/components/FilePreviewModal.vue'
    export default {
        name: 'Comment',
        props: {
            comment: {
                type: Object,
                required: true
            }
        },
        components: {
            CommentForm,
            Loader,
            FilePreviewModal
        },
        data() {
            return {
                loading: false,
                repliesLoaded: false,
                offsetQuery: {},
                repliesVisible: true,
                showModal: false,
                offsetShift: 0,
                haveNextPage: false,
                showFileModal: false,
                currentFileUrl: null,
                imageLoaded: false
            }
        },
        mounted() {
            subscribeWS(this.handleWSMessage)
        },
        beforeUnmount() {
            unsubscribeWS(this.handleWSMessage)
        },
        watch: {
            'comment.image'(newVal) {
                this.imageLoaded = false }
        },
        methods: {
            async loadReplies(query={}) {
                this.loading = true
                if (query.offset) {
                    // adding offset shift for correct loading if any replies where added to page through Websocket
                    query.offset += this.offsetShift
                    this.offsetShift = 0
                }
                try {
                    const response = await api.get(`/comments/${this.comment.id}/replies`,
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
            updateOffsetShift() {
                if (this.repliesLoaded && this.haveNextPage) {
                    this.offsetShift += 1
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

            openPreview(url) {
                this.showFileModal = true
                this.currentFileUrl = url
            },

            closeFileModal() {
                this.showFileModal = false
                this.currentFileUrl = null
            },
            getFileName(url) {
                return url.split('/').pop()
            },
            onImageLoad() {
                this.imageLoaded = true
            },
            onImageError() {
                this.imageLoaded = false
            },

            handleWSMessage(event_data) {
                if (event_data.type == 'new_comment' && event_data.data.parent) {
                    if (event_data.data.parent == this.comment.id) {
                       this.addReplies({data: [event_data.data], toStart: true})
                       // shift offset for pagination
                       this.updateOffsetShift()
                    }}
            },

            checkIfHasMoreReplies(linkToNextPage) {
                if (linkToNextPage) {
                    const parsedUrl = new URL(linkToNextPage);
                    const offset_value = Number(parsedUrl.searchParams.get('offset'))
                    this.offsetQuery = {offset: offset_value}
                    this.haveNextPage = true
                } else {
                    this.haveNextPage = false
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
                try {
                    const response = await api.post('/comments/', formData)
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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    .comment {
        width: 1000px;
        border-left: 2px solid #ddd;
        padding-left: 1rem;
        margin: 0 auto;
    }

     p {
        font-family: "Montserrat";
        font-optical-sizing: auto;
        font-weight: 400;
        font-style: normal;
        font-variation-settings:
        "wdth" 100;
    }

    .comment-header {
        margin-top: 15px;
        padding-left: 10px;
        background: #bfc7ff;
        height: 60px;
        gap: 15px;
        display: flex;
        align-items: center;
    }

    .date-container {
        margin-left: auto;
        margin-right: 10px;
    }

    .username {
        font-weight: bold;
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
        fill: #2770f5;
    }

    .modal-icon {
        fill: black;
}

    .button-icons:hover {
        fill: #2770f5;
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

.replies-button {
  background-color: #bfc7ff;
  border: 1px solid rgba(27, 31, 35, .15);
  border-radius: 6px;
  box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
  box-sizing: border-box;
  color: #444;
  cursor: pointer;
  display: inline-block;
  font-family: "Montserrat";
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  padding: 6px 16px;
  text-align: center;
  text-decoration: none;
  vertical-align: middle;
  white-space: nowrap;
}

.replies-button:hover {
  background-color: #6c7ae0;
}

strong {
    font-weight: bold;
}

.files {
    display: flex;
    align-items: flex-end;
    gap: 8px;
}

.thumb {
  max-height: 50px;
  max-width: 150px;
  cursor: pointer;
  margin-top: 0.5rem;
}

.file-preview {
  margin-top: 0.5rem;
  cursor: pointer;
  color: #007bff;
  display: inline-block;
  max-width: 100%;
}

.thumb:hover, .file-preview:hover {
    border: 2px solid #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

</style>