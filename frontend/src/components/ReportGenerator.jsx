import React, { useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { Link } from 'react-router-dom'

const ReportGenerator = () => {
  const [formData, setFormData] = useState({
    topic: '',
  })
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')
  const [reportId, setReportId] = useState(null)
  const [selectedFiles, setSelectedFiles] = useState([])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files)
    setSelectedFiles(files)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess(false)

    try {
      // 使用后端实际的API端点和请求格式
      let response
      // 使用绝对URL直接连接后端，绕过代理问题
      const API_URL = 'http://43.153.41.145:8080/api'
      

      
      if (selectedFiles.length > 0) {
        // 有文件需要上传，使用FormData
        const formDataToSend = new FormData()
        formDataToSend.append('topic', formData.topic)
        

        
        selectedFiles.forEach((file, index) => {
          formDataToSend.append('files', file)

        })
        

        

        
        response = await axios.post(`${API_URL}/generate-report`, formDataToSend, {
          // 不要手动设置Content-Type，让axios自动处理multipart/form-data的边界

          timeout: 300000 // 添加5分钟超时设置，确保有足够时间生成报告
        })
      } else {
        // 没有文件需要上传，使用JSON格式

        response = await axios.post(`${API_URL}/generate-report`, {
          topic: formData.topic,
        }, {
          timeout: 300000 // 添加5分钟超时设置，确保有足够时间生成报告
        })
      }
      
      // 获取报告数据
      const reportData = response.data
      
      // 使用当前时间戳作为reportId，确保唯一性
      const reportId = parseInt(Date.now() / 1000)
      
      // 创建新报告对象
      const newReport = {
        id: reportId,
        title: reportData.filename ? reportData.filename.replace('.md', '') : `报告 ${reportId}`,
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

      
      setReportId(reportId)
      setSuccess(true)
      
      // 重置表单
      setFormData({
        topic: '',
      })
    } catch (err) {
        // 详细的错误信息处理
        let errorMessage = '生成报告失败，请重试';
        if (err.response) {
          // 服务器返回了错误响应
          errorMessage = err.response.data?.message || `服务器错误 (${err.response.status})`;
        } else if (err.request) {
          // 请求已发送但没有收到响应
          errorMessage = '网络错误：无法连接到服务器，请检查网络连接';
        } else {
          // 请求配置错误
          errorMessage = err.message || '请求配置错误';
        }
        setError(errorMessage);
        console.error('生成报告错误:', err);
      } finally {
        setLoading(false)
      }
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <h1 className="text-4xl font-bold mb-8">生成实验报告</h1>
      </motion.div>

      {success && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="bg-green-50 border border-green-200 rounded-apple p-6 mb-8 shadow-sm"
        >
          <h3 className="text-xl font-semibold text-green-800 mb-2">
            报告生成成功！
          </h3>
          <p className="text-green-700 mb-4">
            您的实验报告已成功生成，报告ID：{reportId}
          </p>
          <Link
            to={`/reports/${reportId}`}
            className="text-primary font-medium hover:underline transition-colors duration-300"
          >
            查看报告详情 →
          </Link>
        </motion.div>
      )}

      {error && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="bg-red-50 border border-red-200 rounded-apple p-6 mb-8 shadow-sm"
        >
          <h3 className="text-xl font-semibold text-red-800 mb-2">
            生成失败
          </h3>
          <p className="text-red-700">{error}</p>
        </motion.div>
      )}

      <motion.form
        onSubmit={handleSubmit}
        className="space-y-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        {/* 研究主题 */}
        <div>
          <label htmlFor="topic" className="block text-sm font-medium mb-2">
            研究主题
          </label>
          <input
            type="text"
            id="topic"
            name="topic"
            value={formData.topic}
            onChange={handleChange}
            className="input"
            placeholder="请输入研究主题（例如：人工智能、量子计算等）"
            required
          />
        </div>

        {/* 文件上传（可选） */}
        <div>
          <label className="block text-sm font-medium mb-2">
            上传实验数据（可选）
          </label>
          <div className="border-2 border-dashed border-borderSecondary rounded-apple p-8 text-center hover:border-primary transition-colors duration-300 hover:shadow-sm">
            <input
              type="file"
              className="hidden"
              id="file-upload"
              multiple
              onChange={handleFileChange}
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="text-primary text-4xl mb-2">📁</div>
              <p className="text-sm text-textSecondary mb-1">
                点击或拖拽文件到此处上传
              </p>
              <p className="text-xs text-textSecondary">
                支持 PDF、Word、Excel、CSV 等格式
              </p>
            </label>
          </div>
          {/* 显示已选择的文件 */}
          {selectedFiles.length > 0 && (
            <div className="mt-2">
              <p className="text-sm font-medium mb-1">已选择 {selectedFiles.length} 个文件：</p>
              <ul className="text-xs text-textSecondary">
                {selectedFiles.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* 提交按钮 */}
        <div className="flex justify-end">
          <motion.button
            type="submit"
            className="btn btn-primary shadow-apple"
            disabled={loading}
            whileHover={!loading ? { scale: 1.03, boxShadow: "0 10px 20px rgba(0, 122, 255, 0.3)" } : {}}
            whileTap={!loading ? { scale: 0.98 } : {}}
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <div className="spinner"></div>
                <span>生成中...</span>
              </div>
            ) : (
              '生成报告'
            )}
          </motion.button>
        </div>
      </motion.form>

      {/* 提示信息 */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-apple shadow-sm"
      >
        <h4 className="font-medium text-blue-800 mb-2">💡 提示</h4>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• 请尽可能详细地描述实验信息，以获得更准确的报告</li>
          <li>• 支持上传实验原始数据文件，AI将自动分析并整合到报告中</li>
          <li>• 生成报告可能需要几分钟时间，请耐心等待</li>
        </ul>
      </motion.div>
    </div>
  )
}

export default ReportGenerator