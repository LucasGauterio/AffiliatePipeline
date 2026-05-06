<script setup>
import { ref, onMounted } from 'vue'
import { ArrowLeft, Tag, Award, Gem, ExternalLink, Calendar } from 'lucide-vue-next'
import SocialShareWidget from '../components/SocialShareWidget.vue'

const props = defineProps({
  slug: {
    type: String,
    required: true
  }
})

const post = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('/data/posts.json')
    if (res.ok) {
      const posts = await res.json()
      post.value = posts.find(p => p.slug === props.slug)
    }
  } catch (err) {
    console.error('Error fetching post:', err)
  } finally {
    loading.value = false
  }
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
  <div class="detail-view">
    <!-- Navigation Back -->
    <router-link to="/" class="btn-back">
      <ArrowLeft :size="16" />
      <span>Voltar para a Vitrine</span>
    </router-link>

    <!-- Loading State -->
    <div v-if="loading" class="skeleton-detail">
      <div class="skeleton-title"></div>
      <div class="skeleton-meta"></div>
      <div class="skeleton-grid"></div>
      <div class="skeleton-text"></div>
    </div>

    <!-- Page Not Found -->
    <div v-else-if="!post" class="not-found">
      <h2>Comparativo não encontrado</h2>
      <p>O comparativo solicitado não foi encontrado em nossos servidores.</p>
      <router-link to="/" class="btn-home">Ver Outros Comparativos</router-link>
    </div>

    <!-- Product Showcase Detail -->
    <article v-else class="post-detail">
      <header class="detail-header">
        <h1 class="detail-title">{{ post.title }}</h1>
        <div class="detail-meta">
          <div class="meta-item">
            <Calendar :size="16" />
            <span>Publicado em {{ new Date(post.date).toLocaleDateString('pt-BR') }}</span>
          </div>
        </div>
      </header>

      <!-- Main Comparison Grid -->
      <section class="comparison-block">
        <h2 class="section-title">Comparativo Simplificado</h2>
        <div class="comparison-grid">
          <div v-for="product in post.products" :key="product.badge" class="comparison-card">
            
            <!-- Badge -->
            <div class="badge-ribbon" :class="getBadgeClass(product.badge)">
              <component :is="getBadgeIcon(product.badge)" :size="14" />
              <span>{{ product.badge }}</span>
            </div>

            <!-- Product Image -->
            <div class="product-img-box">
              <img :src="product.image_url" :alt="product.title" class="product-img" />
            </div>

            <!-- Title & Store -->
            <div class="product-details">
              <span class="product-store">{{ product.store }}</span>
              <h3 class="product-title">{{ product.title }}</h3>
            </div>

            <!-- Price -->
            <div class="price-section">
              <span class="price-label">Menor Preço Encontrado</span>
              <span class="price-value">R$ {{ parseFloat(product.price).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
            </div>

            <!-- Action Button -->
            <a :href="product.link" target="_blank" rel="noopener noreferrer" class="btn-shop">
              <span>Ir para a Loja</span>
              <ExternalLink :size="16" />
            </a>
          </div>
        </div>
      </section>

      <!-- Deep Dive AI Content -->
      <section class="analysis-block">
        <h2 class="section-title">Análise Completa da nossa Curadoria</h2>
        <div class="analysis-content html-render" v-html="post.content"></div>
      </section>

      <!-- Social Shares -->
      <SocialShareWidget :title="post.title" />
    </article>
  </div>
</template>

<style scoped>
.detail-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: color 0.2s ease;
  align-self: flex-start;
}

.btn-back:hover {
  color: #00f2fe;
}

/* Header */
.detail-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 1.5rem;
}

.detail-title {
  font-family: 'Outfit', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -1px;
  color: #ffffff;
  margin: 0 0 0.75rem 0;
}

.detail-meta {
  display: flex;
  gap: 1.5rem;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

/* Section Title */
.section-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1.5rem;
  border-left: 3px solid #00f2fe;
  padding-left: 0.75rem;
}

/* Comparison Grid */
.comparison-block {
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 2rem;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.comparison-card {
  background: rgba(18, 18, 24, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  transition: all 0.2s ease;
}

.comparison-card:hover {
  border-color: rgba(0, 242, 254, 0.2);
  background: rgba(18, 18, 24, 0.85);
}

.badge-ribbon {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.75rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.2px;
  text-transform: uppercase;
  align-self: flex-start;
}

.badge-cheap {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.badge-value {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.badge-premium {
  background: rgba(139, 92, 246, 0.12);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.product-img-box {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #11111a;
  border-radius: 8px;
  padding: 1rem;
}

.product-img {
  max-height: 150px;
  max-width: 95%;
  object-fit: contain;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  flex-grow: 1;
}

.product-store {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
}

.product-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  line-height: 1.4;
}

.price-section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 1rem;
}

.price-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.price-value {
  font-size: 1.6rem;
  font-weight: 800;
  color: #ffffff;
}

.btn-shop {
  background: #ffffff;
  color: #0c0c12;
  text-decoration: none;
  font-weight: 700;
  border-radius: 8px;
  padding: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn-shop:hover {
  background: #00f2fe;
  color: #0c0c12;
  box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
}

/* Deep Dive Content (HTML render) */
.analysis-block {
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 2.5rem;
}

.html-render {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.05rem;
  line-height: 1.8;
}

/* Style injected HTML elements dynamically */
.html-render :deep(p) {
  margin-top: 0;
  margin-bottom: 1.5rem;
}

.html-render :deep(h2) {
  font-family: 'Outfit', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: #ffffff;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
}

.html-render :deep(h3) {
  font-family: 'Outfit', sans-serif;
  font-size: 1.3rem;
  font-weight: 600;
  color: #ffffff;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
}

.html-render :deep(strong) {
  color: #ffffff;
  font-weight: 600;
}

.html-render :deep(ul), .html-render :deep(ol) {
  padding-left: 1.5rem;
  margin-bottom: 1.5rem;
}

.html-render :deep(li) {
  margin-bottom: 0.5rem;
}

/* Not Found Page */
.not-found {
  text-align: center;
  padding: 5rem 1rem;
}

.btn-home {
  display: inline-block;
  background: #00f2fe;
  color: #0c0c12;
  font-weight: 700;
  text-decoration: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  transition: all 0.2s ease;
}

.btn-home:hover {
  box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
}

/* Skeleton loader */
.skeleton-detail {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.skeleton-title {
  height: 48px;
  width: 70%;
  background: rgba(255,255,255,0.03);
  border-radius: 4px;
}

.skeleton-meta {
  height: 20px;
  width: 250px;
  background: rgba(255,255,255,0.03);
  border-radius: 4px;
}

.skeleton-grid {
  height: 380px;
  background: rgba(255,255,255,0.02);
  border-radius: 12px;
}

.skeleton-text {
  height: 250px;
  background: rgba(255,255,255,0.01);
  border-radius: 12px;
}

/* Responsive */
@media (max-width: 900px) {
  .comparison-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .product-img-box {
    height: 160px;
  }
  .detail-title {
    font-size: 2rem;
  }
  .comparison-block, .analysis-block {
    padding: 1.5rem;
  }
}
</style>
