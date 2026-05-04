# Specification: Affiliate Pipeline & WordPress Integration

## 1. Visão Geral (Overview)
O sistema tem como objetivo automatizar a pesquisa, geração de conteúdo e publicação de posts de comparação de produtos focados em afiliados (Amazon e Mercado Livre). Ele avalia três categorias por pauta: O mais barato, o melhor custo-benefício (médio) e o mais premium (caro).

## 2. Metodologia de Desenvolvimento
*   **Test-Driven Development (TDD):** Todo novo código ou funcionalidade deve começar com a criação de um teste unitário que falha ("failing test"). Somente após o teste falhar, a lógica de negócio deve ser implementada para fazê-lo passar, seguida de eventual refatoração.
*   **Docker-First (Local Dev):** O ambiente de desenvolvimento local será isolado via Docker (`docker-compose` e `Dockerfile.dev`). Nenhuma instalação de dependências Python será exigida na máquina *host*. Scripts utilitários encapsularão os comandos para execução de testes e do projeto dentro dos contêineres.
*   **Infrastructure as Code (IaC):** A implantação na nuvem (Google Cloud Platform) será estritamente automatizada usando ferramentas de IaC. Não haverá provisionamento "clicado" (manual).
*   **Controle de Versão Contínuo (Git/GitHub):** O projeto obrigatoriamente iniciará com a criação de um repositório Git. Ao final de **cada tarefa executada** (cada item do nosso checklist), deve-se fazer um commit atômico registrando o progresso e o resumo da implementação.
*   **Documentação Contínua:** Existe um compromisso estrito com a documentação em tempo real. O arquivo `context.md`, na raiz do projeto, será um documento vivo e atualizado ao final da execução de cada *Fase*.

## 3. Arquitetura da Solução
*   **Ambiente de Execução:** Google Cloud Platform (GCP).
*   **Computação:** Google Cloud Run Jobs (ideal para tarefas em lote que têm começo, meio e fim).
*   **Agendamento:** Google Cloud Scheduler (aciona o Cloud Run Job periodicamente).
*   **Segurança e Chaves:** Google Secret Manager (armazena senhas do WP, chaves de API da Amazon, Mercado Livre e Vertex AI).
*   **Inteligência Artificial:** Google Vertex AI (Gemini) via SDK.
*   **CMS / Frontend:** WordPress (Hospedado separadamente).

## 4. Diretrizes de UI/UX (Frontend WordPress)
*   **Mobile-First e Legibilidade:** O design do site deve ser pensado primeiramente para celulares. A tipografia deve ser perfeitamente legível.
*   **Alta Performance (Core Web Vitals):** O carregamento do site deve ser instantâneo. Devem ser evitadas interfaces complexas e plugins excessivos.
*   **Desktop Responsivo:** As três opções de produtos devem ser posicionadas em grades ou colunas interativas em desktops.

## 5. Estrutura de Exibição (WordPress + ACF)
Utilizaremos o plugin **Advanced Custom Fields (ACF)** para estruturar os dados.
*   **Produto 1 (Mais Barato):** `product_1_title`, `product_1_price`, `product_1_link`, `product_1_store`
*   **Produto 2 (Custo-Benefício):** `product_2_title`, `product_2_price`, `product_2_link`, `product_2_store`
*   **Produto 3 (Premium/Mais Caro):** `product_3_title`, `product_3_price`, `product_3_link`, `product_3_store`

## 6. Armazenamento de Dados e Estado (Data Storage)
*   **Repositório Principal (WordPress Database):** O WP atuará como o *Single Source of Truth* (única fonte da verdade) para exibição.
*   **Controle de Estado do Pipeline:** O pipeline em Python rastreará pautas publicadas via um arquivo **`history.json` armazenado no Google Cloud Storage** (ou localmente, em dev).
*   **Repositório de Mídias:** O site fará "hotlinking" seguro das miniaturas das lojas para poupar uso de disco do servidor.

## 7. Especificação de Endpoints e Payloads
### 7.1. Endpoint de Publicação no WordPress (REST API)
*   **Método:** `POST`
*   **URL:** `https://[SEU_DOMINIO_WORDPRESS]/wp-json/wp/v2/posts`
*   **Autenticação:** Basic Auth via *Application Passwords* do WordPress.
*   **Payload JSON esperado:**
```json
{
  "title": "Melhores Fones Bluetooth de 2026",
  "content": "<h2>Introdução</h2><p>Texto...</p>",
  "status": "publish",
  "categories": [2],
  "acf": {
    "product_1_title": "Fone Genérico X",
    "product_1_price": "59.90",
    "product_1_link": "https://mercadolivre.com.br/afiliado...",
    "product_1_store": "Mercado Livre"
  }
}
```

## 8. Arquitetura Local e Setup (Docker)
A arquitetura inteira roda via Docker. O `docker-compose.yml` orquestrará 3 serviços:
1.  **Serviço `db` (MySQL)**
2.  **Serviço `wordpress` (CMS Destino)**
3.  **Serviço `python-app` (A Pipeline com volumes mapeados e `Dockerfile.dev`)**

## 9. Pipeline Python (Módulos)
Como as chaves de API não estão disponíveis, os scrapers implementarão um modo "Mock" guiado por TDD.
*   `config/secrets_manager.py`: Integração com GCP Secret Manager.
*   `src/discovery.py`: Lógica de pauta e `history.json`.
*   `src/scrapers/mercadolivre.py` & `src/scrapers/amazon.py`: Scrapers.
*   `src/ai_generator.py` e `src/publisher.py`.

## 10. Fluxo de Execução (Runtime Cloud)
O Cloud Scheduler aciona o `main.py`, que carrega a pauta, faz o scrap, gera via Gemini, posta no WP via REST API, atualiza o histórico e morre.

## 11. Implantação (Deploy) com Infrastructure as Code (IaC) e README.md
### 11.1. Deploy via Terraform
Nenhum recurso na Google Cloud Platform será criado manualmente via console ou CLI (ad-hoc). O provisionamento será rigorosamente tratado como código (IaC) através do **Terraform**.

Um diretório de infraestrutura (ex: `infra/`) conterá manifestos (ex: `main.tf`, `variables.tf`, `outputs.tf`) configurados para provisionar:
1.  **Google Artifact Registry:** O repositório destino da imagem Docker da pipeline.
2.  **Google Secret Manager (Secrets):** O esqueleto dos segredos para credenciais sensíveis.
3.  **Google Cloud Run Job:** O worker da pipeline vinculado à imagem e injetando as variáveis do Secret Manager em runtime.
4.  **Google Cloud Scheduler:** O serviço cron que ativará o Cloud Run Job na frequência estipulada.

O controle de estado do Terraform (`terraform.tfstate`) deverá ser salvo em um Cloud Storage Bucket próprio.

### 11.2. Especificação do README.md
O `README.md` guiará a execução do projeto em três pilares:
1.  **Pré-requisitos:** Docker, Docker Compose, Terraform CLI.
2.  **Ambiente Local (TDD):** Comandos exatos para subida com `docker-compose`, configuração da rede WP/Python e como disparar as suítes de testes pytest do container.
3.  **Deploy em Produção (IaC):** Passos exatos para inicializar o ambiente de nuvem (`terraform init`, `plan`, e `apply`) seguidos pelas instruções de como fazer o build Docker (`Dockerfile.prod`) e enviá-lo ao Artifact Registry criado.

## 12. Requisitos de Segurança (Security Posture)
A segurança é crítica tanto para o frontend (CMS exposto na internet) quanto para o backend (Pipeline isolado). A arquitetura deve seguir mecanismos rígidos contra invasões e ataques de negação de serviço (DDoS).

### 12.1. Segurança do Pipeline e Nuvem (GCP)
*   **Princípio do Menor Privilégio (IAM):** O código Terraform deverá criar uma Conta de Serviço (Service Account) **exclusiva** para o Cloud Run Job. Esta conta terá permissão **apenas** de leitura para os segredos específicos no Secret Manager, sem nenhum acesso aos demais recursos do GCP.
*   **Isolamento de Rede (No Ingress):** O Cloud Run Job operará sem URL pública acessível. Ele será configurado via Terraform com o Ingress restrito para "Internal" (aceitando acionamento exclusivo do Cloud Scheduler nativo). Isso torna impossível um ataque DDoS direcionado à API Python.
*   **Sanitização de XSS e IA Prompt Injection:** Embora a IA Gemini seja a geradora do texto, alucinações podem produzir tags de script `<script>`. O módulo `src/publisher.py` deve sanitizar brutalmente o HTML gerado (usando libs como `bleach`) antes de fazer o POST para o WordPress, evitando a injeção cruzada de scripts (XSS).

### 12.2. Segurança do CMS Frontend (WordPress)
*   **WAF e Escudo Anti-DDoS:** O servidor do WordPress deve ser obrigatoriamente roteado por trás da **Cloudflare** (mesmo na camada gratuita) ou do **Google Cloud Armor**. Isso ocultará o IP real do servidor MySQL e fará o bloqueio nativo de robôs raspadores de conteúdo (Scraping Bots) e ataques Layer 7.
*   **Restrições de API e Login:**
    *   O arquivo nativo `xmlrpc.php` será bloqueado no nível da Cloudflare ou Nginx para prevenir ataques de força bruta no banco de senhas do WP.
    *   O usuário que autoriza as chamadas da API terá um nível de acesso restrito (apenas *Editor/Author*, não *Administrator*), contendo o raio de explosão no improvável cenário de um vazamento das "Application Passwords".
    *   O endpoint REST de listagem de usuários (`/wp-json/wp/v2/users`) deverá ser desabilitado ou restrito a administradores autenticados para evitar vazamento de *usernames*.
