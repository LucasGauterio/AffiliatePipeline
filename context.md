# Contexto do Projeto: Affiliate Pipeline

Este arquivo serve como um registro vivo das implementações e decisões arquiteturais.

## Fase 1: Setup do Ambiente e Git
- **Data:** 2026-05-04
- **Resumo:** Repositório Git inicializado. Estrutura base (`src`, `tests`, `config`, `infra`) criada. Adicionados `requirements.txt` e `requirements-dev.txt` com dependências atualizadas. Ambiente Docker configurado (`docker-compose.yml` e `Dockerfile.dev`) com serviços para MySQL, WordPress e Python em rede isolada. Scripts de teste (`run_tests.ps1` e `pytest.ini`) configurados e versionamento via Git iniciado com commits granulares.

## Fase 2: Configurações e Segredos
- **Data:** 2026-05-04
- **Resumo:** Implementado o módulo `config/settings.py` para carregar variáveis de ambiente. Implementado `config/secrets_manager.py` integrando com o SecretManagerServiceClient do GCP em ambiente de produção, e com fallback para variáveis locais em ambiente de desenvolvimento. TDD seguido com suíte de testes passando com mocks completos do cliente do Google Cloud.

## Fase 3: Módulo de Pauta (Discovery)
- **Data:** 2026-05-04
- **Resumo:** Implementado o arquivo de dados local `data/topics.json` com os nichos de teste. Construído o módulo `src/discovery.py` guiado por TDD para ler os tópicos e verificar contra o `history.json` para evitar repetições, e um método para registrar conclusão.

## Fase 4: Scrapers e Mocks
- **Data:** 2026-05-05
- **Resumo:** Implementada a classe abstrata `BaseScraper` para guiar o formato da raspagem. Implementados os scrapers em modo mock (`MercadoLivreScraper` e `AmazonScraper`) retornando 3 produtos (barato, médio, premium) de acordo com as diretrizes do projeto. Todo o desenvolvimento foi coberto por testes unitários guiados por TDD.

## Fase 5: Módulo de IA (Gemini)
- **Data:** 2026-05-05
- **Resumo:** Implementado o módulo `src/ai_generator.py` contendo a classe `AIGenerator` que orquestra a chamada para a API do Google Gemini (usando o SDK `google-generativeai`). O sistema recebe a pauta e a lista de produtos, formatando-os em um prompt estruturado para gerar o título e o conteúdo HTML da postagem. Implementada a validação da resposta em JSON e os testes TDD através de mocks da API do Gemini.

## Fase 6: Módulo de Publicação (WordPress)
- **Data:** 2026-05-05
- **Resumo:** Implementada a classe `WordPressPublisher` no módulo `src/publisher.py` usando `requests` para se comunicar via Basic Auth com a REST API do WordPress. O módulo inclui mapeamento dos 3 produtos para os campos do plugin ACF e utiliza a biblioteca `bleach` para sanitizar rigorosamente o HTML recebido do Gemini (mitigando ataques XSS). Testes guiados por TDD usando mock do `requests.post`.

## Fase 7: Orquestração (Main)
- **Data:** 2026-05-05
- **Resumo:** Implementado o script principal `src/main.py` que age como ponto de entrada do Cloud Run Job. Ele orquestra sequencialmente: busca da pauta pendente (`discovery.py`), coleta dos dados no scraper (`mercadolivre.py`), envio ao LLM (`ai_generator.py`) e publicação no CMS (`publisher.py`), finalizando com a marcação de conclusão no histórico. A orquestração inteira foi testada (TDD) via mocks para garantir que não haja chamadas reais de rede durante a execução dos testes.

## Fase 8: Deploy IaC (Terraform) e Docs Finais
- **Data:** 2026-05-05
- **Resumo:** Finalizada a conteinerização criando o `Dockerfile.prod` otimizado para a imagem de produção (Cloud Run Job). Criados os manifestos do Terraform (`main.tf`, `variables.tf`, `outputs.tf`) estabelecendo toda a infraestrutura baseada no Google Cloud Platform: Artifact Registry para a imagem Docker, Secret Manager para variáveis seguras, Cloud Run Job e Cloud Scheduler para execução diária. O `README.md` foi finalizado com as instruções completas para rodar TDD local e realizar o deploy em nuvem através de IaC. O projeto está concluído.

## Fase 9: Melhorias de UI/UX e Frontend
- **Data:** 2026-05-05
- **Resumo:** A lacuna visual foi preenchida com a implementação de ponta a ponta de imagens no pipeline. Os scrapers (`mercadolivre.py`, `amazon.py`) e o `publisher.py` foram atualizados para coletar e transmitir o atributo `image_url` para o payload do ACF, devidamente guiados por TDD. No frontend, desenvolvemos o plugin customizado `affiliate-renderer` com PHP e um CSS responsivo, de carregamento otimizado (sem bibliotecas de terceiros) e de alto apelo visual (botões vibrantes, badges, grid em desktop e single-column em mobile). Os dados agora são renderizados com perfeição no final de cada artigo.

## Fase 10: Portabilidade e Auto-Configuração Automática
- **Data:** 2026-05-06
- **Resumo:** Implementado o serviço `wordpress-setup` com o script de inicialização `wp-setup.sh`. O script realiza checagem de conexão nativa com o banco de dados via PHP, instalação silenciosa do WordPress, injeção robusta do usuário `developer` com senha de aplicação autônoma e sincronizada, instalação automática e ativação de plugins (`advanced-custom-fields`, `affiliate-renderer`), configuração do tema `accelerate` e reescrita de links permanentes para `postname` com flush automático de regras do Apache.

## Fase 11: Enriquecimento de Metadados e Compartilhamento Social
- **Data:** 2026-05-06
- **Resumo:** Criado o sistema de compartilhamento social reativo em JavaScript (`script.js`) integrado ao plugin `affiliate-renderer.php`. Implementados botões de compartilhamento responsivos para WhatsApp, Facebook, Twitter, LinkedIn e um botão interativo de cópia de link de área de transferência com transição de estados ("✓ Copiado!"). Integradas tags dinâmicas de OpenGraph (OG) e Twitter Cards injetadas via head do WordPress (`wp_head`), utilizando dinamicamente a imagem do primeiro produto em destaque como thumbnail de compartilhamento.

## Fase 12: Vitrine e Grade de Comparação de Produtos
- **Data:** 2026-05-06
- **Resumo:** Redesenhada a lógica de loops de exibição de conteúdo no WordPress. Nas páginas de listas e arquivos (`!is_single()`), o plugin intercepta o loop padrão para substituir o resumo do artigo por um painel de comparação horizontal ("Comparativo Simplificado") que agrupa side-by-side as opções "Mais Barata", "Custo-Benefício" e "Premium" com imagens, preços, loja e links diretos de afiliados, mantendo um link direcionador para a análise completa. Nos posts individuais (`is_single()`), exibe a grade comparativa detalhada e a barra social de compartilhamento.

## Fase 13: Controle de Qualidade, Automação de Campos e Conclusão
- **Data:** 2026-05-06
- **Resumo:** Corrigido o bug de teste unitário `test_publisher.py` resolvendo a NameError de escopo. Implementada a auto-definição e registro programático das tabelas de campos customizados do ACF via `acf_add_local_field_group` com exposição completa para a API REST (`show_in_rest => true`) e compatibilidade dinâmica com conexões HTTP locais via filtro. Rodada a suíte completa de testes no contêiner com 100% de sucesso e 97% de cobertura. A conformidade visual de ponta a ponta e a interatividade dos widgets foram verificadas com sucesso através de testes automatizados via browser headless.

## Fase 14: Migração para Arquitetura JAMstack e Vitrine Vue.js 3
- **Data:** 2026-05-06
- **Resumo:** Refatoração completa de toda a arquitetura da aplicação para eliminar a dependência do CMS WordPress e banco de dados relacional MySQL. 
  1. No backend, reescrevemos o publicador para a classe `StaticPublisher` em `src/publisher.py` (com 100% de testes unitários passando em pytest com cobertura de 82%), salvando as comparações como um banco de dados de arquivos JSON estruturados. O módulo suporta salvamento local e escrita direta e transacional na nuvem (GCP Cloud Storage) pelo prefixo de protocolo `gs://`.
  2. No frontend, scaffoldamos uma aplicação de vitrine em Vue 3 + Vite na pasta `storefront/` e construímos um Design System premium com tema escuro glassmorphic, micro-animações, e filtros integrados por texto e lojas na `HomeView.vue`, além de páginas ricas de análise em `ComparisonDetailView.vue` e botões de compartilhamento integrados com feedback animado no `SocialShareWidget.vue`.
  3. Desenvolvemos o motor de SEO pre-render (`storefront/prerender.js`) acionado pós-build para pré-renderizar páginas estáticas `.html` em tempo de build para cada slug com injeção automática de tags OpenGraph ricas e dados estruturados Schema.org JSON-LD (e-commerce Product/Offer) para indexação rápida no Googlebot.
  4. Atualizamos a infraestrutura IaC (`infra/main.tf`) removendo variáveis do WordPress e provisionando um bucket no Google Cloud Storage configurado para hospedagem estática, garantindo permissões granulares de escrita para o Cloud Run Job.
  5. Verificamos a conformidade de compilação, build estático, integridade do pre-render SEO e fluxos de navegação e compartilhamento no localhost através de testes visuais robustos com subagente browser. O projeto foi completamente modernizado para o padrão serverless estático.
