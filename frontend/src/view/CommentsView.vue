<template>
 <div>
  <div v-if="loading"><Loader /></div>
  <div v-else-if="error">{{ error }}</div>
  <div v-else>
   <div v-if="comments_count === 0">
    <p class="no-comments-text">there is no comments yet, but you can...</p>
    <div class="create-comment-button">
      <button @click="showModalWithForm">Create comment</button>
     </div>
   </div>
   <div v-else>
     <table class="comments-table">
      <thead class="comments-table-header">
       <tr>
         <th class="sortable" @click="sortBy('email')">Email
          <span class="arrow" :class="sortedBy === 'email' ? (sortOrder === 'asc' ? 'up' : 'down') : ''"></span>
         </th>
         <th class="sortable" @click="sortBy('username')">Username
           <span class="arrow" :class="sortedBy === 'username' ? (sortOrder === 'asc' ? 'up' : 'down') : ''"></span>
         </th>
         <th>Homepage</th>
         <th>Text</th>
         <th class="sortable" @click="sortBy('created_at')">Date
          <span class="arrow" :class="sortedBy === 'created_at' ? (sortOrder === 'asc' ? 'up' : 'down') : ''"></span>
        </th>
       </tr>
   </thead>
      <tbody>
        <tr v-for="comment in comments" :key="comment.id" @click="goToComment(comment.id)">
         <td class="email-cell" :title="getTooltip(comment.email, 40)"> {{ getPreview(comment.email, 40) }} </td>
         <td class="username-cell" :title="getTooltip(comment.username, 40)"> {{ getPreview(comment.username, 40) }} </td>
         <td class="homepage-cell" :title="getTooltip(comment.homepage, 60)"> {{ getPreview(comment.homepage, 60) }} </td>
         <td class="text-cell" :title="getTooltip(comment.text, 300)"> {{ getPreview(comment.text, 300) }} </td>
         <td class="date-cell"> {{ formatDate(comment.created_at) }} </td>
        </tr>
      </tbody>
  </table>
     <div class="buttons">
         <div class="pagination">
            <button :disabled="!previous_page" @click="goToPreviousPage"> Back </button>
            <button :disabled="!next_page" @click="goToNextPage"> Next</button>
         </div>
         <div v-if="showNewCommentNotification" class="notification">
            New comment available ({{newCommentsCount}})
            <button @click="reloadTable">Обновить</button>
        </div>
         <div class="create-comment-button">
            <button @click="showModalWithForm">Create comment</button>
         </div>
     </div>
   </div>
  </div>
  <div v-if="showModal" class="modal-overlay">
   <div class="modal-content">
      <CommentForm :onSubmit="createComment" @cancel="showModal = false"/>
   </div>
    </div>
 </div>
</template>

<script>
 import axios from 'axios'
 import api from '@/services/api.js'
 import { toRaw } from 'vue'
 import { API_BASE_URL, PAGE_SIZE, WS_BASE_URL } from '@/config'
 import { formatDate } from '@/service.js'
 import { subscribeWS, unsubscribeWS } from '@/services/websocket.js'
 import CommentForm from '@/components/CommentForm.vue'
 import Loader from '@/components/Loader.vue'
 export default {
    name: 'CommentsTable',
    components: {
     CommentForm,
     Loader
    },
    data() {
        return {
            comments: [],
            sortedBy: 'created_at',
            sortOrder: 'desc',
            loading: true,
            error: null,
            next_page: null,
            previous_page: null,
            comments_count: null,
            currentPage: 1,
            showModal: false,
            showNewCommentNotification: false,
            newCommentsCount: 0
        }
    },
    mounted() {
        this.fetchComments()
        subscribeWS(this.handleWSMessage)
    },
    beforeUnmount() {
        unsubscribeWS(this.handleWSMessage)
    },

    methods: {
        async fetchComments({ url=null, query={} } = {}) {
         var url = url ? url : '/comments/'

         try {
          const response = await api.get(url, {params: query})
          this.comments = response.data.results
          this.comments_count = response.data.count
          this.next_page = response.data.next
          this.previous_page = response.data.previous
          this.loading = false }
         catch (error) {
          console.error('error') }
        },

        showModalWithForm() {
          this.showModal = true
        },

        handleWSMessage(event_data) {
            if (event_data.type == "new_comment" && !event_data.data.parent) {
                if (this.sortedBy == 'created_at' && this.sortOrder == 'desc' && !this.previous_page) {
                    this.comments.unshift(event_data.data)
                } else {
                    this.showNewCommentNotification = true
                    this.newCommentsCount += 1
                }
            }
        },
        reloadTable() {
            this.showNewCommentNotification = false
            this.newCommentsCount = 0
            var params = this.getSortParams()
            this.fetchComments({ query: params })
        },

        isTooLong(text, limit) {
        if (text) {
         return text.length > limit
        }
        else {return false}
        },

        getTooltip(text, limit) {
         return this.isTooLong(text, limit) ? text : null
        },

        getPreview(text, limit) {
         if (this.isTooLong(text, limit)) {
          return text.slice(0, limit) + '...' }
         else {
          return text }
        },

        formatDate,

        getSortParams() {
         var order_field = this.sortedBy
         var order_param = this.sortOrder === 'asc' ? order_field : '-' + order_field
         return {ordering: order_param}
        },

        sortBy(key) {
         var current_sorted = this.sortedBy
         if (key === current_sorted){
          this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc' }
         else {
          this.sortedBy = key
          this.sortOrder = 'asc' }
         var params = this.getSortParams()
         this.fetchComments({ query: params })
        },

        loadPage(page_number) {
         this.currentPage = page_number
         console.log(page_number, this.currentPage)
        },

        goToNextPage() {
         if (this.next_page) {
          this.fetchComments({url: this.next_page})
         }
        },

        goToPreviousPage() {
         if (this.previous_page) {
          this.fetchComments({url: this.previous_page})
         }
        },

        async createComment(formData) {
          formData.parent = null

          try {
            await api.post('/comments/', formData)
            this.showModal = false
          } catch (error) {
            if (error.response && error.response.data) {
              return Promise.reject(error.response.data)
            }
            console.log("Error while creating comment", error)
            }
        },

        goToComment(id) {
          this.$router.push(`/comments/${id}`)
        },

    },
    computed: {
     totalPages() {
      return Math.ceil(this.comments_count / PAGE_SIZE)
     }
    }
 };
</script>


<style scoped>
 .comments-table {
   width: 100%;
   table-layout: fixed;
   border-collapse: collapse;
 }

 .comments-table th, .comments-table td {
   width: 300px;
   padding: 8px, 12px;
   border: 1px solid #ccc;
   text-align: center;
   overflow: hidden;
   text-overflow: ellipsis;
   white-space: break-word;
 }
th:nth-child(1),
td:nth-child(1){
   width: 200px; /* email */
 }
th:nth-child(2),
td:nth-child(2){
   width: 200px; /* username */
 }
th:nth-child(3),
td:nth-child(3){
   width: 250px; /* homepage */
 }
th:nth-child(4),
td:nth-child(4){
   width: 600px; /* text */
 }
th:nth-child(5),
td:nth-child(5){
   width: 200px; /* data */
 }

.comments-table-header th {
  font-family: Lato-Bold;
  font-size: 18px;
  color: #fff;
  background-color: #6c7ae0;
  padding-top: 18px;
  padding-bottom: 18px;
  text-align: center;
}

.comments-table-header th.sortable {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.comments-table-header th.sortable:hover {
  background-color: #f0f0f0;
  color: #6c7ae0;
}

 .text-cell:hover, .email-cell:hover, .username-cell:hover, .homepage-cell:hover {
    box-shadow: inset 0 4px 6px -2px rgba(0,0,0,0.2);
 }

 tbody td {
  cursor: pointer;
 }

 tbody tr:hover {
   box-shadow: 0 4px 6px -2px rgba(0,0,0,0.2);
 }

 .arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.up {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 7px solid currentColor;
}

.arrow.down {
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 7px solid currentColor;
}

.pagination {
    display: flex;
    gap: 7px;
}

.pagination button:disabled {
    background-color: white;
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

button {
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
  position: relative;
  text-align: center;
  text-decoration: none;
  vertical-align: middle;
  white-space: nowrap;
}

.buttons {
    display: flex;
    margin-top: 10px;
    justify-content: space-between;
}

button:hover {
  background-color: #6c7ae0;
}

.create-comment-button {
    margin-right: 10px;
}

.no-comments-text{
    margin-bottom: 10px;
}

.notification {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    text-transform: uppercase;
    font-family: 'Montserrat';
    font-weight: 600;
}

</style>
