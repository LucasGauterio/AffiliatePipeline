# Affiliate Pipeline & Vue.js 3 Static Storefront

Pipeline de automação serverless para pesquisa, geração e publicação de comparativos de produtos de afiliados (Amazon e Mercado Livre) utilizando Inteligência Artificial (Google Gemini) integrada a uma vitrine estática moderna de altíssima performance construída em **Vue 3, Vite, e Node.js (SSG)**.

---

## 🛠️ Stack Tecnológica
*   **Backend**: Python 3.10 (Scrapers, Gemini SDK, Bleach, Unittests).
*   **Frontend**: Vue.js 3 (Composition API), Vite, Lucide Icons, Vanilla CSS (Tema Escuro Glassmorphism).
*   **SEO Engine**: Node.js (Pre-renderizador SSG de arquivos `.html` estáticos com injeção automática de metadados OpenGraph e Schema.org JSON-LD).
*   **Local Dev**: Docker, Docker Compose (Isolamento completo e hot-reloading).
*   **Produção**: Google Cloud Platform (Cloud Storage para hospedagem estática, Cloud Run Jobs, Cloud Scheduler, Secret Manager) e IaC via **Terraform**.

---

## 💻 Ambiente de Desenvolvimento Local (Local Dev)

Toda a infraestrutura de desenvolvimento está conteinerizada, garantindo que você não precise instalar nada localmente além de **Docker** e **Docker Compose**.

### 1. Configurando Variáveis de Ambiente
Copie o arquivo de exemplo de variáveis de ambiente e configure sua API Key do Google Gemini:
```bash
cp .env.example .env
```
*(Certifique-se de preencher `GEMINI_API_KEY` com uma chave válida para chamadas reais, ou os testes rodarão automaticamente no modo Mock).*

---

### 2. Rodando o Backend (Pipeline Python)

Os testes e execução da pipeline rodam dentro do container isolado `python-app`.

*   **Executar Testes de TDD (Pytest + Coverage)**:
    ```bash
    docker-compose run --rm python-app pytest
    ```
*   **Executar a Pipeline Manualmente**:
    ```bash
    docker-compose run --rm python-app python src/main.py
    ```

---

### 3. Rodando o Frontend (Vitrine Vue 3)

O frontend possui hot-reloading ativo que sincroniza qualquer alteração de design instantaneamente com o navegador.

*   **Subir Servidor de Desenvolvimento via Docker-Compose** (Porta `5173`):
    ```bash
    docker-compose up storefront
    ```
    *Acesse `http://localhost:5173` no seu navegador.*

*   **Alternativa (Execução Local Direta com Node)**:
    ```bash
    cd storefront
    npm install
    npm run dev
    ```

---

### 4. Compilação e Pré-Renderização Estática (SSG)

Ao executar a compilação de produção, o compilador Vite gerará a aplicação e, imediatamente após, o motor `prerender.js` lerá o banco de dados local `posts.json` para pré-compilar caminhos físicos indexados para cada análise.

1.  Acesse a pasta da vitrine:
    ```bash
    cd storefront
    ```
2.  Execute o script de compilação:
    ```bash
    npm run build
    ```
    *Este comando rodará o Vite build e na sequência acionará o script `node prerender.js` automaticamente. Os arquivos prontos para deploy estático estarão na pasta `storefront/dist/`.*

3.  Para testar a versão otimizada de produção localmente na porta `4173`:
    ```bash
    npm run preview
    ```

---

## ☁️ Implantação em Produção (GCP & Terraform)

O provisionamento da infraestrutura em nuvem na Google Cloud Platform é feito estritamente como código (IaC).

### 1. Provisionando Recursos com Terraform
Acesse a pasta de infraestrutura e aplique as configurações:
```bash
cd infra
terraform init
terraform plan
terraform apply
```
*Este comando criará o bucket público do GCS configurado para hospedagem estática, os repositórios Artifact Registry para a pipeline, as chaves do Secret Manager, o Cloud Run Job, e o Cloud Scheduler.*

### 2. Deploy da Imagem Backend (Python Job)
Construa e publique a imagem Docker do backend para que o Cloud Run a execute:
```bash
docker build -t us-central1-docker.pkg.dev/SEU_PROJETO/affiliate-pipeline-repo/python-app:latest -f Dockerfile.prod .
docker push us-central1-docker.pkg.dev/SEU_PROJETO/affiliate-pipeline-repo/python-app:latest
```

### 3. Deploy do Site Estático (Vue Storefront)
Compile o site estático gerando os arquivos de produção e envie-os diretamente para o bucket público do Google Cloud Storage:
```bash
cd storefront
npm run build
gsutil rsync -R dist gs://affiliate-pipeline-storefront-SEU_PROJETO
```
*O site estará disponível publicamente através do endereço de hospedagem de site do GCS instantaneamente, escalando infinitamente a custo quase nulo e com 100/100 de pontuação de SEO.*
