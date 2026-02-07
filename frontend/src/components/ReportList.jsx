import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import axios from 'axios'

const ReportList = () => {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    setLoading(true)
    setError('')

    try {
      // 从localStorage获取报告列表
      const storedReports = localStorage.getItem('reports')
      const reports = storedReports ? JSON.parse(storedReports) : []
      setReports(reports)
    } catch (err) {
      console.error('Error fetching reports:', err)
      setError('获取报告列表失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (reportId) => {
    if (window.confirm('确定要删除此报告吗？')) {
      try {
        // 从localStorage删除报告，使用类型无关的比较
        const updatedReports = reports.filter(report => {
          const id1 = typeof report.id === 'string' ? parseInt(report.id) : report.id
          const id2 = typeof reportId === 'string' ? parseInt(reportId) : reportId
          return id1 !== id2
        })
        localStorage.setItem('reports', JSON.stringify(updatedReports))
        setReports(updatedReports)
      } catch (err) {
        console.error('Error deleting report:', err)
        setError('删除报告失败')
      }
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
        <p className="text-red-700 mb-4">{error}</p>
        <button
          onClick={fetchReports}
          className="btn btn-primary"
        >
          重试
        </button>
      </div>
    )
  }

  return (
    <div className="px-6 py-8">
      <div className="flex justify-between items-center mb-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-3xl font-bold"
        >
          我的报告
        </motion.h1>
        <motion.div
          whileHover={{ scale: 1.03, boxShadow: "0 10px 20px rgba(0, 122, 255, 0.3)" }}
          whileTap={{ scale: 0.98 }}
        >
          <Link to="/generate" className="btn btn-primary shadow-apple">
            生成新报告
          </Link>
        </motion.div>
      </div>

      {reports.length === 0 ? (
        <div className="card shadow-apple text-center py-12">
          <div className="text-textSecondary text-5xl mb-4">📄</div>
          <h3 className="text-xl font-semibold mb-2">
            暂无报告
          </h3>
          <p className="text-textSecondary mb-6">
            您还没有生成任何实验报告
          </p>
          <Link to="/generate" className="btn btn-primary shadow-apple">
            立即生成
          </Link>
        </div>
      ) : (
        <div className="grid gap-6">
          {reports.map((report, index) => (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="card shadow-apple hover:shadow-apple-hover transition-all duration-300"
            >
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
                <div className="flex-1">
                  <Link
                    to={`/reports/${report.id}`}
                    className="group"
                  >
                    <h3 className="text-xl font-semibold mb-1 group-hover:text-primary transition-colors duration-300">
                      {report.title || `报告 ${report.id}`}
                    </h3>
                    <p className="text-sm text-textSecondary mb-2">
                      {report.topic || '无描述'}
                    </p>
                  </Link>
                  
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="px-2 py-1 bg-primary/10 text-primary rounded-full">
                      {report.status || '已完成'}
                    </span>
                    <span className="px-2 py-1 bg-backgroundTertiary text-textSecondary rounded-full">
                      创建于 {new Date(report.created_at || Date.now()).toLocaleString()}
                    </span>
                    <span className="px-2 py-1 bg-backgroundTertiary text-textSecondary rounded-full">
                      {report.word_count} 字
                    </span>
                  </div>
                </div>

                <div className="mt-4 md:mt-0 flex gap-3">
                  <Link
                    to={`/reports/${report.id}`}
                    className="btn btn-secondary"
                  >
                    查看
                  </Link>
                  <button
                    onClick={() => handleDelete(report.id)}
                    className="btn bg-red-100 text-red-800 hover:bg-red-200 active:bg-red-300 transition-colors duration-300"
                  >
                    删除
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* 分页组件（如果需要） */}
      {/* <div className="mt-8 flex justify-center">
        <nav className="flex items-center space-x-2">
          <button className="btn btn-secondary disabled:opacity-50">
            上一页
          </button>
          <button className="btn btn-primary">1</button>
          <button className="btn btn-secondary">2</button>
          <button className="btn btn-secondary">3</button>
          <button className="btn btn-secondary">下一页</button>
        </nav>
      </div> */}
    </div>
  )
}

export default ReportList