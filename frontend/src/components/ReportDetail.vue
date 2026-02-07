<template>
  <div class="space-y-8 px-6 py-8">
    <!-- 报告头部 -->
    <div>
      <div class="flex flex-col md:flex-row justify-between items-start gap-6 mb-4">
        <div>
          <router-link
            to="/reports"
            class="text-primary font-medium hover:underline mb-4 inline-block transition-colors duration-300"
          >
            ← 返回报告列表
          </router-link>
          <h1 class="text-4xl font-bold mb-2">
            {{ report?.title || `报告 ${id}` }}
          </h1>
          <p class="text-textSecondary">
            创建于 {{ formatDate(report?.created_at) }}
          </p>
        </div>

        <div class="flex gap-3">
          <button
            @click="handleDownload"
            class="btn btn-secondary"
          >
            💾 下载
          </button>
          <button
            @click="handleDelete"
            class="btn bg-red-100 text-red-800 hover:bg-red-200 active:bg-red-300 transition-colors duration-300"
          >
            🗑️ 删除
          </button>
        </div>
      </div>

      <!-- 报告标签 -->
      <div class="flex flex-wrap gap-3 mb-6">
        <span class="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">
          {{ report?.status || '已完成' }}
        </span>
        <span class="px-3 py-1 bg-backgroundTertiary text-textSecondary rounded-full text-sm">
          ID: {{ id }}
        </span>
        <span class="px-3 py-1 bg-backgroundTertiary text-textSecondary rounded-full text-sm">
          {{ report?.word_count || 0 }} 字
        </span>
        <span class="px-3 py-1 bg-backgroundTertiary text-textSecondary rounded-full text-sm">
          更新于 {{ formatDate(report?.updated_at || report?.created_at) }}
        </span>
      </div>
    </div>

    <!-- 报告内容 -->
    <div class="card shadow-apple" v-if="report">
      <div class="p-6">
        <h2 class="text-2xl font-bold mb-4">报告内容</h2>
        <!-- 使用prose类并添加额外的表格样式 -->
        <div class="prose max-w-none" v-html="renderMarkdown(report.content)"></div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex justify-center gap-6">
      <router-link to="/reports" class="btn btn-secondary">
        返回报告列表
      </router-link>
      <router-link to="/generate" class="btn btn-primary shadow-apple">
        生成新报告
      </router-link>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="spinner w-10 h-10"></div>
    </div>

    <!-- 错误状态 -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
      <h3 class="text-xl font-semibold text-red-800 mb-2">
        获取失败
      </h3>
      <p class="text-red-700 mb-6">{{ error }}</p>
      <div class="flex justify-center gap-4">
        <button
          @click="fetchReport"
          class="btn btn-primary"
        >
          重试
        </button>
        <router-link to="/reports" class="btn btn-secondary">
          返回列表
        </router-link>
      </div>
    </div>

    <!-- 报告不存在 -->
    <div v-if="!report && !loading && !error" class="card text-center py-12">
      <div class="text-secondary text-5xl mb-4">🔍</div>
      <h3 class="text-xl font-semibold text-text mb-2">
        报告不存在
      </h3>
      <p class="text-secondary mb-6">
        该报告可能已被删除或ID错误
      </p>
      <router-link to="/reports" class="btn btn-primary">
        返回报告列表
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, getCurrentInstance } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const route = useRoute()
const router = useRouter()
const report = ref(null)
const loading = ref(true)
const error = ref('')

const id = ref(route.params.id)

// 配置marked支持GFM
onMounted(() => {
  marked.setOptions({
    gfm: true,
    breaks: true,
    headerIds: true,
    mangle: false
  })
  fetchReport()
})

watch(() => route.params.id, (newId) => {
  id.value = newId
  fetchReport()
})

const fetchReport = async () => {
  loading.value = true
  error.value = ''
  try {
    // 从localStorage获取报告列表
    const storedReports = localStorage.getItem('reports')
    
    const reports = storedReports ? JSON.parse(storedReports) : []
    
    // 根据URL参数查找对应的报告（同时尝试字符串和数字类型匹配）
    const foundReport = reports.find(report => 
      report.id === parseInt(id.value) || report.id === id.value
    )
    
    if (foundReport) {
      if (typeof foundReport.content === 'string') {
        report.value = foundReport
      } else {
        error.value = '报告内容格式错误'
        console.error('报告内容不是字符串:', foundReport.content)
      }
    } else {
      error.value = '未找到该报告'
    }
  } catch (err) {
    console.error('Error fetching report:', err)
    error.value = '获取报告详情失败'
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (window.confirm('确定要删除这个报告吗？')) {
    try {
      // 从localStorage删除报告
      const storedReports = localStorage.getItem('reports')
      const reports = storedReports ? JSON.parse(storedReports) : []
      // 使用类型无关的比较来查找报告
      const updatedReports = reports.filter(report => 
        report.id !== parseInt(id.value) && report.id !== id.value
      )
      localStorage.setItem('reports', JSON.stringify(updatedReports))
      router.push('/reports')
    } catch (err) {
      console.error('Error deleting report:', err)
      error.value = '删除报告失败'
    }
  }
}

const handleDownload = async () => {
  try {
    // 创建一个Blob对象包含报告内容
    const blob = new Blob([report.value.content], { type: 'text/markdown;charset=utf-8' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${report.value.title || 'report'}.md`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (err) {
    console.error('Error downloading report:', err)
    error.value = '下载报告失败'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return new Date().toLocaleString()
  return new Date(dateString).toLocaleString()
}

// 直接在渲染时使用marked转换，简化逻辑
const renderMarkdown = (content) => {
  const rawContent = content || '# 报告内容\n\n该报告内容正在生成中...'
  
  // 先处理块级公式，使用更可靠的正则表达式
  let processedContent = rawContent.replace(/\$\$(.*?)\$\$/gs, (match, math) => {
    try {
      // 移除可能的首尾空格和换行符
      const cleanedMath = math.trim()
      return `<div class="katex-block">${katex.renderToString(cleanedMath, {
        displayMode: true,
        throwOnError: false
      })}</div>`
    } catch (error) {
      console.error('块级公式渲染错误:', error)
      return match
    }
  })
  
  // 再处理行内公式
  processedContent = processedContent.replace(/\$(.*?)\$/g, (match, math) => {
    try {
      // 移除可能的首尾空格
      const cleanedMath = math.trim()
      return katex.renderToString(cleanedMath, {
        displayMode: false,
        throwOnError: false
      })
    } catch (error) {
      console.error('行内公式渲染错误:', error)
      return match
    }
  })
  
  // 最后使用marked转换为HTML
  let html = marked(processedContent)
  
  return html
}
</script>
