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
