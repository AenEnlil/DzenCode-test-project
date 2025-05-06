<template>
    <form @submit.prevent="handleSubmit" class="comment-form">
        <div>
            <label>Email: </label>
            <input type="email" v-model="form.email" required />
        </div>
        <div>
            <label>Username: </label>
            <input type="text" v-model="form.username" required />
        </div>
        <div>
            <label>Homepage </label>
            <input type="url" v-model="form.homepage" placeholder="https://example.com" />
        </div>
        <div>
            <label>Text </label>
            <input type="text" v-model="form.text" required />
        </div>
        <button type="submit"> Отправить </button>
    </form>
</template>

<script>
    export default {
      name: 'CommentForm',
      props: {
        onSubmit: Function
      },
      data() {
        return {
          form: {
            email: '',
            username: '',
            homepage: '',
            text: ''
          }
        }
      },
      methods: {
        handleSubmit() {
          if (this.onSubmit) {
            this.onSubmit({...this.form})
          }
          this.clearForm()
        },

        clearForm() {
          this.form = {
            email: '',
            username: '',
            homepage: '',
            text: ''
          }
        },
      },
    }
</script>

<style scoped>
    .comment-form {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
    }
    .comment-form input, .comment-form textarea {
      padding: 6px;
      width: 100%;
    }
</style>
