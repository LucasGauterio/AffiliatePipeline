# Lista de Tarefas: Vitrine Estática Vue.js (Affiliate Pipeline)

Este arquivo substitui a versão WordPress e serve como nosso checklist unificado para a migração rumo a uma vitrine estática em Vue 3, servida de forma serverless e 100% otimizada para SEO.

> **REGRA DE OURO (CICLO POR TAREFA):**
> 1. Escrever o **Failing Test (TDD)** no Python para qualquer mudança no pipeline.
> 2. Implementar o código e fazer o teste passar.
> 3. Fazer o **Commit no Git** (`git commit -m "..."`) com o escopo da tarefa.
> 4. Atualizar o arquivo **`context.md`** ao concluir cada Fase.

---

## Fase 1: Limpeza do Ambiente e Reorganização
- `[x]` 1.1. Modificar o `docker-compose.yml` para remover os serviços `db`, `wordpress` e `wordpress-setup`.
- `[x]` 1.2. Remover arquivos legados do WordPress (`wp-content` e `infra/wp-setup.sh`) para manter a árvore limpa.
- `[x]` 1.3. Realizar o commit de limpeza inicial do ambiente.

## Fase 2: Redesenho da Publicação para JSON Estático (TDD)
- `[x]` 2.1. Implementar testes unitários em `tests/test_publisher.py` cobrindo a gravação de JSON, geração de slugs e atualização de posts (TDD).
- `[x]` 2.2. Reescrever `src/publisher.py` como `StaticPublisher`, gravando os comparativos em `storefront/public/data/posts.json` com higienização via `bleach`.
- `[x]` 2.3. Atualizar `src/main.py` e certificar que a suíte `pytest` de testes unitários passe com 100% de sucesso.
- `[x]` 2.4. Realizar o commit das alterações do publicador estático.

## Fase 3: Inicialização da Vitrine Vue.js 3 + Vite
- `[x]` 3.1. Inicializar o projeto Vue 3 + Vite na pasta `storefront`: `npm create vite@latest storefront -- --template vue`.
- `[x]` 3.2. Instalar dependências essenciais: `vue-router` e `lucide-vue-next`.
- `[x]` 3.3. Estruturar diretórios internos (`components/`, `views/`, `router/`, `data/`) e configurar o roteamento (`/` para Home, `/posts/:slug` para Detalhes).
- `[/]` 3.4. Realizar o commit do scaffolding da vitrine.

## Fase 4: Desenvolvimento da Página Inicial (Vitrine Curada)
- `[x]` 4.1. Criar o design system em Vanilla CSS em `storefront/src/style.css` (tema escuro com glassmorphism, tipografia Outfit, efeitos hover e badges de destaque).
- `[x]` 4.2. Desenvolver os componentes globais de layout: `StorefrontHeader.vue` e `StorefrontFooter.vue`.
- `[x]` 4.3. Implementar `HomeView.vue` apresentando o grid de comparativos lado a lado com fotos, preços, lojas de origem, barra de pesquisa e filtros interativos.
- `[/]` 4.4. Realizar o commit da página inicial da vitrine.

## Fase 5: Detalhes do Comparativo & Compartilhamento Social
- `[x]` 5.1. Desenvolver `ComparisonDetailView.vue` renderizando o grid de comparação detalhado (Mais Barato, Custo-Benefício, Premium) e o texto de análise do Gemini.
- `[x]` 5.2. Construir `SocialShareWidget.vue` integrado com links sociais ativos e botão copiar link com feedback animado ("✓ Copiado!").
- `[x]` 5.3. Ajustar responsividade Mobile-First extrema para leitura confortável.
- `[/]` 5.4. Realizar o commit dos widgets e detalhamento.

## Fase 6: Engine de Pré-Renderização Automatizada para SEO
- `[ ]` 6.1. Desenvolver `storefront/prerender.js` (Node) para ler `posts.json` e exportar arquivos `.html` estáticos em `dist/` para cada rota.
- `[ ]` 6.2. Injetar metadados SEO ricos em tempo de build (Title, Description, OpenGraph, Twitter Cards e Schema.org) no cabeçalho de cada página estática.
- `[ ]` 6.3. Integrar a execução do pré-renderizador no pipeline do `package.json` pós-build (`npm run build`).
- `[ ]` 6.4. Realizar o commit do pré-renderizador SEO.

## Fase 7: Ambiente Docker para Desenvolvedor (Vite Dev Server)
- `[ ]` 7.1. Desenvolver o `storefront/Dockerfile.dev` com Node para rodar o Vite local.
- `[ ]` 7.2. Configurar o serviço `storefront` no `docker-compose.yml` mapeando volumes para hot-reloading e expondo a porta 8080.
- `[ ]` 7.3. Subir e testar o fluxo de desenvolvimento interativo local.
- `[ ]` 7.4. Realizar o commit das configurações Docker.

## Fase 8: Infraestrutura Cloud Serverless Estática (IaC)
- `[ ]` 8.1. Modificar `infra/main.tf` para remover variáveis do WP e provisionar um Bucket do Google Cloud Storage (GCS) como hospedagem de site estático.
- `[ ]` 8.2. Associar permissões de escrita/leitura do bucket para a Conta de Serviço (SA) do Cloud Run Job.
- `[ ]` 8.3. Ajustar o Job no Terraform para sincronizar e enviar dados gerados direto para o Bucket de produção.
- `[ ]` 8.4. Realizar o commit das atualizações IaC.

## Fase 9: Controle de Qualidade e Validação End-to-End
- `[ ]` 9.1. Executar suíte completa de testes `pytest` e cobertura de código.
- `[ ]` 9.2. Executar build de produção do Vue e auditar as pastas e arquivos em `dist/` para comprovar os metadados e tags SEO estáticas.
- `[ ]` 9.3. Validar a experiência de usuário e interações de ponta a ponta na porta do localhost.
- `[ ]` 9.4. Realizar o commit final de validação.

## Fase 10: Atualização das Especificações e Conclusão
- `[ ]` 10.1. Atualizar o arquivo `g:\Documents\Utils\AffiliatePipeline\spec.md` refletindo o novo motor de exibição Vue.
- `[ ]` 10.2. Atualizar `g:\Documents\Utils\AffiliatePipeline\context.md` consolidando a cronologia de migração.
- `[ ]` 10.3. Reescrever o `g:\Documents\Utils\AffiliatePipeline\README.md` com instruções sobre o ambiente de desenvolvimento Vue, build estático, pré-renderização e deploy GCS via Terraform.
- `[ ]` 10.4. Commit final de encerramento do projeto.
