
<template>
 <div>
  <SiteHeader />
  <router-view />
 </div>
</template>

<script>
import SiteHeader from '@/components/Header.vue'

export default {
    components: {
        SiteHeader
    }
}
</script>
