<template>
  <div class="max-w-4xl mx-auto px-6 py-8">
    <div>
      <h1 class="text-4xl font-bold mb-8">生成实验报告</h1>
    </div>

    <div
      v-if="success"
      class="bg-green-50 border border-green-200 rounded-apple p-6 mb-8 shadow-sm"
    >
      <h3 class="text-xl font-semibold text-green-800 mb-2">
        报告生成成功！
      </h3>
      <p class="text-green-700 mb-4">
        您的实验报告已成功生成，报告ID：{{ reportId }}
      </p>
      <router-link
        :to="`/reports/${reportId}`"
        class="text-primary font-medium hover:underline transition-colors duration-300"
      >
        查看报告详情 →
      </router-link>
    </div>

    <div
      v-if="error"
      class="bg-red-50 border border-red-200 rounded-apple p-6 mb-8 shadow-sm"
    >
      <h3 class="text-xl font-semibold text-red-800 mb-2">
        生成失败
      </h3>
      <p class="text-red-700">{{ error }}</p>
    </div>

    <form
      @submit.prevent="handleSubmit"
      class="space-y-6"
    >
      <!-- 研究主题 -->
      <div>
        <label for="topic" class="block text-sm font-medium mb-2">
          研究主题
        </label>
        <input
          type="text"
          id="topic"
          name="topic"
          v-model="formData.topic"
          class="input"
          placeholder="请输入研究主题（例如：人工智能、量子计算等）"
          required
        />
      </div>

      <!-- 模板上传区域 -->
      <div>
        <label class="block text-sm font-medium mb-2">
          上传报告模板（可选）
        </label>
        <div class="border-2 border-dashed border-borderSecondary rounded-apple p-8 text-center hover:border-primary transition-colors duration-300 hover:shadow-sm">
          <input
            type="file"
            class="hidden"
            id="template-upload"
            @change="handleTemplateChange"
            accept=".doc,.docx"
          />
          <label for="template-upload" class="cursor-pointer">
            <div class="text-primary text-4xl mb-2">📄</div>
            <p class="text-sm text-textSecondary mb-1">
              点击或拖拽模板文件到此处上传
            </p>
            <p class="text-xs text-textSecondary">
              支持 Word 文档格式 (.doc, .docx)
            </p>
          </label>
        </div>
        <!-- 显示已选择的模板文件 -->
        <div v-if="selectedTemplate" class="mt-2">
          <p class="text-sm font-medium mb-1">已选择模板文件：</p>
          <ul class="text-xs text-textSecondary">
            <li>{{ selectedTemplate.name }}</li>
          </ul>
        </div>
        <!-- 模板上传按钮 -->
        <div v-if="selectedTemplate" class="mt-2">
          <button
            type="button"
            class="btn btn-secondary mr-2"
            @click="uploadTemplate"
            :disabled="uploadingTemplate"
          >
            <div v-if="uploadingTemplate" class="flex items-center gap-2">
              <div class="spinner"></div>
              <span>上传中...</span>
            </div>
            <span v-else>上传模板</span>
          </button>
          <button
            type="button"
            class="btn btn-outline"
            @click="clearTemplate"
          >
            取消选择
          </button>
        </div>
        <!-- 模板上传成功提示 -->
        <div v-if="templateUploadSuccess" class="mt-2 text-sm text-green-600">
          ✅ 模板上传成功！
        </div>
      </div>

      <!-- 选择模板 -->
      <div>
        <label for="template-select" class="block text-sm font-medium mb-2">
          选择报告模板（可选）
        </label>
        <select
          id="template-select"
          v-model="formData.template"
          class="input"
        >
          <option value="">无（使用默认模板）</option>
          <option v-for="template in templates" :key="template" :value="template">
            {{ template }}
          </option>
        </select>
        <p class="text-xs text-textSecondary mt-1">
          选择已上传的模板，生成报告将按照该模板格式
        </p>
      </div>

      <!-- 文件上传（可选） -->
      <div>
        <label class="block text-sm font-medium mb-2">
          上传实验数据（可选）
        </label>
        <div class="border-2 border-dashed border-borderSecondary rounded-apple p-8 text-center hover:border-primary transition-colors duration-300 hover:shadow-sm">
          <input
            type="file"
            class="hidden"
            id="file-upload"
            multiple
            @change="handleFileChange"
          />
          <label for="file-upload" class="cursor-pointer">
            <div class="text-primary text-4xl mb-2">📁</div>
            <p class="text-sm text-textSecondary mb-1">
              点击或拖拽文件到此处上传
            </p>
            <p class="text-xs text-textSecondary">
              支持 PDF、Word、Excel、CSV 等格式
            </p>
          </label>
        </div>
        <!-- 显示已选择的文件 -->
        <div v-if="selectedFiles.length > 0" class="mt-2">
          <p class="text-sm font-medium mb-1">已选择 {{ selectedFiles.length }} 个文件：</p>
          <ul class="text-xs text-textSecondary">
            <li v-for="(file, index) in selectedFiles" :key="index">{{ file.name }}</li>
          </ul>
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="flex justify-end">
        <button
          type="submit"
          class="btn btn-primary shadow-apple"
          :disabled="loading"
        >
          <div v-if="loading" class="flex items-center gap-2">
            <div class="spinner"></div>
            <span>生成中...</span>
          </div>
          <span v-else>生成报告</span>
        </button>
      </div>
    </form>

    <!-- 提示信息 -->
    <div class="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-apple shadow-sm">
      <h4 class="font-medium text-blue-800 mb-2">💡 提示</h4>
      <ul class="text-sm text-blue-700 space-y-1">
        <li>• 请尽可能详细地描述实验信息，以获得更准确的报告</li>
        <li>• 支持上传实验原始数据文件，AI将自动分析并整合到报告中</li>
        <li>• 可上传自定义报告模板，生成的报告将按照模板格式编写</li>
        <li>• 生成报告可能需要几分钟时间，请耐心等待</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const formData = ref({
  topic: '',
  template: ''
})
const loading = ref(false)
const success = ref(false)
const error = ref('')
const reportId = ref(null)
const selectedFiles = ref([])

// 模板相关状态
const selectedTemplate = ref(null)
const uploadingTemplate = ref(false)
const templateUploadSuccess = ref(false)
const templates = ref([])

// API URL - 使用相对路径，自动适配当前域名和端口
const API_URL = '/api'

// 组件初始化时获取已上传的模板列表
onMounted(() => {
  fetchTemplates()
})

// 获取已上传的模板列表
const fetchTemplates = async () => {
  try {
    const response = await axios.get(`${API_URL}/get-templates`)
    if (response.data.status === 'success') {
      templates.value = response.data.templates
    }
  } catch (err) {
    console.error('获取模板列表失败:', err)
  }
}

const handleChange = (e) => {
  const { name, value } = e.target
  formData.value[name] = value
}

const handleFileChange = (e) => {
  const files = Array.from(e.target.files)
  selectedFiles.value = files
}

// 处理模板文件选择
const handleTemplateChange = (e) => {
  if (e.target.files.length > 0) {
    selectedTemplate.value = e.target.files[0]
    templateUploadSuccess.value = false
  }
}

// 上传模板文件
const uploadTemplate = async () => {
  if (!selectedTemplate.value) return
  
  uploadingTemplate.value = true
  templateUploadSuccess.value = false
  
  try {
    const formDataToSend = new FormData()
    formDataToSend.append('template', selectedTemplate.value)
    
    const response = await axios.post(`${API_URL}/upload-template`, formDataToSend, {
      timeout: 300000
    })
    
    if (response.data.status === 'success') {
      templateUploadSuccess.value = true
      // 重新获取模板列表
      await fetchTemplates()
      // 自动选择刚上传的模板
      formData.value.template = response.data.filename
    }
  } catch (err) {
    let errorMessage = '模板上传失败，请重试'
    if (err.response) {
      errorMessage = err.response.data?.message || `服务器错误 (${err.response.status})`
      console.error('上传模板错误 - 服务器响应:', err.response)
      console.error('上传模板错误 - 服务器数据:', err.response.data)
    } else if (err.request) {
      errorMessage = '网络错误：无法连接到服务器，请检查网络连接'
      console.error('上传模板错误 - 请求发送失败:', err.request)
    } else {
      errorMessage = err.message || '请求配置错误'
      console.error('上传模板错误 - 请求配置错误:', err)
    }
    error.value = errorMessage
    console.error('上传模板错误:', err)
    console.error('上传模板错误 - 完整错误:', JSON.stringify(err, null, 2))
  } finally {
    uploadingTemplate.value = false
  }
}

// 清除已选择的模板
const clearTemplate = () => {
  selectedTemplate.value = null
  document.getElementById('template-upload').value = ''
  templateUploadSuccess.value = false
}

const handleSubmit = async (e) => {
  e.preventDefault()
  loading.value = true
  error.value = ''
  success.value = false

  try {
    // 使用后端实际的API端点和请求格式
    let response
    
    if (selectedFiles.value.length > 0) {
      // 有文件需要上传，使用FormData
      const formDataToSend = new FormData()
      formDataToSend.append('topic', formData.value.topic)
      formDataToSend.append('template', formData.value.template)
      
      selectedFiles.value.forEach((file, index) => {
        formDataToSend.append('files', file)
      })
      
      response = await axios.post(`${API_URL}/generate-report`, formDataToSend, {
        // 不要手动设置Content-Type，让axios自动处理multipart/form-data的边界
        timeout: 300000 // 添加5分钟超时设置，确保有足够时间生成报告
      })
    } else {
      // 没有文件需要上传，使用JSON格式
      response = await axios.post(`${API_URL}/generate-report`, {
        topic: formData.value.topic,
        template: formData.value.template
      }, {
        timeout: 300000 // 添加5分钟超时设置，确保有足够时间生成报告
      })
    }
    
    // 获取报告数据
    const reportData = response.data
    
    // 使用当前时间戳作为reportId，确保唯一性
    const newReportId = parseInt(Date.now() / 1000)
    
    // 创建新报告对象
    const newReport = {
      id: newReportId,
      title: reportData.filename ? reportData.filename.replace('.md', '') : `报告 ${newReportId}`,
      content: typeof reportData.content === 'string' ? reportData.content : '# 报告内容\n\n生成的报告内容为空',
      word_count: typeof reportData.word_count === 'number' ? reportData.word_count : 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    // 从localStorage获取现有报告列表
    const storedReports = localStorage.getItem('reports')
    const reports = storedReports ? JSON.parse(storedReports) : []
    
    // 将新报告添加到列表中
    reports.push(newReport)
    
    // 更新localStorage
    localStorage.setItem('reports', JSON.stringify(reports))

    reportId.value = newReportId
    success.value = true
    
    // 重置表单
    formData.value = {
      topic: '',
      template: ''
    }
    selectedFiles.value = []
    clearTemplate()
  } catch (err) {
    // 详细的错误信息处理
    let errorMessage = '生成报告失败，请重试'
    if (err.response) {
      // 服务器返回了错误响应
      errorMessage = err.response.data?.message || `服务器错误 (${err.response.status})`
    } else if (err.request) {
      // 请求已发送但没有收到响应
      errorMessage = '网络错误：无法连接到服务器，请检查网络连接'
    } else {
      // 请求配置错误
      errorMessage = err.message || '请求配置错误'
    }
    error.value = errorMessage
    console.error('生成报告错误:', err)
  } finally {
    loading.value = false
  }
}
</script>
