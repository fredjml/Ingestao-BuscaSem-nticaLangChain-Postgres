# 02 — Pre-flight (desafio1)

Executado em **2026-09-04** em modo **read-only** (somente verificações de versão/presença). Nada instalado, nada alterado, nenhum serviço iniciado.

## 1. Comandos executados (PowerShell, read-only)

```powershell
python --version; py -3 --version; pip --version
docker --version; docker compose version; docker info --format '{{.ServerVersion}}'
git --version; git rev-parse --is-inside-work-tree; node --version
```

## 2. Resultado observado

| Item | Resultado | Veredito |
| --- | --- | --- |
| Python | **ausente** ("Python não foi encontrado… Microsoft Store") | ❌ instalar |
| py launcher | **ausente** | ❌ vem com instalador python.org |
| pip | **ausente** | ❌ vem com Python |
| Docker client | 29.6.2 (build dfc4efb) | ✅ |
| Docker Compose | v5.3.1 | ✅ |
| Docker daemon | **parado** (pipe `dockerDesktopLinuxEngine` não encontrado) | ⚠️ iniciar Docker Desktop |
| Git | 2.55.0.windows.4 | ✅ |
| Workspace git | **não é repositório** | ⚠️ depende de DEC-02 (fork × scaffold) |
| Node | v24.19.0 | ✅ (só p/ validador de diagramas do kit; opcional) |

## 3. Software a instalar/configurar (com autorização just-in-time na Fase B)

| # | Software | Versão alvo | Para quê | Autorização necessária |
| --- | --- | --- | --- | --- |
| S1 | Python (python.org, com py launcher + pip) | **3.11+** (DEC-04) | runtime do desafio | owner de infra |
| S2 | Docker Desktop | já instalado — **apenas iniciar** o daemon | Postgres+pgVector | owner de infra |
| S3 | venv | vem com Python | isolamento de deps (`venv\Scripts\Activate.ps1`) | junto com S1 |
| S4 | Git — `git init` ou fork do template | — | versionamento/entrega | DEC-02 + DEC-08 |
| S5 | Credenciais OpenAI e/ou Google | — | embeddings + LLM live | owner de credenciais (**nunca colar no chat**) |

Não instalar nada além do listado sem novo pre-flight (regra do kit: ferramenta por requisito, risco, licença, telemetria e fallback).

## 4. Decisão de prontidão (Gate 0)

- **Para preparação/documentação (Passos 0–4): GO** — executado neste pacote.
- **Para implementação (Gate 3): NO-GO** até: S1 instalado, S2 com daemon ativo, DEC-02/03/07 fechadas, e **reexecução deste pre-flight** após qualquer mudança de runtime/ambiente.

## 5. Limitações

- Pre-flight não testa rede externa, cotas de API, nem disponibilidade dos modelos citados no enunciado (INC-07/08) — verificação com fonte oficial datada é tarefa da Fase B.
