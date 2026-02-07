<template>
  <div class="px-6 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold">我的报告</h1>
      </div>
      <router-link
        to="/generate"
        class="btn btn-primary shadow-apple"
      >
        生成新报告
      </router-link>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="spinner w-10 h-10"></div>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
      <h3 class="text-xl font-semibold text-red-800 mb-2">
        获取失败
      </h3>
      <p class="text-red-700 mb-4">{{ error }}</p>
      <button
        @click="fetchReports"
        class="btn btn-primary"
      >
        重试
      </button>
    </div>

    <div v-else-if="reports.length === 0" class="card shadow-apple text-center py-12">
      <div class="text-textSecondary text-5xl mb-4">📄</div>
      <h3 class="text-xl font-semibold mb-2">
        暂无报告
      </h3>
      <p class="text-textSecondary mb-6">
        您还没有生成任何实验报告
      </p>
      <router-link to="/generate" class="btn btn-primary shadow-apple">
        立即生成
      </router-link>
    </div>

    <div v-else class="grid gap-6">
      <div
        v-for="(report, index) in reports"
        :key="report.id"
        class="card shadow-apple hover:shadow-apple-hover transition-all duration-300"
      >
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div class="flex-1">
            <router-link
              :to="`/reports/${report.id}`"
              class="group"
            >
              <h3 class="text-xl font-semibold mb-1 group-hover:text-primary transition-colors duration-300">
                {{ report.title || `报告 ${report.id}` }}
              </h3>
              <p class="text-sm text-textSecondary mb-2">
                {{ report.topic || '无描述' }}
              </p>
            </router-link>
            
            <div class="flex flex-wrap gap-2 text-xs">
              <span class="px-2 py-1 bg-primary/10 text-primary rounded-full">
                {{ report.status || '已完成' }}
              </span>
              <span class="px-2 py-1 bg-backgroundTertiary text-textSecondary rounded-full">
                创建于 {{ formatDate(report.created_at) }}
              </span>
              <span class="px-2 py-1 bg-backgroundTertiary text-textSecondary rounded-full">
                {{ report.word_count }} 字
              </span>
            </div>
          </div>

          <div class="mt-4 md:mt-0 flex gap-3">
            <router-link
              :to="`/reports/${report.id}`"
              class="btn btn-secondary"
            >
              查看
            </router-link>
            <button
              @click="handleDelete(report.id)"
              class="btn bg-red-100 text-red-800 hover:bg-red-200 active:bg-red-300 transition-colors duration-300"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页组件（如果需要） -->
    <!-- <div class="mt-8 flex justify-center">
      <nav class="flex items-center space-x-2">
        <button class="btn btn-secondary disabled:opacity-50">
          上一页
        </button>
        <button class="btn btn-primary">1</button>
        <button class="btn btn-secondary">2</button>
        <button class="btn btn-secondary">3</button>
        <button class="btn btn-secondary">下一页</button>
      </nav>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const reports = ref([])
const loading = ref(true)
const error = ref('')

onMounted(() => {
  fetchReports()
})

const fetchReports = async () => {
  loading.value = true
  error.value = ''

  try {
    // 从localStorage获取报告列表
    const storedReports = localStorage.getItem('reports')
    const reportsList = storedReports ? JSON.parse(storedReports) : []
    reports.value = reportsList
  } catch (err) {
    console.error('Error fetching reports:', err)
    error.value = '获取报告列表失败，请重试'
  } finally {
    loading.value = false
  }
}

const handleDelete = async (reportId) => {
  if (window.confirm('确定要删除此报告吗？')) {
    try {
      // 从localStorage删除报告，使用类型无关的比较
      const updatedReports = reports.value.filter(report => {
        const id1 = typeof report.id === 'string' ? parseInt(report.id) : report.id
        const id2 = typeof reportId === 'string' ? parseInt(reportId) : reportId
        return id1 !== id2
      })
      localStorage.setItem('reports', JSON.stringify(updatedReports))
      reports.value = updatedReports
    } catch (err) {
      console.error('Error deleting report:', err)
      error.value = '删除报告失败'
    }
  }
}

const formatDate = (dateString) => {
  if (!dateString) return new Date().toLocaleString()
  return new Date(dateString).toLocaleString()
}
</script>
