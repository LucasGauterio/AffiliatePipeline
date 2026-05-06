<script setup>
import { ref } from 'vue'
import { Share2, Link, MessageSquare, Facebook, Twitter, Linkedin } from 'lucide-vue-next'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const copied = ref(false)

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Falha ao copiar o link:', err)
  }
}

const getShareUrl = (platform) => {
  const url = encodeURIComponent(window.location.href)
  const text = encodeURIComponent(`Veja essa recomendação incrível: ${props.title}`)
  
  switch(platform) {
    case 'whatsapp':
      return `https://api.whatsapp.com/send?text=${text}%20${url}`
    case 'facebook':
      return `https://www.facebook.com/sharer/sharer.php?u=${url}`
    case 'twitter':
      return `https://twitter.com/intent/tweet?url=${url}&text=${text}`
    case 'linkedin':
      return `https://www.linkedin.com/sharing/share-offsite/?url=${url}`
    default:
      return '#'
  }
}
</script>

<template>
  <div class="social-share-widget">
    <div class="share-title-container">
      <Share2 :size="18" class="icon-share" />
      <span class="share-title">Gostou? Compartilhe com os amigos!</span>
    </div>
    
    <div class="share-buttons">
      <!-- WhatsApp -->
      <a :href="getShareUrl('whatsapp')" target="_blank" rel="noopener noreferrer" class="btn-share whatsapp" title="Compartilhar no WhatsApp">
        <MessageSquare :size="18" />
        <span class="btn-text">WhatsApp</span>
      </a>

      <!-- Facebook -->
      <a :href="getShareUrl('facebook')" target="_blank" rel="noopener noreferrer" class="btn-share facebook" title="Compartilhar no Facebook">
        <Facebook :size="18" />
        <span class="btn-text">Facebook</span>
      </a>

      <!-- Twitter / X -->
      <a :href="getShareUrl('twitter')" target="_blank" rel="noopener noreferrer" class="btn-share twitter" title="Compartilhar no Twitter/X">
        <Twitter :size="18" />
        <span class="btn-text">Twitter</span>
      </a>

      <!-- LinkedIn -->
      <a :href="getShareUrl('linkedin')" target="_blank" rel="noopener noreferrer" class="btn-share linkedin" title="Compartilhar no LinkedIn">
        <Linkedin :size="18" />
        <span class="btn-text">LinkedIn</span>
      </a>

      <!-- Copy Link -->
      <button @click="copyLink" class="btn-share copy-link" :class="{ 'copied': copied }" title="Copiar Link">
        <Link :size="18" v-if="!copied" />
        <span v-else class="copied-check">✓</span>
        <span class="btn-text">{{ copied ? 'Copiado!' : 'Copiar Link' }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.social-share-widget {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.25rem;
  margin-top: 2rem;
  box-shadow: 0 4px 20px var(--shadow-color);
}

.share-title-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
}

.icon-share {
  color: var(--accent-blue);
}

:root.dark .icon-share {
  color: var(--accent-green);
}

.share-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.share-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.btn-share {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  color: var(--text-main);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: var(--bg-panel);
  outline: none;
}

.btn-share:hover {
  transform: translateY(-2px);
  color: #ffffff;
}

.whatsapp:hover {
  background: #25d366;
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.25);
}

.facebook:hover {
  background: #1877f2;
  box-shadow: 0 4px 12px rgba(24, 119, 242, 0.25);
}

.twitter:hover {
  background: #1da1f2;
  box-shadow: 0 4px 12px rgba(29, 161, 242, 0.25);
}

.linkedin:hover {
  background: #0a66c2;
  box-shadow: 0 4px 12px rgba(10, 102, 194, 0.25);
}

.copy-link {
  background: rgba(0, 98, 255, 0.08);
  color: var(--accent-blue);
  border: 1px solid rgba(0, 98, 255, 0.12);
}

.copy-link:hover {
  background: var(--accent-blue) !important;
  color: #ffffff !important;
}

:root.dark .copy-link {
  background: rgba(0, 255, 135, 0.08);
  color: var(--accent-green);
  border: 1px solid rgba(0, 255, 135, 0.15);
}

:root.dark .copy-link:hover {
  background: var(--accent-green) !important;
  color: #0c0c12 !important;
}

.copy-link.copied {
  background: #10b981 !important;
  color: #ffffff !important;
  border-color: #10b981 !important;
}

.copied-check {
  font-weight: bold;
}

@media (max-width: 768px) {
  .social-share-widget {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.25rem;
  }
  .share-buttons {
    width: 100%;
  }
  .btn-share {
    flex-grow: 1;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .btn-text {
    display: none;
  }
  .btn-share {
    padding: 0.6rem 0.8rem;
  }
}
</style>
