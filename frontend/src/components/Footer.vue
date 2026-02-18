<template>
  <footer class="bg-backgroundTertiary border-t border-borderSecondary">
    <div class="container mx-auto px-6 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-10 h-10 rounded-apple flex items-center justify-center bg-primary text-white font-bold shadow-sm">
              R
            </div>
            <span class="text-xl font-bold">智研</span>
          </div>
          <p class="text-textSecondary mb-4">
            智能生成实验报告，提高科研效率
          </p>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">快速链接</h3>
          <nav class="space-y-2">
            <router-link to="/" class="block text-textSecondary hover:text-primary">首页</router-link>
            <router-link to="/generate" class="block text-textSecondary hover:text-primary">生成报告</router-link>
            <router-link to="/reports" class="block text-textSecondary hover:text-primary">我的报告</router-link>
          </nav>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">技术支持</h3>
          <p class="text-textSecondary">
            如果您有任何问题，请联系我们的技术支持团队
          </p>
        </div>
      </div>
      
      <div class="mt-12 pt-8 border-t border-borderSecondary text-center text-textTertiary">
        <p>© 2024 实验报告生成器. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>
