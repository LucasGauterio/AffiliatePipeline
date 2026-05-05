# Affiliate Pipeline & WordPress Integration

Pipeline de automação para pesquisa, geração e publicação de posts de afiliados (Amazon e Mercado Livre) utilizando inteligência artificial (Google Gemini).

## Bloco 1: Pré-Requisitos e Stack
Para contribuir ou executar o projeto, você precisará ter instalado em sua máquina:
- **Docker e Docker Compose** (Para subir a malha local do CMS e Python).
- **Terraform CLI** (Para subir as atualizações na nuvem do Google).

## Bloco 2: Rodando Localmente (Local Dev)
Toda a infraestrutura de desenvolvimento está encapsulada em contêineres Docker.

1. **Subir a Infraestrutura Base:**
   ```bash
   docker-compose up -d
   ```
   *Isso levantará os serviços: `db` (MySQL), `wordpress` (Porta 8080) e o `python-app`.*

2. **Setup do CMS Local:**
   - Acesse `http://localhost:8080` no navegador.
   - Siga a instalação básica ("Famous 5-Minute Install").
   - Instale o plugin **Advanced Custom Fields (ACF)** e configure os 12 campos necessários para o post.
   - Gere uma *Application Password* no perfil de usuário do WordPress.

3. **Configuração de Variáveis:**
   - Copie o arquivo `.env.example` para `.env`.
   - Adicione suas chaves simuladas (Mock) e preencha a URL interna do WordPress (`http://wordpress:80`) e a *Application Password* obtida no passo anterior.

4. **Executando a Suíte TDD (Testes):**
   Todos os testes rodam dentro do container isolado:
   ```bash
   docker-compose run --rm python-app pytest
   ```

## Bloco 3: Deploy Cloud via Terraform
O provisionamento da arquitetura serverless no Google Cloud é gerido por **Infrastructure as Code (IaC)**.

1. **Iniciando a Infraestrutura:**
   Acesse a pasta `/infra` e aplique os manifestos:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```
   *Isto criará o Artifact Registry, os Segredos, o Cloud Run Job e o Cloud Scheduler.*

2. **Deploy do Código Fonte:**
   Após a infraestrutura criada, construa a imagem de produção e faça o push:
   ```bash
   docker build -t us-central1-docker.pkg.dev/SEU_PROJETO/affiliate-pipeline-repo/python-app:latest -f Dockerfile.prod .
   docker push us-central1-docker.pkg.dev/SEU_PROJETO/affiliate-pipeline-repo/python-app:latest
   ```
