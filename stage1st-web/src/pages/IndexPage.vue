<template>
  <q-page class="q-pa-md index-page">
    <div class="hero">
      <h1 class="hero-title">S1 战报中心</h1>
      <p class="hero-subtitle">Stage1st 论坛中东局势专楼实时追踪</p>
    </div>

    <div class="quick-actions">
      <q-btn color="primary" size="lg" icon="newspaper" label="查看最新战报" to="/report" />
    </div>

    <div class="features">
      <div class="feature-card">
        <q-icon name="update" size="48px" color="primary" />
        <h3>实时更新</h3>
        <p>每日中午12点自动爬取最新帖子</p>
      </div>
      <div class="feature-card">
        <q-icon name="analytics" size="48px" color="secondary" />
        <h3>数据分析</h3>
        <p>关键词提取、用户活跃度统计</p>
      </div>
      <div class="feature-card">
        <q-icon name="smart_toy" size="48px" color="accent" />
        <h3>AI 分析</h3>
        <p>智能投资建议与风险评估</p>
      </div>
    </div>

    <div class="info-section">
      <h2>关于本项目</h2>
      <p>本项目自动爬取Stage1st论坛中东局势专楼(#2275908)的帖子内容，生成可视化战报。</p>
      <p>数据来源：Stage1st论坛 | 生成工具：Claude Code</p>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

onMounted(() => {
  $q.notify({
    type: 'info',
    message: '欢迎来到S1战报中心！',
    position: 'top',
    timeout: 2000
  })
})
</script>

<style scoped>
.index-page {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 20px;
  margin-bottom: 30px;
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  color: white;
  margin: 0 0 15px;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255,255,255,0.7);
  margin: 0;
}

.quick-actions {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.feature-card h3 {
  margin: 15px 0 10px;
  font-size: 1.2rem;
}

.feature-card p {
  color: #666;
  margin: 0;
}

.info-section {
  background: #f5f5f5;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
}

.info-section h2 {
  margin: 0 0 15px;
  color: #333;
}

.info-section p {
  color: #666;
  margin: 5px 0;
}
</style>
