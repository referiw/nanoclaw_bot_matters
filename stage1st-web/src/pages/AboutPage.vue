<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md text-primary">ℹ️ 关于</div>
    
    <q-card flat bordered>
      <q-card-section class="bg-primary text-white">
        <div class="text-h6">Stage1st 战报中心</div>
      </q-card-section>
      <q-card-section>
        <p class="text-body1">
          这是一个基于 Stage1st 论坛数据的战报生成系统。系统会自动抓取指定帖子的讨论内容，
          分析关键词热度，生成每日战报，并提供AI投资建议。
        </p>
        <q-separator class="q-my-md" />
        <div class="text-h6 q-mb-sm">🚀 功能特点</div>
        <q-list>
          <q-item>
            <q-item-section avatar><q-icon color="primary" name="auto_awesome" /></q-item-section>
            <q-item-section>自动抓取论坛数据，每日更新</q-item-section>
          </q-item>
          <q-item>
            <q-item-section avatar><q-icon color="secondary" name="analytics" /></q-item-section>
            <q-item-section>关键词分析和词云生成</q-item-section>
          </q-item>
          <q-item>
            <q-item-section avatar><q-icon color="accent" name="smart_toy" /></q-item-section>
            <q-item-section>AI生成投资建议</q-item-section>
          </q-item>
          <q-item>
            <q-item-section avatar><q-icon color="positive" name="devices" /></q-item-section>
            <q-item-section>响应式设计，支持移动端</q-item-section>
          </q-item>
        </q-list>
        <q-separator class="q-my-md" />
        <div class="text-h6 q-mb-sm">🛠️ 技术栈</div>
        <div class="q-gutter-sm">
          <q-chip color="primary" text-color="white">Vue 3</q-chip>
          <q-chip color="secondary" text-color="white">Quasar</q-chip>
          <q-chip color="accent" text-color="white">TypeScript</q-chip>
          <q-chip color="positive" text-color="white">Pinia</q-chip>
          <q-chip color="warning" text-color="white">Netlify</q-chip>
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat color="primary" icon="code" label="GitHub" href="https://github.com/referiw/nanoclaw_bot_matters" target="_blank" />
        <q-btn flat color="primary" icon="forum" label="Stage1st" href="https://stage1st.com" target="_blank" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
</script>
