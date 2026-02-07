import React from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="space-y-20 px-6">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center py-16 md:py-24"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-8">
          智能实验报告生成器
        </h1>
        <p className="text-xl md:text-2xl text-textSecondary max-w-3xl mx-auto mb-12">
          利用AI技术，快速生成专业、准确的实验报告，让科研工作更高效
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-6">
          <motion.div
            whileHover={{ scale: 1.03, boxShadow: "0 10px 20px rgba(0, 122, 255, 0.3)" }}
            whileTap={{ scale: 0.98 }}
          >
            <Link to="/generate" className="btn btn-primary shadow-apple">
              立即生成报告
            </Link>
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
          >
            <Link to="/reports" className="btn btn-secondary">
              查看我的报告
            </Link>
          </motion.div>
        </div>
      </motion.section>



      {/* How It Works Section */}
      <section className="py-16 bg-backgroundTertiary rounded-apple px-6">
        <h2 className="text-3xl font-bold text-center mb-16">
          简单三步，生成专业报告
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="flex flex-col items-center"
            >
              <div className="w-16 h-16 rounded-apple bg-primary text-white flex items-center justify-center text-2xl font-bold mb-6 shadow-apple">
                {step.number}
              </div>
              <h3 className="text-xl font-semibold mb-4">
                {step.title}
              </h3>
              <p className="text-textSecondary max-w-xs text-center">
                {step.description}
              </p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="card text-center py-16 shadow-apple"
      >
        <h2 className="text-3xl font-bold mb-4">
          准备好开始了吗？
        </h2>
        <p className="text-xl text-textSecondary max-w-3xl mx-auto mb-10">
          体验AI驱动的实验报告生成，提升您的科研效率
        </p>
        <motion.div
          whileHover={{ scale: 1.03, boxShadow: "0 10px 20px rgba(0, 122, 255, 0.3)" }}
          whileTap={{ scale: 0.98 }}
        >
          <Link to="/generate" className="btn btn-primary shadow-apple">
            开始生成报告
          </Link>
        </motion.div>
      </motion.section>
    </div>
  )
}

// 功能数据
const features = [
  {
    title: '智能分析',
    description: 'AI自动分析实验数据，识别关键结果和趋势，生成专业分析内容',
    icon: '🧠',
  },
  {
    title: '模板丰富',
    description: '提供多种学科的实验报告模板，满足不同领域的科研需求',
    icon: '📋',
  },
  {
    title: '实时预览',
    description: '生成过程中实时预览报告内容，支持在线编辑和调整',
    icon: '👀',
  },
  {
    title: '导出便捷',
    description: '支持导出多种格式（PDF、Word等），方便提交和分享',
    icon: '💾',
  },
  {
    title: '数据安全',
    description: '严格的数据加密和隐私保护，确保您的科研数据安全',
    icon: '🔒',
  },
  {
    title: '协作功能',
    description: '支持团队协作编辑，多人共同完成实验报告',
    icon: '👥',
  },
]

// 步骤数据
const steps = [
  {
    number: '1',
    title: '输入实验信息',
    description: '填写实验名称、目的、方法等基本信息',
  },
  {
    number: '2',
    title: '上传实验数据',
    description: '上传实验原始数据或直接输入关键数据点',
  },
  {
    number: '3',
    title: '生成并下载',
    description: 'AI自动生成完整报告，预览后下载使用',
  },
]

export default Home