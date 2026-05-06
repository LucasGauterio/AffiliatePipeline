import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const distDir = path.join(__dirname, 'dist')
const publicDataFile = path.join(__dirname, 'public', 'data', 'posts.json')

console.log('🏁 Iniciando processo de pré-renderização SEO estática...')

// 1. Check if build directory exists
if (!fs.existsSync(distDir)) {
  console.error('❌ Erro: A pasta "dist/" não existe. Por favor, execute "npm run build" antes.')
  process.exit(1)
}

// 2. Read template and database
const templatePath = path.join(distDir, 'index.html')
const template = fs.readFileSync(templatePath, 'utf-8')

let posts = []
if (fs.existsSync(publicDataFile)) {
  try {
    posts = JSON.parse(fs.readFileSync(publicDataFile, 'utf-8'))
  } catch (err) {
    console.error('❌ Erro ao ler posts.json:', err)
    process.exit(1)
  }
} else {
  console.warn('⚠️ Alerta: posts.json não encontrado na pasta public. Gerando apenas home vazia.')
}

// Helper: Replace title and meta tags in head
const replaceHeadTags = (html, metaTags) => {
  // Clear any existing title
  let cleanHtml = html.replace(/<title>[^<]*<\/title>/i, '')
  // Clear any existing description metatag
  cleanHtml = cleanHtml.replace(/<meta name="description"[^>]*>/i, '')
  // Inject the new meta blocks before </head>
  return cleanHtml.replace('</head>', `${metaTags}\n</head>`)
}

// Helper: Inject static pre-rendered HTML into #app container
const injectAppContent = (html, content) => {
  return html.replace('<div id="app"></div>', `<div id="app">${content}</div>`)
}

// --- Home Page Pre-rendering ---
console.log('🏠 Pré-renderizando Home Page...')
const homeMeta = `
  <title>Vitrine de Recomendações Inteligentes | AffiliatePipeline</title>
  <meta name="description" content="Sua vitrine de comparativos de eletrônicos e tecnologia. Análises profundas geradas por IA com os melhores links de afiliado." />
  <meta property="og:title" content="Vitrine de Recomendações Inteligentes | AffiliatePipeline" />
  <meta property="og:description" content="Sua vitrine de comparativos de eletrônicos e tecnologia. Análises profundas geradas por IA com os melhores links de afiliado." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://vitrine.pipeline.com.br/" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Vitrine de Recomendações Inteligentes | AffiliatePipeline" />
  <meta name="twitter:description" content="Sua vitrine de comparativos de eletrônicos e tecnologia. Análises profundas geradas por IA com os melhores links de afiliado." />
`

const homeStaticContent = `
  <header style="text-align:center; padding: 2rem;">
    <h1>Vitrine de Recomendações Inteligentes</h1>
    <p>Comparativos detalhados de produtos para simplificar sua decisão de compra.</p>
  </header>
  <main style="max-width: 800px; margin: 0 auto; padding: 1rem;">
    <h2>Análises e Comparativos Disponíveis:</h2>
    <ul style="line-height: 2;">
      ${posts.map(post => `
        <li>
          <a href="/posts/${post.slug}"><strong>${post.title}</strong></a> - Publicado em ${new Date(post.date).toLocaleDateString('pt-BR')}
        </li>
      `).join('')}
    </ul>
  </main>
`

let homeHtml = replaceHeadTags(template, homeMeta)
homeHtml = injectAppContent(homeHtml, homeStaticContent)
fs.writeFileSync(templatePath, homeHtml)
console.log('✅ Home Page pré-renderizada com sucesso em dist/index.html!')


// --- Detail Pages Pre-rendering ---
posts.forEach(post => {
  console.log(`📄 Pré-renderizando post: /posts/${post.slug}...`)
  
  const siteUrl = 'https://vitrine.pipeline.com.br'
  const postUrl = `${siteUrl}/posts/${post.slug}`
  const pageTitle = `${post.title} | AffiliatePipeline`
  const pageDescription = `Análise comparativa completa: ${post.title}. Veja nossa seleção de modelos: Mais Barato, Custo-Benefício e Premium.`
  const coverImage = post.products[0]?.image_url || `${siteUrl}/favicon.svg`

  // Construct JSON-LD schema
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": pageTitle,
    "description": pageDescription,
    "url": postUrl,
    "about": post.products.map(p => ({
      "@type": "Product",
      "name": p.title,
      "image": p.image_url,
      "offers": {
        "@type": "Offer",
        "price": p.price,
        "priceCurrency": "BRL",
        "url": p.link,
        "seller": {
          "@type": "Organization",
          "name": p.store
        },
        "availability": "https://schema.org/InStock"
      }
    }))
  }

  const postMeta = `
    <title>${pageTitle}</title>
    <meta name="description" content="${pageDescription}" />
    <meta property="og:title" content="${pageTitle}" />
    <meta property="og:description" content="${pageDescription}" />
    <meta property="og:url" content="${postUrl}" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="${coverImage}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${pageTitle}" />
    <meta name="twitter:description" content="${pageDescription}" />
    <meta name="twitter:image" content="${coverImage}" />
    <script type="application/ld+json">
      ${JSON.stringify(schema, null, 2)}
    </script>
  `

  const postStaticContent = `
    <main style="max-width: 1000px; margin: 0 auto; padding: 2rem;">
      <a href="/">← Voltar para a Vitrine</a>
      <header style="margin: 2rem 0; border-bottom: 1px solid #eee; padding-bottom: 1rem;">
        <h1>${post.title}</h1>
        <p>Publicado em ${new Date(post.date).toLocaleDateString('pt-BR')}</p>
      </header>
      
      <section style="margin: 3rem 0;">
        <h2>Comparativo de Modelos Selecionados</h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem; text-align: left;">
          <thead>
            <tr style="border-bottom: 2px solid #ddd; background: #f9f9f9;">
              <th style="padding: 10px;">Categoria</th>
              <th style="padding: 10px;">Produto</th>
              <th style="padding: 10px;">Preço</th>
              <th style="padding: 10px;">Loja</th>
              <th style="padding: 10px;">Link</th>
            </tr>
          </thead>
          <tbody>
            ${post.products.map(p => `
              <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;"><strong>${p.badge}</strong></td>
                <td style="padding: 10px;">${p.title}</td>
                <td style="padding: 10px;">R$ ${parseFloat(p.price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                <td style="padding: 10px;">${p.store}</td>
                <td style="padding: 10px;"><a href="${p.link}" target="_blank">Acessar Oferta</a></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </section>

      <article style="line-height: 1.8; font-size: 1.1rem;">
        <h2>Análise Completa da nossa Curadoria</h2>
        <div>${post.content}</div>
      </article>
    </main>
  `

  let postHtml = replaceHeadTags(template, postMeta)
  postHtml = injectAppContent(postHtml, postStaticContent)

  // Output to dist/posts/[slug]/index.html
  const postOutputDir = path.join(distDir, 'posts', post.slug)
  fs.mkdirSync(postOutputDir, { recursive: true })
  fs.writeFileSync(path.join(postOutputDir, 'index.html'), postHtml)
  console.log(`✅ Post pré-renderizado com sucesso em dist/posts/${post.slug}/index.html!`)
})

console.log('🚀 Todo o conteúdo estático foi pré-renderizado e otimizado para SEO com sucesso!')
