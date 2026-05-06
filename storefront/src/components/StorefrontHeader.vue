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
      </nav>
    </div>
  </header>
</template>

<style scoped>
.storefront-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(18, 18, 24, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
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
  gap: 1.5rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
}

.nav-link:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: #00ff87;
  background: rgba(0, 255, 135, 0.08);
}
</style>
