<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Stage1st 战报中心
        </q-toolbar-title>
        <q-btn flat round icon="dark_mode" @click="toggleDark">
          <q-tooltip>{{ $q.dark.isActive ? '亮色模式' : '暗色模式' }}</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above side="left" bordered>
      <q-list>
        <q-item-label header>导航</q-item-label>
        <q-item clickable v-ripple to="/" exact>
          <q-item-section avatar><q-icon name="home" /></q-item-section>
          <q-item-section>首页</q-item-section>
        </q-item>
        <q-item clickable v-ripple to="/history">
          <q-item-section avatar><q-icon name="history" /></q-item-section>
          <q-item-section>历史战报</q-item-section>
        </q-item>
        <q-item clickable v-ripple to="/about">
          <q-item-section avatar><q-icon name="info" /></q-item-section>
          <q-item-section>关于</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title class="text-center text-caption">
          Powered by Quasar & Vue 3 | 数据来源: Stage1st
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function toggleDark() {
  $q.dark.toggle()
}
</script>
