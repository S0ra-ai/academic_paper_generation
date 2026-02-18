import React from 'react'
import { BrowserRouter as Router, Switch, Route, Link, useLocation, NavLink } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

// 导入页面组件（将在后面创建）
import Home from './components/Home'
import ReportGenerator from './components/ReportGenerator'
import ReportList from './components/ReportList'
import ReportDetail from './components/ReportDetail'

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <NavBar />
        <main className="flex-grow container mx-auto px-6 py-8">
          <AnimatePresence mode="wait">
            <Switch>
              <Route
                path="/generate"
                component={() => (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5 }}
                  >
                    <ReportGenerator />
                  </motion.div>
                )}
              />
              <Route
                path="/"
                exact
                component={() => (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5 }}
                  >
                    <Home />
                  </motion.div>
                )}
              />
              <Route
                path="/reports/:id"
                component={() => (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5 }}
                  >
                    <ReportDetail />
                  </motion.div>
                )}
              />
              <Route
                path="/reports"
                component={() => (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5 }}
                  >
                    <ReportList />
                  </motion.div>
                )}
              />
            </Switch>
          </AnimatePresence>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

// 导航栏组件
function NavBar() {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)
  const routes = [
    { path: '/', label: '首页' },
    { path: '/generate', label: '生成报告' },
    { path: '/reports', label: '我的报告' },
  ]

  return (
    <header className="sticky top-0 z-50 glass border-b border-borderSecondary">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 rounded-apple flex items-center justify-center bg-primary text-white font-bold shadow-sm">
              R
            </div>
            <span className="text-xl font-bold">智研</span>
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-2">
            {routes.map((route) => (
              <NavLink
                key={route.path}
                to={route.path}
                className={({ isActive }) => isActive ? 'nav-item nav-item-active' : 'nav-item'}
              >
                {route.label}
              </NavLink>
            ))}
          </nav>
          
          {/* Mobile Menu Button */}
          <button 
            className="md:hidden p-2 rounded-apple-sm text-textSecondary hover:bg-backgroundTertiary"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
        
        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <motion.nav 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
            className="md:hidden mt-4 pb-4 space-y-2"
          >
            {routes.map((route) => (
              <NavLink
                key={route.path}
                to={route.path}
                className={({ isActive }) => isActive ? 'block py-3 px-4 rounded-apple-sm bg-primary/10 text-primary font-medium' : 'block py-3 px-4 rounded-apple-sm text-text hover:bg-backgroundTertiary'}
                onClick={() => setMobileMenuOpen(false)}
              >
                {route.label}
              </NavLink>
            ))}
          </motion.nav>
        )}
      </div>
    </header>
  )
}

// 页脚组件
function Footer() {
  return (
    <motion.footer 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="bg-backgroundTertiary border-t border-borderSecondary"
    >
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 rounded-apple flex items-center justify-center bg-primary text-white font-bold shadow-sm">
                R
              </div>
              <span className="text-xl font-bold">智研</span>
            </div>
            <p className="text-textSecondary mb-4">
              智能生成实验报告，提高科研效率
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">快速链接</h3>
            <nav className="space-y-2">
              <Link to="/" className="block text-textSecondary hover:text-primary">首页</Link>
              <Link to="/generate" className="block text-textSecondary hover:text-primary">生成报告</Link>
              <Link to="/reports" className="block text-textSecondary hover:text-primary">我的报告</Link>
            </nav>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">技术支持</h3>
            <p className="text-textSecondary">
              如果您有任何问题，请联系我们的技术支持团队
            </p>
          </div>
        </div>
        
        <div className="mt-12 pt-8 border-t border-borderSecondary text-center text-textTertiary">
          <p>© 2024 实验报告生成器. 保留所有权利.</p>
        </div>
      </div>
    </motion.footer>
  )
}

export default App