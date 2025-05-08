<template>
    <form @submit.prevent="handleSubmit" class="comment-form">
        <div>
            <label>Email: </label>
            <input type="email" v-model="form.email" required />
            <div v-if="errors.email">
                <ul>
                    <li v-for="(error, index) in errors.email" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Username: </label>
            <input type="text" v-model="form.username" required />
            <div v-if="errors.username">
                <ul>
                    <li v-for="(error, index) in errors.username" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Homepage </label>
            <input type="url" v-model="form.homepage" placeholder="https://example.com" />
            <div v-if="errors.homepage">
                <ul>
                    <li v-for="(error, index) in errors.homepage" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Text </label>
            <input type="text" v-model="form.text" required />
            <div v-if="errors.text">
                <ul>
                    <li v-for="(error, index) in errors.text" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <button type="submit"> Отправить </button>
        <button type="button" @click="$emit('cancel')"> Отмена </button>
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
          },
          errors: {}
        }
      },
      methods: {
        async handleSubmit() {
            this.errors = {}
            try {
                if (this.onSubmit) {
                    await this.onSubmit({...this.form})
                }
                this.clearForm()
            } catch (serverErrors) {
                this.errors = serverErrors
            }
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
