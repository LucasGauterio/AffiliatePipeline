# Lista de Tarefas: Pipeline de Afiliados

> **REGRA DE OURO (CICLO POR TAREFA):**
> 1. Escrever o **Failing Test (TDD)**.
> 2. Implementar o código e fazer o teste passar.
> 3. Fazer o **Commit no Git** (`git commit -m "..."`) com o escopo da tarefa.
> 4. Atualizar o arquivo **`context.md`** ao concluir a Fase.

## Fase 1: Setup do Ambiente e Git
- `[x]` 1.1. Inicializar o repositório Git (`git init`) e adicionar o `.gitignore`.
- `[x]` 1.2. Criar estrutura (`src`, `tests`, `config`, `infra`) e fazer o Commit inicial.
- `[x]` 1.3. Criar `requirements.txt` e `requirements-dev.txt` (Commit).
- `[x]` 1.4. Criar `Dockerfile.dev` e `docker-compose.yml` (Commit).
- `[x]` 1.5. Criar scripts de execução (`run_tests`) e `pytest.ini` (Commit).
- `[x]` 1.6. Inicializar o `context.md` com o resumo da Fase 1 e fazer o Push/Commit.

## Fase 2: Configurações e Segredos
- `[x]` 2.1. TDD + Code: Implementar `config/settings.py` (Commit).
- `[x]` 2.2. TDD + Code: Implementar `config/secrets_manager.py` (Commit).
- `[x]` 2.3. Atualizar `context.md` com o resumo da Fase 2 (Commit).

## Fase 3: Módulo de Pauta (Discovery)
- `[x]` 3.1. TDD + Code: Implementar arquivo de mocks e lógica do `discovery.py` (Commit).
- `[x]` 3.2. Atualizar `context.md` com o resumo da Fase 3 (Commit).

## Fase 4: Scrapers e Mocks
- `[x]` 4.1. TDD + Code: Implementar `base.py` e interface abstrata (Commit).
- `[x]` 4.2. TDD + Code: Implementar `src/scrapers/mercadolivre.py` modo mock (Commit).
- `[x]` 4.3. TDD + Code: Implementar `src/scrapers/amazon.py` modo mock (Commit).
- `[x]` 4.4. Atualizar `context.md` com o resumo da Fase 4 (Commit).

## Fase 5: Módulo de IA (Gemini)
- `[ ]` 5.1. TDD + Code: Implementar a orquestração do prompt em `ai_generator.py` (Commit).
- `[ ]` 5.2. Atualizar `context.md` com o resumo da Fase 5 (Commit).

## Fase 6: Módulo de Publicação (WordPress)
- `[ ]` 6.1. TDD + Code: Implementar `create_payload()` e `publisher.py` (Commit).
- `[ ]` 6.2. Atualizar `context.md` com o resumo da Fase 6 (Commit).

## Fase 7: Orquestração (Main)
- `[ ]` 7.1. TDD + Code: Implementar `main.py` costurando todos os módulos (Commit).
- `[ ]` 7.2. Atualizar `context.md` com o resumo da Fase 7 (Commit).

## Fase 8: Deploy IaC (Terraform) e Docs Finais
- `[ ]` 8.1. Criar `Dockerfile.prod` (Commit).
- `[ ]` 8.2. Codificar a infraestrutura IaC em `infra/main.tf` (Commit).
- `[ ]` 8.3. Escrever o `README.md` final com o tutorial do Terraform (Commit).
- `[ ]` 8.4. Fazer o commit final de conclusão de projeto.
