<script setup>
import { ref, onMounted } from 'vue'
import { Sun, Moon } from 'lucide-vue-next'

const isDark = ref(false)

onMounted(() => {
  // Read current pre-initialized state on load
  isDark.value = document.documentElement.classList.contains('dark')
})

const toggleTheme = () => {
  if (document.documentElement.classList.contains('dark')) {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
    isDark.value = false
  } else {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
    isDark.value = true
  }
}
</script>

<template>
  <header class="storefront-header">
    <div class="header-container">
      <router-link to="/" class="logo">
        <img src="/ehbom-header.png" alt="É bom?" class="logo-image" />
      </router-link>
      <nav class="nav-links">
        <router-link to="/" class="nav-link" active-class="active">
          Vitrine
        </router-link>
        
        <!-- Premium Theme Toggle Button -->
        <button @click="toggleTheme" class="btn-theme" aria-label="Alterar Tema">
          <Sun v-if="isDark" :size="18" class="icon-theme" />
          <Moon v-else :size="18" class="icon-theme" />
        </button>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.storefront-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-glass-header);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  padding: 0.8rem 1.5rem;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  text-decoration: none;
  display: flex;
  align-items: center;
}

.logo-image {
  height: 48px;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.logo-image:hover {
  transform: scale(1.03);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
}

.nav-link:hover {
  color: var(--text-main);
  background: rgba(100, 116, 139, 0.08);
}

.nav-link.active {
  color: var(--accent-green);
  background: rgba(0, 255, 135, 0.08);
}

:root:not(.dark) .nav-link.active {
  color: var(--accent-blue);
  background: rgba(0, 98, 255, 0.08);
}

/* Theme Toggle Button Styling */
.btn-theme {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-theme:hover {
  color: var(--text-main);
  background: rgba(100, 116, 139, 0.08);
}

.icon-theme {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-theme:hover .icon-theme {
  transform: rotate(25deg);
}
</style>
