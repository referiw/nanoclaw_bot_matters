<template>
  <div class="app">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="logo">
        <span class="logo-icon">⛰️</span>
        <span class="logo-text">中华名山图志</span>
      </div>
      <div class="stats">
        <span class="stat-item">
          <span class="stat-number">{{ visitedCount }}</span>
          <span class="stat-label">已登</span>
        </span>
        <span class="stat-item">
          <span class="stat-number">{{ mountains.length }}</span>
          <span class="stat-label">名山</span>
        </span>
        <span class="stat-number progress">{{ progressPercent }}%</span>
      </div>
      <button class="reset-btn" @click="resetVisited" v-if="visitedCount > 0">
        重置记录
      </button>
    </header>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 地图区域 -->
      <div class="map-container">
        <div ref="mapContainer" class="map"></div>

        <!-- 分类图例 -->
        <div class="legend">
          <h4>分类图例</h4>
          <div class="legend-items">
            <div class="legend-item" v-for="(icon, cat) in categoryIcons" :key="cat">
              <span class="legend-icon">{{ icon }}</span>
              <span class="legend-label">{{ cat }}</span>
            </div>
          </div>
        </div>

        <!-- 难度图例 -->
        <div class="difficulty-legend">
          <h4>难度等级</h4>
          <div class="difficulty-items">
            <div class="difficulty-item" v-for="(color, level) in difficultyColors" :key="level">
              <span class="difficulty-dot" :style="{ background: color }"></span>
              <span class="difficulty-label">{{ level }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 侧边栏 -->
      <aside class="sidebar" :class="{ open: selectedMountain }">
        <!-- 搜索和筛选 -->
        <div class="filter-section">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索名山..."
            class="search-input"
          />
          <div class="filter-tabs">
            <button
              v-for="cat in categories"
              :key="cat"
              :class="['filter-tab', { active: activeCategory === cat }]"
              @click="activeCategory = cat"
            >
              {{ cat === '全部' ? '全部' : categoryIcons[cat] + ' ' + cat }}
            </button>
          </div>
        </div>

        <!-- 山列表 -->
        <div class="mountain-list">
          <div
            v-for="m in filteredMountains"
            :key="m.id"
            class="mountain-card"
            :class="{ visited: isVisited(m.id), selected: selectedMountain?.id === m.id }"
            @click="selectMountain(m)"
          >
            <div class="card-header">
              <span class="mountain-icon">{{ categoryIcons[m.category] }}</span>
              <div class="mountain-info">
                <h3>{{ m.name }}</h3>
                <span class="mountain-alias">{{ m.alias }}</span>
              </div>
              <button
                class="visit-btn"
                :class="{ visited: isVisited(m.id) }"
                @click.stop="toggleVisited(m.id)"
              >
                {{ isVisited(m.id) ? '✓' : '+' }}
              </button>
            </div>
            <div class="card-meta">
              <span class="meta-item">
                <span class="meta-icon">📍</span>
                {{ m.province }} · {{ m.city }}
              </span>
              <span class="meta-item">
                <span class="meta-icon">📏</span>
                {{ m.elevation }}m
              </span>
              <span class="meta-item difficulty" :style="{ color: difficultyColors[m.difficulty] }">
                {{ m.difficulty }}
              </span>
            </div>
            <div class="card-footer">
              <span class="rating">⭐ {{ m.rating }}</span>
              <span class="best-time">最佳: {{ m.bestSeason }}</span>
            </div>
          </div>
        </div>

        <!-- 详情面板 -->
        <div class="detail-panel" v-if="selectedMountain">
          <button class="close-btn" @click="selectedMountain = null">×</button>
          <div class="detail-header">
            <span class="detail-icon">{{ categoryIcons[selectedMountain.category] }}</span>
            <div class="detail-title">
              <h2>{{ selectedMountain.name }}</h2>
              <span class="detail-alias">{{ selectedMountain.alias }}</span>
            </div>
            <button
              class="detail-visit-btn"
              :class="{ visited: isVisited(selectedMountain.id) }"
              @click="toggleVisited(selectedMountain.id)"
            >
              {{ isVisited(selectedMountain.id) ? '已登山 ✓' : '标记登顶' }}
            </button>
          </div>

          <div class="detail-meta">
            <div class="meta-tag">
              <span class="tag-icon">📍</span>
              {{ selectedMountain.province }} {{ selectedMountain.city }}
            </div>
            <div class="meta-tag">
              <span class="tag-icon">📏</span>
              海拔 {{ selectedMountain.elevation }}m
            </div>
            <div class="meta-tag" :style="{ borderColor: difficultyColors[selectedMountain.difficulty], color: difficultyColors[selectedMountain.difficulty] }">
              <span class="tag-icon">⚡</span>
              {{ selectedMountain.difficulty }}
            </div>
            <div class="meta-tag">
              <span class="tag-icon">⭐</span>
              {{ selectedMountain.rating }} 分
            </div>
          </div>

          <div class="detail-section">
            <h4>📖 简介</h4>
            <p>{{ selectedMountain.description }}</p>
          </div>

          <div class="detail-section">
            <h4>🎯 主要景点</h4>
            <div class="attractions">
              <span class="attraction-tag" v-for="a in selectedMountain.attractions" :key="a">
                {{ a }}
              </span>
            </div>
          </div>

          <div class="detail-section">
            <h4>🗓️ 登山建议</h4>
            <div class="tips-grid">
              <div class="tip-item">
                <span class="tip-icon">📅</span>
                <div class="tip-content">
                  <span class="tip-label">最佳季节</span>
                  <span class="tip-value">{{ selectedMountain.bestSeason }}</span>
                </div>
              </div>
              <div class="tip-item">
                <span class="tip-icon">⏱️</span>
                <div class="tip-content">
                  <span class="tip-label">建议时长</span>
                  <span class="tip-value">{{ selectedMountain.duration }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>💡 实用贴士</h4>
            <p class="tips-text">{{ selectedMountain.tips }}</p>
          </div>
        </div>
      </aside>
    </div>

    <!-- 统计面板 -->
    <div class="stats-panel" v-if="showStats">
      <div class="stats-content">
        <h3>我的登山统计</h3>
        <div class="stats-grid">
          <div class="stat-box">
            <span class="stat-value">{{ visitedCount }}</span>
            <span class="stat-label">已登名山</span>
          </div>
          <div class="stat-box">
            <span class="stat-value">{{ totalElevation }}</span>
            <span class="stat-label">累计海拔(m)</span>
          </div>
          <div class="stat-box">
            <span class="stat-value">{{ visitedProvinces.length }}</span>
            <span class="stat-label">涉足省份</span>
          </div>
        </div>
        <div class="province-stats">
          <h4>省份分布</h4>
          <div class="province-list">
            <div class="province-item" v-for="p in provinceStats" :key="p.name">
              <span class="province-name">{{ p.name }}</span>
              <div class="province-bar">
                <div class="province-fill" :style="{ width: p.percent + '%', background: provinceColors[p.name] || '#3498db' }"></div>
              </div>
              <span class="province-count">{{ p.count }}</span>
            </div>
          </div>
        </div>
        <button class="close-stats" @click="showStats = false">关闭</button>
      </div>
    </div>

    <!-- 统计按钮 -->
    <button class="stats-btn" @click="showStats = true">
      📊 我的战绩
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { mountains, provinceColors, categoryIcons, difficultyColors } from './data/mountains.js'

// 状态
const mapContainer = ref(null)
const map = ref(null)
const markers = ref({})
const selectedMountain = ref(null)
const searchQuery = ref('')
const activeCategory = ref('全部')
const visited = ref(new Set())
const showStats = ref(false)

// 从localStorage加载已访问记录
onMounted(() => {
  const saved = localStorage.getItem('visitedMountains')
  if (saved) {
    visited.value = new Set(JSON.parse(saved))
  }

  initMap()
})

// 保存到localStorage
watch(visited, (newVal) => {
  localStorage.setItem('visitedMountains', JSON.stringify([...newVal]))
}, { deep: true })

// 计算属性
const categories = computed(() => {
  const cats = ['全部', ...new Set(mountains.map(m => m.category))]
  return cats
})

const filteredMountains = computed(() => {
  let result = mountains
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(m =>
      m.name.includes(query) ||
      m.alias.includes(query) ||
      m.province.includes(query) ||
      m.city.includes(query)
    )
  }
  if (activeCategory.value !== '全部') {
    result = result.filter(m => m.category === activeCategory.value)
  }
  return result
})

const visitedCount = computed(() => visited.value.size)

const progressPercent = computed(() => {
  return Math.round((visitedCount.value / mountains.length) * 100)
})

const totalElevation = computed(() => {
  return mountains
    .filter(m => visited.value.has(m.id))
    .reduce((sum, m) => sum + m.elevation, 0)
})

const visitedProvinces = computed(() => {
  return [...new Set(
    mountains
      .filter(m => visited.value.has(m.id))
      .map(m => m.province)
  )]
})

const provinceStats = computed(() => {
  const stats = {}
  mountains.forEach(m => {
    if (!stats[m.province]) {
      stats[m.province] = { total: 0, visited: 0 }
    }
    stats[m.province].total++
    if (visited.value.has(m.id)) {
      stats[m.province].visited++
    }
  })
  return Object.entries(stats)
    .map(([name, data]) => ({
      name,
      count: data.visited,
      total: data.total,
      percent: Math.round((data.visited / data.total) * 100)
    }))
    .filter(p => p.count > 0)
    .sort((a, b) => b.count - a.count)
})

// 方法
function initMap() {
  // 创建地图，中心点在中国
  map.value = L.map(mapContainer.value, {
    center: [35, 105],
    zoom: 4,
    minZoom: 3,
    maxZoom: 10,
    zoomControl: false
  })

  // 添加地图图层 (使用高德地图瓦片)
  L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    attribution: '© 高德地图'
  }).addTo(map.value)

  // 添加缩放控制
  L.control.zoom({ position: 'bottomright' }).addTo(map.value)

  // 添加标记点
  mountains.forEach(m => addMarker(m))
}

function addMarker(mountain) {
  const isVisitedNow = visited.value.has(mountain.id)
  const color = isVisitedNow ? '#27ae60' : difficultyColors[mountain.difficulty]

  // 创建自定义图标
  const icon = L.divIcon({
    className: 'mountain-marker',
    html: `
      <div class="marker-wrapper ${isVisitedNow ? 'visited' : ''}" style="--marker-color: ${color}">
        <div class="marker-icon">${categoryIcons[mountain.category]}</div>
        <div class="marker-pulse" style="background: ${color}"></div>
        <span class="marker-label">${mountain.name}</span>
      </div>
    `,
    iconSize: [40, 50],
    iconAnchor: [20, 50]
  })

  const marker = L.marker(mountain.coordinates, { icon })
    .addTo(map.value)
    .on('click', () => selectMountain(mountain))

  markers.value[mountain.id] = marker
}

function selectMountain(mountain) {
  selectedMountain.value = mountain
  map.value.setView(mountain.coordinates, 7, { animate: true })
}

function toggleVisited(id) {
  if (visited.value.has(id)) {
    visited.value.delete(id)
  } else {
    visited.value.add(id)
  }
  visited.value = new Set(visited.value) // 触发响应式更新

  // 更新标记点
  const mountain = mountains.find(m => m.id === id)
  if (mountain && markers.value[id]) {
    map.value.removeLayer(markers.value[id])
    addMarker(mountain)
  }
}

function isVisited(id) {
  return visited.value.has(id)
}

function resetVisited() {
  if (confirm('确定要清除所有登山记录吗？')) {
    visited.value = new Set()
    // 重新渲染所有标记
    Object.values(markers.value).forEach(marker => map.value.removeLayer(marker))
    markers.value = {}
    mountains.forEach(m => addMarker(m))
  }
}
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #0f0f23;
  color: #e0e0e0;
  overflow: hidden;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

/* 头部 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stats {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #4ade80;
}

.stat-label {
  font-size: 14px;
  color: #888;
}

.progress {
  font-size: 20px;
  color: #fbbf24;
  margin-left: 8px;
}

.reset-btn {
  padding: 8px 16px;
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.reset-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

/* 主内容 */
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 地图容器 */
.map-container {
  flex: 1;
  position: relative;
}

.map {
  width: 100%;
  height: 100%;
  background: #1a1a2e;
}

/* Leaflet 自定义样式 */
.leaflet-container {
  background: #1a1a2e;
}

.leaflet-tile {
  filter: brightness(0.7) saturate(0.8) hue-rotate(180deg) invert(1);
}

.mountain-marker {
  background: transparent !important;
  border: none !important;
}

.marker-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s;
}

.marker-wrapper:hover {
  transform: scale(1.2);
}

.marker-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: var(--marker-color);
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 2;
}

.marker-wrapper.visited .marker-icon {
  background: #27ae60;
  box-shadow: 0 0 12px rgba(39, 174, 96, 0.6);
}

.marker-pulse {
  position: absolute;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  opacity: 0.3;
  animation: pulse 2s ease-out infinite;
}

@keyframes pulse {
  0% { transform: scale(0.5); opacity: 0.5; }
  100% { transform: scale(1.5); opacity: 0; }
}

.marker-label {
  font-size: 11px;
  color: #fff;
  background: rgba(0, 0, 0, 0.7);
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  margin-top: 2px;
}

/* 图例 */
.legend, .difficulty-legend {
  position: absolute;
  background: rgba(15, 15, 35, 0.9);
  backdrop-filter: blur(10px);
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1000;
}

.legend {
  bottom: 80px;
  left: 16px;
}

.difficulty-legend {
  bottom: 80px;
  left: 180px;
}

.legend h4, .difficulty-legend h4 {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

.legend-items, .difficulty-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.legend-item, .difficulty-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.legend-icon {
  font-size: 14px;
}

.difficulty-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* 侧边栏 */
.sidebar {
  width: 380px;
  background: rgba(15, 15, 35, 0.95);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.filter-section {
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  margin-bottom: 12px;
}

.search-input::placeholder {
  color: #666;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-tab {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  color: #888;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.1);
}

.filter-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: #fff;
}

/* 山列表 */
.mountain-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.mountain-list::-webkit-scrollbar {
  width: 6px;
}

.mountain-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

.mountain-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.mountain-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.mountain-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.mountain-card.visited {
  border-color: rgba(39, 174, 96, 0.3);
  background: rgba(39, 174, 96, 0.05);
}

.mountain-card.selected {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.mountain-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.mountain-info {
  flex: 1;
}

.mountain-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 2px;
}

.mountain-alias {
  font-size: 12px;
  color: #888;
}

.visit-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  color: #888;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.visit-btn:hover {
  border-color: #4ade80;
  color: #4ade80;
}

.visit-btn.visited {
  background: #27ae60;
  border-color: #27ae60;
  color: #fff;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #888;
}

.meta-icon {
  font-size: 14px;
}

.difficulty {
  font-weight: 600;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.rating {
  color: #fbbf24;
}

.best-time {
  color: #666;
}

/* 详情面板 */
.detail-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 15, 35, 0.98);
  backdrop-filter: blur(10px);
  overflow-y: auto;
  padding: 20px;
  z-index: 10;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-icon {
  font-size: 36px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
}

.detail-title {
  flex: 1;
}

.detail-title h2 {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 4px;
}

.detail-alias {
  font-size: 14px;
  color: #888;
}

.detail-visit-btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: 2px solid #667eea;
  background: transparent;
  color: #667eea;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.detail-visit-btn:hover {
  background: rgba(102, 126, 234, 0.2);
}

.detail-visit-btn.visited {
  background: #27ae60;
  border-color: #27ae60;
  color: #fff;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}

.meta-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  font-size: 13px;
  color: #ccc;
}

.tag-icon {
  font-size: 14px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  font-size: 14px;
  color: #888;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-section p {
  font-size: 14px;
  line-height: 1.8;
  color: #ccc;
}

.attractions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.attraction-tag {
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  border-radius: 20px;
  font-size: 13px;
  color: #a5b4fc;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
}

.tip-icon {
  font-size: 24px;
}

.tip-content {
  display: flex;
  flex-direction: column;
}

.tip-label {
  font-size: 11px;
  color: #666;
}

.tip-value {
  font-size: 14px;
  color: #fff;
  font-weight: 600;
}

.tips-text {
  padding: 16px;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
  border-left: 3px solid #fbbf24;
  border-radius: 0 8px 8px 0;
  font-size: 14px;
  line-height: 1.8;
}

/* 统计面板 */
.stats-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.stats-content {
  background: rgba(15, 15, 35, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 32px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.stats-content h3 {
  font-size: 24px;
  text-align: center;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-box {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.stat-box .stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #4ade80;
  display: block;
}

.stat-box .stat-label {
  font-size: 12px;
  color: #888;
}

.province-stats h4 {
  font-size: 14px;
  color: #888;
  margin-bottom: 12px;
}

.province-list {
  max-height: 200px;
  overflow-y: auto;
}

.province-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.province-name {
  width: 60px;
  font-size: 13px;
  color: #ccc;
}

.province-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.province-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s;
}

.province-count {
  width: 30px;
  text-align: right;
  font-size: 13px;
  color: #888;
}

.close-stats {
  width: 100%;
  padding: 14px;
  margin-top: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.close-stats:hover {
  opacity: 0.9;
}

/* 统计按钮 */
.stats-btn {
  position: fixed;
  bottom: 24px;
  right: 420px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 25px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
}

.stats-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

/* 响应式 */
@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    right: 0;
    top: 0;
    bottom: 0;
    transform: translateX(100%);
    z-index: 500;
    transition: transform 0.3s;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .stats-btn {
    right: 24px;
  }

  .legend, .difficulty-legend {
    display: none;
  }
}
</style>
