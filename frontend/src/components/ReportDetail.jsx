import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link, useParams, useHistory } from 'react-router-dom'
import axios from 'axios'
import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const ReportDetail = () => {
  const { id } = useParams()
  const history = useHistory()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // 配置marked支持GFM
  useEffect(() => {
    marked.setOptions({
      gfm: true,
      breaks: true,
      headerIds: true,
      mangle: false
    })
  }, [])

  useEffect(() => {
    fetchReport()
  }, [id])

  const fetchReport = async () => {
    setLoading(true)
    setError('')
    try {
      // 从localStorage获取报告列表
      const storedReports = localStorage.getItem('reports')
      
      const reports = storedReports ? JSON.parse(storedReports) : []
      
      // 根据URL参数查找对应的报告（同时尝试字符串和数字类型匹配）
      const foundReport = reports.find(report => 
        report.id === parseInt(id) || report.id === id
      )
      
      if (foundReport) {
        if (typeof foundReport.content === 'string') {
          setReport(foundReport)
        } else {
          setError('报告内容格式错误')
          console.error('报告内容不是字符串:', foundReport.content)
        }
      } else {
        setError('未找到该报告')
      }
    } catch (err) {
      console.error('Error fetching report:', err)
      setError('获取报告详情失败')
    } finally {
      setLoading(false)
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
          report.id !== parseInt(id) && report.id !== id
        )
        localStorage.setItem('reports', JSON.stringify(updatedReports))
        history.push('/reports')
      } catch (err) {
        console.error('Error deleting report:', err)
        setError('删除报告失败')
      }
    }
  }

  const handleDownload = async () => {
    try {
      // 创建一个Blob对象包含报告内容
      const blob = new Blob([report.content], { type: 'text/markdown;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${report.title || 'report'}.md`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      console.error('Error downloading report:', err)
      setError('下载报告失败')
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="spinner w-10 h-10"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
        <h3 className="text-xl font-semibold text-red-800 mb-2">
          获取失败
        </h3>
        <p className="text-red-700 mb-6">{error}</p>
        <div className="flex justify-center gap-4">
          <button
            onClick={fetchReport}
            className="btn btn-primary"
          >
            重试
          </button>
          <Link to="/reports" className="btn btn-secondary">
            返回列表
          </Link>
        </div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="card text-center py-12">
        <div className="text-secondary text-5xl mb-4">🔍</div>
        <h3 className="text-xl font-semibold text-text mb-2">
          报告不存在
        </h3>
        <p className="text-secondary mb-6">
          该报告可能已被删除或ID错误
        </p>
        <Link to="/reports" className="btn btn-primary">
          返回报告列表
        </Link>
      </div>
    )
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

  return (
    <div className="space-y-8 px-6 py-8">
      {/* 报告头部 */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex flex-col md:flex-row justify-between items-start gap-6 mb-4">
          <div>
            <Link
              to="/reports"
              className="text-primary font-medium hover:underline mb-4 inline-block transition-colors duration-300"
            >
              ← 返回报告列表
            </Link>
            <h1 className="text-4xl font-bold mb-2">
              {report.title || `报告 ${id}`}
            </h1>
            <p className="text-textSecondary">
              创建于 {new Date(report.created_at || Date.now()).toLocaleString()}
            </p>
          </div>

          <div className="flex gap-3">
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleDownload}
              className="btn btn-secondary"
            >
              💾 下载
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleDelete}
              className="btn bg-red-100 text-red-800 hover:bg-red-200 active:bg-red-300 transition-colors duration-300"
            >
              🗑️ 删除
            </motion.button>
          </div>
        </div>

        {/* 报告标签 */}
        <div className="flex flex-wrap gap-3 mb-6">
          <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">
            {report.status || '已完成'}
          </span>
          <span className="px-3 py-1 bg-backgroundTertiary text-textSecondary rounded-full text-sm">
            ID: {id}
          </span>
          <span className="px-3 py-1 bg-backgroundTertiary text-textSecondary rounded-full text-sm">
            {report.word_count || 0} 字
          </span>
          <span className="px-3 py-1 bg-backgroundTertiary text-textSecondary rounded-full text-sm">
            更新于 {new Date(report.updated_at || report.created_at || Date.now()).toLocaleString()}
          </span>
        </div>
      </motion.div>

      {/* 报告内容 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="card shadow-apple"
      >
        <div className="p-6">

          
          <h2 className="text-2xl font-bold mb-4">报告内容</h2>
          
          {/* 使用prose类并添加额外的表格样式 */}
          <div className="prose max-w-none">
            <div dangerouslySetInnerHTML={{ __html: renderMarkdown(report.content) }} />
          </div>
        </div>
      </motion.div>

      {/* 操作按钮 */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="flex justify-center gap-6"
      >
        <Link to="/reports" className="btn btn-secondary">
          返回报告列表
        </Link>
        <Link to="/generate" className="btn btn-primary shadow-apple">
          生成新报告
        </Link>
      </motion.div>
    </div>
  )
}

export default ReportDetail