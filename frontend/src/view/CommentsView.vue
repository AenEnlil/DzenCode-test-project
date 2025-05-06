<template>
 <div class="p-4">
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">{{ error }}</div>
  <div v-else>
   <div v-if="comments_count === 0">
    <p>no comments</p>
   </div>
   <table v-else>
   <thead>
    <tr>
     <th @click="sortBy('email')">Email
      <span class="arrow" :class="sortedBy === 'email' ? (sortOrder === 'asc' ? 'up' : 'down') : ''"></span>
     </th>
     <th @click="sortBy('username')">Username
      <span class="arrow" :class="sortedBy === 'username' ? (sortOrder === 'asc' ? 'up' : 'down') : ''"></span>
     </th>
     <th>Homepage</th>
     <th>Text</th>
     <th @click="sortBy('created_at')">Date
      <span class="arrow" :class="sortedBy === 'created_at' ? (sortOrder === 'asc' ? 'up' : 'down') : ''"></span>
     </th>
    </tr>
   </thead>
   <tbody>
    <tr v-for="comment in comments" :key="comment.id">
     <td> {{ comment.email }} </td>
     <td> {{ comment.username }} </td>
     <td> {{ comment.homepage }} </td>
     <td class="text-cell" :title="getTooltip(comment.text, 300)"> {{ getPreview(comment.text, 300) }} </td>
     <td> {{ comment.created_at }} </td>
    </tr>
   </tbody>
  </table>
  </div>
  <div class="pagination">
   <button :disabled="!previous_page" @click="goToPreviousPage"> Назад </button>
   <button :disabled="!next_page" @click="goToNextPage"> Вперед </button>
  </div>
 </div>
</template>

<script>
 import axios from 'axios'
 import { toRaw } from 'vue'
 import { API_BASE_URL, PAGE_SIZE } from '@/config'
 export default {
    name: 'CommentsTable',
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
            currentPage: 1
        }
    },
    mounted() {
        this.fetchComments()
    },
    methods: {
        async fetchComments({ url=null, query={} } = {}) {
         var url = url ? url : API_BASE_URL+'/comments/'

         try {
          const response = await axios.get(url, {params: query})
          this.comments = response.data.results
          this.comments_count = response.data.count
          this.next_page = response.data.next
          this.previous_page = response.data.previous
          this.loading = false }
         catch (error) {
          console.error('error') }
        },

        isTooLong(text, limit) {
         return text.length > limit
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
    },
    computed: {
     totalPages() {
      return Math.ceil(this.comments_count / PAGE_SIZE)
     }
    }
 };
</script>

<style scoped>
 table {
  width: 100%;
  border-collapse: collapse;
 }

 th, td {
  max-width: 250px;
  word-wrap: break-word;
  padding: 8px, 12px;
  border: 1px solid #ddd;
 }
 .text-cell {
  max-width: 600px;
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: help;
 }

 .text-cell:hover {
    box-shadow: 0 4px 6px -2px rgba(0,0,0,0.2);
 }

 .text-cell[title] {
  position: relative
 }

 .text-cell[title]:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  left: 0;
  background-color: #333;
  color: white;
  padding: 6px;
  border-radius: 4px;
  font-size: 14px;
  white-space: pre-wrap;
  max-width: 300px;
  width: max-content;
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
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #ff1515;
}

.arrow.down {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #ff1515;
}

.pagination {
  margin-top: 10px;
}

</style>
