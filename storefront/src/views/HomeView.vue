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
        <h1 class="hero-title">Vitrine Inteligente de Recomendações</h1>
        <p class="hero-subtitle">Análises independentes geradas por IA com curadoria das melhores ofertas das maiores lojas do país.</p>
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
  background: radial-gradient(circle at top, rgba(0, 242, 254, 0.08) 0%, rgba(0, 0, 0, 0) 70%);
  border-radius: 20px;
}

.hero-title {
  font-family: 'Outfit', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.7) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: rgba(255, 255, 255, 0.6);
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Search & Filters */
.filter-section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.25rem;
  border-radius: 14px;
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
  color: rgba(255, 255, 255, 0.35);
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 0.9rem 1rem 0.9rem 3rem;
  color: #ffffff;
  font-size: 1rem;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.search-input:focus {
  background: rgba(255, 255, 255, 0.05);
  border-color: #00f2fe;
  box-shadow: 0 0 0 4px rgba(0, 242, 254, 0.15);
}

.store-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.95rem;
  min-width: 220px;
}

.filter-label {
  font-weight: 500;
}

.filter-select {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  color: #ffffff;
  padding: 0.6rem 1.25rem;
  font-size: 0.95rem;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.filter-select:focus {
  border-color: #00f2fe;
}

/* Vitrine Grid */
.vitrine-grid {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.vitrine-card {
  background: rgba(18, 18, 24, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

.vitrine-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 242, 254, 0.25);
  box-shadow: 0 12px 40px rgba(0, 242, 254, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 1.25rem;
}

.card-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.5px;
}

.card-date {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
}

/* Product Row layout inside card */
.products-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.product-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  position: relative;
  transition: all 0.2s ease;
}

.product-item:hover {
  background: rgba(255, 255, 255, 0.035);
  border-color: rgba(255, 255, 255, 0.08);
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
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.badge-value {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.25);
}

.badge-premium {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.25);
}

.image-wrapper {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #161622;
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
  color: #ffffff;
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
  border-top: 1px solid rgba(255, 255, 255, 0.04);
  padding-top: 0.75rem;
}

.product-store {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
}

.product-price {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
}

.btn-buy {
  background: #ffffff;
  color: #0c0c12;
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
  background: #00f2fe;
  color: #0c0c12;
  box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
}

/* Card Footer */
.card-footer {
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 1.5rem;
}

.btn-detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  color: #ffffff;
  padding: 0.8rem 1.75rem;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-detail:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: #00f2fe;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 1rem;
  background: rgba(255, 255, 255, 0.01);
  border: 1px dashed rgba(255, 255, 255, 0.05);
  border-radius: 16px;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.5);
}

/* Skeletons */
.skeletons-grid {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.skeleton-card {
  height: 480px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.skeleton-header {
  height: 32px;
  width: 50%;
  background: rgba(255,255,255,0.04);
  border-radius: 4px;
}

.skeleton-products {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  flex-grow: 1;
}

.skeleton-product {
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
}

.skeleton-button {
  height: 44px;
  width: 200px;
  align-self: center;
  background: rgba(255,255,255,0.04);
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
