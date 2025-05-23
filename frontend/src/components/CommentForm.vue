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
            <div class="formatting-buttons">
                <button @click.prevent="wrapSelection('i')"><i>i</i></button>
                <button @click.prevent="wrapSelection('strong')"><strong>B</strong></button>
                <button @click.prevent="wrapSelection('a', 'href=# title=')"><a>a</a></button>
                <button @click.prevent="wrapSelection('code')"><code>code</code></button>
            </div>
            <label>Text </label>
            <input type="text" ref="textInput" v-model="form.text" required />
            <div v-if="errors.text">
                <ul>
                    <li v-for="(error, index) in errors.text" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Attach file: </label>
            <input type="file"  ref="fileInput" accept=".txt" @change="handleFileUpload"/>
            <div v-if="errors.file">
                <ul>
                    <li v-for="(error, index) in errors.file" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div>
            <label>Attach image: </label>
            <input type="file" ref="imageInput" accept="image/jpeg,image/png,image/gif" @change="handleImageUpload"/>
            <div v-if="errors.image">
                <ul>
                    <li v-for="(error, index) in errors.image" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <div class="captcha">
            <img :src="captchaImageSrc" @click="generateCaptcha" alt="captcha"></img>
            <canvas ref="canvas" width="150" height="50" style="display: none"></canvas>
            <input v-model="captchaInput" placeholder="Input captcha: " />
            <div v-if="errors.captcha">
                <ul>
                    <li v-for="(error, index) in errors.captcha" :key="index"> {{error}} </li>
                </ul>
            </div>
        </div>
        <button class="form-button" type="submit"> Отправить </button>
        <button class="form-button cancel" type="button" @click="$emit('cancel')"> Отмена </button>
    </form>
</template>

<script>
    export default {
      name: 'CommentForm',
      props: {
        onSubmit: Function,
        parent: Number
      },
      data() {
        return {
          form: {
            email: '',
            username: '',
            homepage: '',
            text: ''
          },
          errors: {},
          captchaInput: null,
          captchaImageSrc: null
        }
      },
      mounted() {
        this.generateCaptcha()
      },
      methods: {
        updateErrors({errors, field, data}) {
            if (!errors[field]) {
                errors[field] = [data]
            } else {
                errors[field].push(data)
            }
        },
        generateCaptcha() {
            const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ123456789'
            this.captchaCode = ''
            for (let i=0; i < 6; i++) {
                this.captchaCode += chars[Math.floor(Math.random() * chars.length)]
            }

            const canvas = this.$refs.canvas
            const ctx = canvas.getContext('2d')
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            // background
            ctx.fillStyle = '#f2f2f2'
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            for (let i = 0; i < 5; i++) {
                ctx.strokeStyle = this.getRandomColor()
                ctx.beginPath()
                ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height)
                ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height)
                ctx.stroke()
            }

            for (let i = 0; i < 30; i++) {
                ctx.fillStyle = this.getRandomColor()
                ctx.beginPath()
                ctx.arc(Math.random() * canvas.width, Math.random() * canvas.height, 1.5, 0, 2*Math.PI)
                ctx.fill()
            }


            ctx.font = '28px sans-serif'
            ctx.fillStyle = '#333'
            ctx.fillText(this.captchaCode, 10, 35)

            this.captchaImageSrc = canvas.toDataURL('image/png')
        },
        getRandomColor() {
            const r = Math.floor(Math.random() * 150)
            const g = Math.floor(Math.random() * 150)
            const b = Math.floor(Math.random() * 150)
            return `rgb(${r},${g},${b})`
        },
        checkCaptcha() {
            if (!this.captchaInput) {return false}
            const trimmed = this.captchaInput.trim().toUpperCase()
            if (trimmed.length === this.captchaCode.length) {
                return trimmed === this.captchaCode
            } else { return false}
        },

        wrapSelection(tag, attrs='') {
            const input = this.$refs.textInput
            const start = input.selectionStart
            const end = input.selectionEnd
            const selected = this.form.text.slice(start, end)
            const openTag = `<${tag}${attrs?' ' + attrs : ''}>`
            const closeTag = `</${tag}>`

            let currentText = input.value
            let newText
            if (selected) {
                newText = currentText.slice(0, start) + openTag + selected + closeTag + currentText.slice(end)
            } else {
                newText = currentText + openTag + closeTag
            }
            input.value = newText
            this.form.text = newText
        },

        validate() {
            const errors = {}

            if (!this.checkCaptcha()) {
                this.updateErrors({errors: errors, field: 'captcha', data: 'Captcha incorrect'})
                this.generateCaptcha()
            }

            if (this.form.text) {
                if (this.form.text.length > 1500) {
                    this.updateErrors({errors: errors, field: 'text', data: 'Text too big. Maximum size is 1500 characters'})
                } else if (this.form.text.trim() === '') {
                    this.updateErrors({errors: errors, field: 'text', data: 'field can`t blank'})
                }
            }

            if (this.form.email) {
                if (this.form.email.length > 254){
                    this.updateErrors({errors: errors, field: 'email', data: 'Email too big. Maximum size is 254 characters'})
                }
            }

            if (this.form.username) {
                if (!/^[a-zA-Z0-9]+$/.test(this.form.username)) {
                    this.updateErrors({errors: errors, field: 'username', data: 'Username can only contain Latin letters and numbers'})
                }
                if (this.form.username.length < 3) {
                    this.updateErrors({errors: errors, field: 'username', data: 'Username too small. Minimum size is 3 characters'})
                } else if (this.form.username.length > 60) {
                    this.updateErrors({errors: errors, field: 'username', data: 'Username too big. Maximum size is 60 characters'})
                }
            if (this.form.homepage) {
                if (this.form.homepage.length > 200) {
                     this.updateErrors({errors: errors, field: 'homepage', data: 'URL too big. Maximum size is 200 characters'})
                }
            }

            }
            this.errors = errors
            return Object.keys(this.errors).length === 0
        },

        async handleSubmit() {
            this.errors = {}
            if (!this.validate()){
                return
            }
            try {
                if (this.onSubmit) {
                    let payload
                    if (this.parent) {this.form.parent = this.parent}
                    if (this.form.file || this.form.image) {
                        payload = new FormData()
                        for (const key of Object.keys(this.form)) {
                            payload.append(`${key}`, this.form[key])
                        }
                    } else {
                        payload = {...this.form}
                    }
                    await this.onSubmit(payload)
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
        handleFileUpload(event) {
         const file = event.target.files[0]
         this.errors.file = null

         if (file && file.type === 'text/plain' && file.size <= 100 * 1024){
            this.form.file = file
         } else {
            this.form.file = null
            this.$refs.fileInput.value = ''
            this.updateErrors({errors: this.errors, field: 'file', data: 'Txt lower than 100KB only accepted'})
         }
        },
        resizeImage(file, maxWidth = 320, maxHeight = 240) {
          return new Promise((resolve, reject) => {
            const img = new Image()
            const reader = new FileReader()

            reader.onload = (e) => {
            img.src = e.target.result }

            img.onload = () => {
                let { width, height } = img;

                // Keeping proportions
                const scale = Math.min(maxWidth / width, maxHeight / height, 1);
                width = width * scale;
                height = height * scale

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height)

                canvas.toBlob((blob) => {
                if (blob) {
                    // Creating new file
                    const resizedFile = new File([blob], file.name, { type: file.type });
                    resolve(resizedFile);
                } else {
                    reject(new Error("Failed to compress image"))}
                }, file.type) }
                reader.onerror = reject;
                reader.readAsDataURL(file) })
        },

        async handleImageUpload(event) {
            const image = event.target.files[0]
            this.errors.image = null
            if(!image) {return}

            const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']

            if (!allowedTypes.includes(image.type)) {
              this.updateErrors({errors: this.errors, field: 'image', data: 'Only JPG, PNG, GIF allowed'})
              this.form.image = null
              this.$refs.imageInput.value = ''
              return
            }

            const resizedImage = await this.resizeImage(image)
            this.form.image = resizedImage
        }
      },
    }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    * {
        font-family: "Montserrat";
    }

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

    .form-button {
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

.form-button:hover {
  background-color: #6c7ae0;
}

form {
    width: 350px;
}

ul {
    list-style: none;
    padding: 0px;
    margin: 0px;
}

li {
    color: #b90d0d;
    font-size: 14px;
}

label {
    font-weight: 500;
}

.captcha {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

img {
    border: 1px solid #ccc;
    cursor: pointer;
    margin-bottom: 5px;
    width: 150px;
    height: 50px;
}

.formatting-buttons {
    display: flex;
    gap: 7px;
}

</style>
