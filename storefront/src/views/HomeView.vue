<script setup>
import { ref, onMounted, computed } from 'vue'
import { Search, SlidersHorizontal, ArrowRight, Tag, Award, Gem } from 'lucide-vue-next'

const posts = ref([])
const searchQuery = ref('')
const selectedStore = ref('all')
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('/data/posts.json')
    if (res.ok) {
      posts.value = await res.json()
    }
  } catch (err) {
    console.error('Error fetching posts:', err)
  } finally {
    loading.value = false
  }
})

// Extract all stores dynamically for filtering
const allStores = computed(() => {
  const stores = new Set()
  posts.value.forEach(post => {
    post.products.forEach(p => {
      if (p.store) stores.add(p.store)
    })
  })
  return ['all', ...Array.from(stores)]
})

// Filter comparisons based on search and store
const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          post.products.some(p => p.title.toLowerCase().includes(searchQuery.value.toLowerCase()))
    
    const matchesStore = selectedStore.value === 'all' || 
                         post.products.some(p => p.store === selectedStore.value)
                         
    return matchesSearch && matchesStore
  })
})

const getBadgeIcon = (badge) => {
  if (badge === 'Mais Barato') return Tag
  if (badge === 'Custo-Benefício') return Award
  return Gem
}

const getBadgeClass = (badge) => {
  if (badge === 'Mais Barato') return 'badge-cheap'
  if (badge === 'Custo-Benefício') return 'badge-value'
  return 'badge-premium'
}
</script>

<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">É bom?</h1>
        <p class="hero-subtitle">Descubra se o produto realmente vale a pena com nossas análises independentes e comparativos das maiores lojas do país.</p>
      </div>
    </section>

    <!-- Search & Filters -->
    <section class="filter-section">
      <div class="filter-bar">
        <div class="search-box">
          <Search class="icon-search" :size="20" />
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="O que você está procurando hoje? (Ex: fone bluetooth, TV...)" 
            class="search-input"
          />
        </div>
        <div class="store-filter">
          <SlidersHorizontal :size="16" />
          <span class="filter-label">Loja:</span>
          <select v-model="selectedStore" class="filter-select">
            <option value="all">Todas as Lojas</option>
            <option v-for="store in allStores.filter(s => s !== 'all')" :key="store" :value="store">
              {{ store }}
            </option>
          </select>
        </div>
      </div>
    </section>

    <!-- Skeletons Loader -->
    <div v-if="loading" class="skeletons-grid">
      <div v-for="i in 3" :key="i" class="skeleton-card">
        <div class="skeleton-header"></div>
        <div class="skeleton-products">
          <div v-for="j in 3" :key="j" class="skeleton-product"></div>
        </div>
        <div class="skeleton-button"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredPosts.length === 0" class="empty-state">
      <h3>Nenhum comparativo encontrado</h3>
      <p>Tente ajustar sua pesquisa ou redefinir seus filtros.</p>
    </div>

    <!-- Storefront Grid -->
    <div v-else class="vitrine-grid">
      <article v-for="post in filteredPosts" :key="post.slug" class="vitrine-card">
        <div class="card-header">
          <h2 class="card-title">{{ post.title }}</h2>
          <span class="card-date">Publicado em {{ new Date(post.date).toLocaleDateString('pt-BR') }}</span>
        </div>

        <!-- Horizontal Product Grid -->
        <div class="products-row">
          <div v-for="product in post.products" :key="product.badge" class="product-item">
            <!-- Badge -->
            <div class="product-badge" :class="getBadgeClass(product.badge)">
              <component :is="getBadgeIcon(product.badge)" :size="14" />
              <span>{{ product.badge }}</span>
            </div>

            <!-- Image -->
            <div class="image-wrapper">
              <img :src="product.image_url" :alt="product.title" class="product-img" loading="lazy" />
            </div>

            <!-- Title & Price -->
            <div class="product-info">
              <h3 class="product-title">{{ product.title }}</h3>
              <div class="product-meta">
                <span class="product-store">{{ product.store }}</span>
                <span class="product-price">R$ {{ parseFloat(product.price).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
              </div>
            </div>

            <!-- Direct Affiliate Button -->
            <a :href="product.link" target="_blank" rel="noopener noreferrer" class="btn-buy">
              Ir para Loja
            </a>
          </div>
        </div>

        <!-- Footer CTA -->
        <div class="card-footer">
          <router-link :to="`/posts/${post.slug}`" class="btn-detail">
            <span>Ver Análise Detalhada</span>
            <ArrowRight :size="16" />
          </router-link>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: 3rem 1rem;
  background: radial-gradient(circle at top, var(--shadow-hover) 0%, rgba(0, 0, 0, 0) 70%);
  border-radius: 20px;
}

.hero-title {
  font-family: 'Outfit', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--text-main) 0%, var(--text-muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: var(--text-muted);
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Search & Filters */
.filter-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 1.25rem;
  border-radius: 14px;
  box-shadow: 0 4px 20px var(--shadow-color);
}

.filter-bar {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex-grow: 1;
}

.icon-search {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  opacity: 0.6;
}

.search-input {
  width: 100%;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 0.9rem 1rem 0.9rem 3rem;
  color: var(--text-main);
  font-size: 1rem;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.search-input:focus {
  background: var(--bg-wrapper);
  border-color: var(--accent-green);
  box-shadow: 0 0 0 4px rgba(0, 255, 135, 0.15);
}

:root:not(.dark) .search-input:focus {
  box-shadow: 0 0 0 4px rgba(0, 98, 255, 0.1);
}

.store-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.95rem;
  min-width: 220px;
}

.filter-label {
  font-weight: 500;
}

.filter-select {
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-main);
  padding: 0.6rem 1.25rem;
  font-size: 0.95rem;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.filter-select:focus {
  border-color: var(--accent-green);
}

/* Vitrine Grid */
.vitrine-grid {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.vitrine-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 30px var(--shadow-color);
}

.vitrine-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 255, 135, 0.25);
  box-shadow: 0 12px 40px var(--shadow-hover);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1.25rem;
}

.card-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
  letter-spacing: -0.5px;
}

.card-date {
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* Product Row layout inside card */
.products-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.product-item {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  position: relative;
  transition: all 0.2s ease;
}

.product-item:hover {
  background: var(--bg-panel);
  border-color: var(--border-color);
}

.product-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.75rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.2px;
  text-transform: uppercase;
  z-index: 5;
}

.badge-cheap {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

:root:not(.dark) .badge-cheap {
  background: rgba(16, 185, 129, 0.08);
  color: #059669;
}

.badge-value {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

:root:not(.dark) .badge-value {
  background: rgba(245, 158, 11, 0.08);
  color: #d97706;
}

.badge-premium {
  background: rgba(139, 92, 246, 0.12);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

:root:not(.dark) .badge-premium {
  background: rgba(139, 92, 246, 0.08);
  color: #7c3aed;
}

.image-wrapper {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-page);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  margin-top: 1.5rem;
}

.product-img {
  max-height: 130px;
  max-width: 90%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.product-item:hover .product-img {
  transform: scale(1.05);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex-grow: 1;
}

.product-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.8rem;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
  padding-top: 0.75rem;
}

.product-store {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
}

.product-price {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
}

.btn-buy {
  background: var(--accent-blue);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem;
  font-weight: 700;
  font-size: 0.9rem;
  text-decoration: none;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-buy:hover {
  background: var(--accent-green);
  color: #0c0c12;
  box-shadow: 0 4px 15px var(--shadow-hover);
}

/* Card Footer */
.card-footer {
  display: flex;
  justify-content: center;
  border-top: 1px solid var(--border-color);
  padding-top: 1.5rem;
}

.btn-detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-main);
  padding: 0.8rem 1.75rem;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-detail:hover {
  background: var(--bg-panel);
  border-color: var(--accent-green);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 1rem;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: 16px;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-muted);
}

/* Skeletons */
.skeletons-grid {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.skeleton-card {
  height: 480px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.skeleton-header {
  height: 32px;
  width: 50%;
  background: var(--border-color);
  border-radius: 4px;
}

.skeleton-products {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  flex-grow: 1;
}

.skeleton-product {
  background: var(--bg-panel);
  border-radius: 12px;
}

.skeleton-button {
  height: 44px;
  width: 200px;
  align-self: center;
  background: var(--border-color);
  border-radius: 8px;
}

/* Responsive Extreme */
@media (max-width: 900px) {
  .products-row {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
  .image-wrapper {
    height: 140px;
  }
}

@media (max-width: 600px) {
  .hero-title {
    font-size: 2rem;
  }
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .store-filter {
    min-width: unset;
  }
  .vitrine-card {
    padding: 1.25rem;
  }
}
</style>
