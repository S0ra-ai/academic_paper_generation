<template>
  <div class="space-y-20 px-6">
    <!-- Hero Section -->
    <transition
      enter-active-class="transition-all duration-800 ease-out"
      leave-active-class="transition-all duration-500 ease-in"
      enter-from-class="opacity-0 translate-y-10"
      leave-to-class="opacity-0 translate-y-10"
    >
      <section
        v-if="isLoaded"
        class="text-center py-16 md:py-24"
      >
      <h1 class="text-4xl md:text-5xl font-bold mb-8">
        智研
      </h1>
      <p class="text-xl md:text-2xl text-textSecondary max-w-3xl mx-auto mb-12">
        利用AI技术，快速生成专业、准确的实验报告，让科研工作更高效
      </p>
      <div class="flex flex-col sm:flex-row justify-center gap-6">
        <router-link
          to="/generate"
          class="btn btn-primary shadow-apple"
        >
          立即生成报告
        </router-link>
        <router-link
          to="/generate-code"
          class="btn btn-secondary"
        >
          计算机专业论文
        </router-link>
        <router-link
          to="/reports"
          class="btn btn-outline"
        >
          查看我的报告
        </router-link>
      </div>
      </section>
    </transition>

    <!-- How It Works Section -->
    <transition
      enter-active-class="transition-all duration-800 ease-out"
      leave-active-class="transition-all duration-500 ease-in"
      enter-from-class="opacity-0 translate-y-10"
      leave-to-class="opacity-0 translate-y-10"
    >
      <section 
        v-if="isLoaded"
        class="py-16 bg-backgroundTertiary rounded-apple px-6"
      >
      <h2 class="text-3xl font-bold text-center mb-16">
        简单三步，生成专业报告
      </h2>
      <transition-group
        tag="div"
        class="grid grid-cols-1 md:grid-cols-3 gap-12"
        enter-active-class="transition-all duration-500 ease-out"
        leave-active-class="transition-all duration-300 ease-in"
        enter-from-class="opacity-0 translate-y-20"
        leave-to-class="opacity-0 translate-y-20"
      >
        <div
          v-for="(step, index) in steps"
          :key="step.title"
          class="flex flex-col items-center"
          :style="{ transitionDelay: index * 100 + 'ms' }"
        >
          <div class="w-16 h-16 rounded-apple bg-primary text-white flex items-center justify-center text-2xl font-bold mb-6 shadow-apple">
            {{ step.number }}
          </div>
          <h3 class="text-xl font-semibold mb-4">
            {{ step.title }}
          </h3>
          <p class="text-textSecondary max-w-xs text-center">
            {{ step.description }}
          </p>
        </div>
      </transition-group>
    </section>
    </transition>

    <!-- CTA Section -->
    <transition
      enter-active-class="transition-all duration-800 ease-out"
      leave-active-class="transition-all duration-500 ease-in"
      enter-from-class="opacity-0 scale-95"
      leave-to-class="opacity-0 scale-95"
    >
      <section 
        v-if="isLoaded"
        class="card text-center py-16 shadow-apple"
      >
      <h2 class="text-3xl font-bold mb-4">
        准备好开始了吗？
      </h2>
      <p class="text-xl text-textSecondary max-w-3xl mx-auto mb-10">
        体验AI驱动的实验报告生成，提升您的科研效率
      </p>
      <div class="flex flex-col sm:flex-row justify-center gap-6">
        <router-link
          to="/generate"
          class="btn btn-primary shadow-apple"
        >
          开始生成报告
        </router-link>
        <router-link
          to="/generate-code"
          class="btn btn-secondary"
        >
          计算机专业论文
        </router-link>
      </div>
    </section>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 添加初始加载状态，用于触发动画
const isLoaded = ref(false)

// 组件挂载后触发动画
onMounted(() => {
  isLoaded.value = true
})

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
</script>
