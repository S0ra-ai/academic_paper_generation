<template>
  <header class="sticky top-0 z-50 glass border-b border-borderSecondary">
    <div class="container mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <router-link to="/" class="flex items-center space-x-2">
          <div class="w-10 h-10 rounded-apple flex items-center justify-center bg-primary text-white font-bold shadow-sm">
            R
          </div>
          <span class="text-xl font-bold">智研</span>
        </router-link>
        
        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-2">
          <router-link
            v-for="route in routes"
            :key="route.path"
            :to="route.path"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path === route.path }"
          >
            {{ route.label }}
          </router-link>
        </nav>
        
        <!-- Mobile Menu Button -->
        <button 
          class="md:hidden p-2 rounded-apple-sm text-textSecondary hover:bg-backgroundTertiary"
          @click="mobileMenuOpen = !mobileMenuOpen"
          aria-label="Toggle menu"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
      
      <!-- Mobile Navigation -->
      <nav v-if="mobileMenuOpen" class="md:hidden mt-4 pb-4 space-y-2 animate-fade-in">
        <router-link
          v-for="route in routes"
          :key="route.path"
          :to="route.path"
          class="block py-3 px-4 rounded-apple-sm text-text hover:bg-backgroundTertiary"
          :class="{ 'bg-primary/10 text-primary font-medium': $route.path === route.path }"
          @click="mobileMenuOpen = false"
        >
          {{ route.label }}
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
const routes = [
  { path: '/', label: '首页' },
  { path: '/generate', label: '生成报告' },
  { path: '/reports', label: '我的报告' },
]
</script>
