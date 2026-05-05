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
