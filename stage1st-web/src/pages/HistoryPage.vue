<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md text-primary">📅 历史战报</div>
    
    <q-card flat bordered class="q-mb-md">
      <q-card-section>
        <div class="row q-gutter-md items-center">
          <q-select v-model="selectedMonth" :options="monthOptions" label="选择月份" outlined dense style="min-width: 200px" />
          <q-btn color="primary" icon="search" label="搜索" @click="searchHistory" />
        </div>
      </q-card-section>
    </q-card>

    <div class="row q-col-gutter-md">
      <div v-for="report in historyReports" :key="report.id" class="col-12 col-sm-6 col-md-4">
        <q-card flat bordered class="cursor-pointer" @click="viewReport(report.id)">
          <q-card-section class="bg-primary text-white">
            <div class="text-h6">{{ report.title }}</div>
            <div class="text-caption">{{ report.date }}</div>
          </q-card-section>
          <q-card-section>
            <div class="text-body2 ellipsis-2-lines">{{ report.summary }}</div>
          </q-card-section>
          <q-separator />
          <q-card-actions>
            <q-chip dense color="blue" text-color="white">{{ report.postCount }} 帖</q-chip>
            <q-chip dense color="green" text-color="white">{{ report.keywordCount }} 关键词</q-chip>
            <q-space />
            <q-btn flat round icon="arrow_forward" color="primary" />
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedMonth = ref('2026年3月')
const monthOptions = ['2026年3月', '2026年2月', '2026年1月', '2025年12月']

const historyReports = ref([
  { id: 1, title: '3月10日战报', date: '2026-03-10', summary: '新能源领涨，市场情绪乐观...', postCount: 814, keywordCount: 25 },
  { id: 2, title: '3月9日战报', date: '2026-03-09', summary: '科技股调整，关注低估值板块...', postCount: 756, keywordCount: 22 },
  { id: 3, title: '3月8日战报', date: '2026-03-08', summary: '医药板块反弹，港股表现亮眼...', postCount: 689, keywordCount: 20 },
  { id: 4, title: '3月7日战报', date: '2026-03-07', summary: '美联储言论影响市场...', postCount: 723, keywordCount: 23 },
  { id: 5, title: '3月6日战报', date: '2026-03-06', summary: 'A股延续震荡格局...', postCount: 654, keywordCount: 19 },
  { id: 6, title: '3月5日战报', date: '2026-03-05', summary: '两会题材受关注...', postCount: 891, keywordCount: 28 }
])

function searchHistory() {
  console.log('Searching for:', selectedMonth.value)
}

function viewReport(id: number) {
  router.push(`/report/${id}`)
}
</script>
