<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md text-primary">📊 Stage1st 战报中心</div>
    
    <q-card class="q-mb-md" flat bordered>
      <q-card-section>
        <div class="text-h6">实时战报</div>
        <div class="text-caption text-grey">每日中午12点自动更新</div>
      </q-card-section>
      <q-card-section>
        <q-btn color="primary" icon="refresh" label="查看最新战报" to="/report" />
        <q-btn flat color="secondary" icon="history" label="历史记录" to="/history" class="q-ml-sm" />
      </q-card-section>
    </q-card>

    <div class="row q-gutter-md">
      <div class="col-12 col-md-4">
        <q-card flat bordered>
          <q-card-section class="bg-primary text-white">
            <div class="text-h6">📈 今日统计</div>
          </q-card-section>
          <q-card-section>
            <q-list>
              <q-item>
                <q-item-section avatar><q-icon color="primary" name="forum" /></q-item-section>
                <q-item-section>
                  <q-item-label>帖子总数</q-item-label>
                  <q-item-label caption>{{ stats.totalPosts }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section avatar><q-icon color="positive" name="person" /></q-item-section>
                <q-item-section>
                  <q-item-label>参与用户</q-item-label>
                  <q-item-label caption>{{ stats.activeUsers }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section avatar><q-icon color="warning" name="local_fire_department" /></q-item-section>
                <q-item-section>
                  <q-item-label>热门话题</q-item-label>
                  <q-item-label caption>{{ stats.hotTopic }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-7">
        <q-card flat bordered>
          <q-card-section class="bg-secondary text-white">
            <div class="text-h6">🔥 热门关键词</div>
          </q-card-section>
          <q-card-section>
            <div class="q-gutter-sm">
              <q-chip v-for="keyword in hotKeywords" :key="keyword" color="primary" text-color="white" clickable>
                {{ keyword }}
              </q-chip>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <q-card class="q-mt-md" flat bordered>
      <q-card-section>
        <div class="text-h6">💡 AI 投资建议</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-banner class="bg-blue-1 text-blue-9" rounded>
          <template v-slot:avatar>
            <q-icon name="lightbulb" color="blue" />
          </template>
          {{ aiAdvice }}
        </q-banner>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const stats = ref({
  totalPosts: '814',
  activeUsers: '156',
  hotTopic: 'A股市场'
})

const hotKeywords = ref([
  'A股', '新能源', '半导体', '医药', '消费', '科技', '金融', '港股', '美股', '基金'
])

const aiAdvice = ref('根据近期论坛讨论热点，建议关注新能源和半导体板块的长期投资机会，同时注意控制仓位风险。')

onMounted(() => {
  $q.notify({
    type: 'info',
    message: '欢迎来到Stage1st战报中心！',
    position: 'top',
    timeout: 2000
  })
})
</script>
