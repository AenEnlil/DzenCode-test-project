<template>
    <div v-if="visible" class="modal-overlay" @click="close">
        <div class="modal-content" @click.stop>
            <template v-if="isImage(file)">
                <img :src="file" alt="file not found"></img>
            </template>
            <template v-else>
                <p>
                    File:
                    <a :href="file" target="_blank" rel="noopener noreferrer">{{getFileName(file)}}</a>
                </p>
            </template>
            <button class="close-button" @click="close">Close</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FilePreviewModal',
    props: {
        file: String,
        visible: Boolean
    },
    emits: ['close'],
    methods: {
        close() {
            this.$emit('close')
        },
        isImage(url) {
            return /\.(jpg|jpeg|png|gif)$/i.test(url)
        },
        getFileName(url) {
            return url?url.split('/').pop() : ''
        }
    }
}
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 6px;
    max-width: 90%;
    max-height: 90%;
    overflow: auto;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
.modal-content img {
    max-width: 100%;
    height: auto;
}
.close-button {
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

.close-button:hover {
   background-color: #6c7ae0;
}

</style>
