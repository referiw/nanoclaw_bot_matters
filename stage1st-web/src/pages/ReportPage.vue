<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md text-primary">📋 战报详情</div>
    
    <q-card class="q-mb-md" flat bordered>
      <q-card-section class="bg-primary text-white">
        <div class="row items-center justify-between">
          <div>
            <div class="text-h6">{{ reportData.title }}</div>
            <div class="text-caption">{{ reportData.date }}</div>
          </div>
          <q-btn flat icon="share" label="分享" @click="shareReport" />
        </div>
      </q-card-section>
      
      <q-tabs v-model="activeTab" dense class="text-grey" active-color="primary" indicator-color="primary">
        <q-tab name="summary" icon="summarize" label="概要" />
        <q-tab name="keywords" icon="tag" label="关键词" />
        <q-tab name="posts" icon="article" label="帖子" />
        <q-tab name="advice" icon="lightbulb" label="建议" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="activeTab" animated>
        <q-tab-panel name="summary">
          <div class="text-body1 q-mb-md">{{ reportData.summary }}</div>
          <div class="row q-gutter-md">
            <q-chip color="primary" text-color="white" icon="forum">{{ reportData.postCount }} 帖子</q-chip>
            <q-chip color="secondary" text-color="white" icon="person">{{ reportData.userCount }} 用户</q-chip>
            <q-chip color="accent" text-color="white" icon="visibility">{{ reportData.viewCount }} 浏览</q-chip>
          </div>
        </q-tab-panel>

        <q-tab-panel name="keywords">
          <div class="q-gutter-sm">
            <q-chip v-for="(item, index) in reportData.keywords" :key="index" 
                    :color="getKeywordColor(index)" text-color="white" size="md">
              {{ item.word }} ({{ item.count }})
            </q-chip>
          </div>
        </q-tab-panel>

        <q-tab-panel name="posts">
          <q-list bordered separator>
            <q-item v-for="post in reportData.posts" :key="post.id" clickable v-ripple>
              <q-item-section avatar>
                <q-avatar color="primary" text-color="white">{{ post.author[0] }}</q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ post.author }}</q-item-label>
                <q-item-label caption lines="2">{{ post.content }}</q-item-label>
              </q-item-section>
              <q-item-section side top>
                <q-item-label caption>{{ post.time }}</q-item-label>
                <q-item-label caption>楼层 #{{ post.floor }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>

        <q-tab-panel name="advice">
          <q-card flat bordered class="bg-blue-1">
            <q-card-section>
              <div class="text-h6 text-blue-9">💡 AI 投资建议</div>
            </q-card-section>
            <q-card-section>
              <div class="text-body1">{{ reportData.aiAdvice }}</div>
            </q-card-section>
            <q-card-actions>
              <q-btn flat color="primary" icon="content_copy" label="复制" @click="copyAdvice" />
            </q-card-actions>
          </q-card>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar, copyToClipboard } from 'quasar'

const $q = useQuasar()
const activeTab = ref('summary')

const reportData = ref({
  title: 'Stage1st 每日战报',
  date: '2026年3月10日',
  summary: '今日论坛活跃度较高，主要讨论集中在A股市场走势、新能源板块机会以及科技股估值等方面。整体情绪偏向乐观，建议投资者保持关注。',
  postCount: 814,
  userCount: 156,
  viewCount: 12580,
  keywords: [
    { word: 'A股', count: 128 },
    { word: '新能源', count: 95 },
    { word: '半导体', count: 87 },
    { word: '医药', count: 72 },
    { word: '消费', count: 65 },
    { word: '科技', count: 58 },
    { word: '金融', count: 45 },
    { word: '港股', count: 38 }
  ],
  posts: [
    { id: 1, author: '股海老手', content: '今天大盘走势不错，新能源板块表现亮眼...', time: '09:30', floor: 1 },
    { id: 2, author: '价值投资', content: '半导体龙头业绩超预期，值得关注...', time: '10:15', floor: 2 },
    { id: 3, author: '技术派', content: '从技术面看，短期还有上涨空间...', time: '11:00', floor: 3 }
  ],
  aiAdvice: '根据今日论坛讨论分析，建议关注以下投资机会：1) 新能源板块持续火热，可关注龙头企业的长期价值；2) 半导体行业景气度回升，建议逢低布局；3) 医药板块估值合理，可适当配置。风险提示：短期波动风险，注意控制仓位。'
})

function getKeywordColor(index: number) {
  const colors = ['primary', 'secondary', 'accent', 'positive', 'warning', 'info', 'dark']
  return colors[index % colors.length]
}

function shareReport() {
  $q.notify({ type: 'positive', message: '链接已复制到剪贴板！' })
}

function copyAdvice() {
  copyToClipboard(reportData.value.aiAdvice)
  $q.notify({ type: 'positive', message: '已复制到剪贴板' })
}
</script>
