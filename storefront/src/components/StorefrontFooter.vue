<template>
  <footer class="storefront-footer">
    <div class="footer-container">
      <div class="footer-brand">
        <span class="brand-accent">É bom?</span>
      </div>
      <p class="footer-disclaimer">
        <strong>Divulgação de Afiliados:</strong> Como associado ou parceiro do Mercado Livre, ganhamos uma pequena comissão por compras qualificadas através de nossos links, sem custo adicional para você. Todas as análises são geradas de forma autônoma com apoio de inteligência artificial baseada em dados reais dos produtos.
      </p>
      <div class="footer-divider"></div>
      <p class="footer-copy">
        &copy; 2026 É bom? - <a href="https://www.ehbom.com.br" target="_blank" style="color: inherit; text-decoration: underline;">www.ehbom.com.br</a>. Desenvolvido para máxima performance e velocidade. Todos os direitos reservados.
      </p>
    </div>
  </footer>
</template>

<style scoped>
.storefront-footer {
  background: #0d0d12;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding: 3rem 1.5rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.5rem;
}

.footer-brand {
  font-family: 'Outfit', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffffff;
}

.brand-accent {
  background: linear-gradient(135deg, #0072ff 0%, #00ff87 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-disclaimer {
  max-width: 800px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.4);
}

.footer-divider {
  width: 100%;
  max-width: 150px;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.footer-copy {
  color: rgba(255, 255, 255, 0.3);
}
</style>
