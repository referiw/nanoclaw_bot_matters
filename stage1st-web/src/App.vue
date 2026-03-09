<template>
  <router-view />
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar'

const $q = useQuasar()

// 监听系统主题变化
$q.dark.set('auto')
</script>
