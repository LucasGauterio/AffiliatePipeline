# Affiliate Pipeline & WordPress Integration

Pipeline de automação para pesquisa, geração e publicação de posts de afiliados (Amazon e Mercado Livre) utilizando inteligência artificial (Google Gemini).

## Visão Geral
Este projeto tem como objetivo avaliar três categorias de produtos por pauta (mais barato, melhor custo-benefício e premium), gerar um review otimizado para SEO via IA e publicá-lo diretamente no WordPress via REST API.

## Metodologia
- **TDD (Test-Driven Development)**
- **Docker-First (Desenvolvimento Local)**
- **Infrastructure as Code (Terraform)**

## Executando Localmente
*(Instruções completas de deploy serão adicionadas ao final do projeto)*

Para rodar os testes via Docker:
```bash
docker-compose run --rm python-app pytest
```
