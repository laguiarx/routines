---
name: daily-briefing
description: Briefing diário com lançamentos de modelos de IA e vulnerabilidades críticas (CVSS 9+) no ecossistema Node/Bun/React/TypeScript/Vercel/TanStack e Rust. Use quando a routine pedir o daily-briefing.
---

# Daily Briefing

Responda em português. Estado: `state/daily-briefing.json`. Saída: `outputs/daily-briefing/AAAA-MM-DD.md`.

## 0. Data de hoje

Rode `TZ=America/Sao_Paulo date +%F` e use o resultado como HOJE em tudo: nome do arquivo de saída,
mensagem de commit, `first_seen` e `last_reported`. Rode `TZ=America/Sao_Paulo date -d '3 days ago' +%F`
para obter DESDE (início da janela estendida). Nunca use a data UTC do sistema nem a do aviso de disparo.

## 1. Memória (antes de pesquisar)

Leia `state/daily-briefing.json`. Ele tem duas listas, `security` e `ai`, com os itens já reportados.

## 2. Seção 1 — Lançamentos de IA

TEMA: Lançamentos e anúncios de modelos de IA.
FONTES PRIORITÁRIAS: blogs e páginas de anúncio oficiais (Anthropic, OpenAI, xAI, Google DeepMind, Meta AI, Mistral, DeepSeek, Alibaba/Qwen, Moonshot/Kimi, Zhipu/GLM), model cards, changelogs de API, Hugging Face. Imprensa de tecnologia só como apoio.
CONSULTA OBRIGATÓRIA (abra todas antes de concluir; se uma falhar, anote no topo do output e siga):
- https://www.anthropic.com/news
- https://openai.com/news/ e https://platform.openai.com/docs/changelog
- https://blog.google/technology/google-deepmind/ e https://ai.google.dev/gemini-api/docs/changelog
- https://x.ai/news
- https://ai.meta.com/blog/
- https://mistral.ai/news
- https://api-docs.deepseek.com/
- Modelos recentes no Hugging Face (JSON, via `curl -s`), para cada org em Qwen, deepseek-ai, moonshotai, zai-org, mistralai, meta-llama, google, openai:
  `https://huggingface.co/api/models?author=<org>&sort=createdAt&direction=-1&limit=10`
Use WebSearch só para completar (ex.: Qwen e Kimi fora do Hugging Face), nunca como fonte principal.
JANELA: últimas 24h (estenda para 72h se não houver lançamento relevante e sinalize isso).
CRITÉRIOS (ordem de prioridade): modelo novo > nova versão > recurso novo de API/SDK > preço/disponibilidade. Dê destaque ao que impacta quem desenvolve agentes, RAG e ferramentas de código.
POR ITEM: o que foi lançado → o que tem de novo na prática → comparação com concorrentes (só com dados oficiais) → disponibilidade (API, preço, região) → link da fonte oficial.
EVITE: benchmarks sem fonte oficial, rumores apresentados como fato, hype ("vai acabar com X").

## 3. Seção 2 — Segurança

TEMA: Vulnerabilidades críticas e ataques de supply chain.
ESCOPO: Node.js, Bun, Deno, npm/pnpm/yarn, React, React Server Components, Next.js, Vercel (plataforma e pacotes), TanStack (Query, Router, Start), Vite, TypeScript e tooling, frameworks e bibliotecas populares do ecossistema (Express, Fastify, Hono, Prisma, Drizzle, tRPC, Zod, Remix, Astro etc.) e pacotes npm com alto volume de download.
EXTRA (Rust): crates populares (tokio, axum, hyper, serde, reqwest, actix, rustls) e o próprio toolchain.
FONTES PRIORITÁRIAS: GitHub Advisory Database (GHSA), NVD, blog de security releases do Node.js, advisories de Vercel/Next.js, releases do Bun, RustSec Advisory Database, Socket.dev, Snyk, OSV.dev.
CONSULTA OBRIGATÓRIA (abra todas antes de concluir; se uma falhar, anote no topo do output e siga):
- GitHub Advisory Database (JSON, via `curl -s`; troque DESDE pela data da etapa 0; `%3E%3D` é `>=` codificado):
  - npm crítico: `https://api.github.com/advisories?ecosystem=npm&severity=critical&published=%3E%3DDESDE&per_page=100`
  - npm malware: `https://api.github.com/advisories?ecosystem=npm&type=malware&published=%3E%3DDESDE&per_page=100` (filtre pelos pacotes populares)
  - Rust crítico: `https://api.github.com/advisories?ecosystem=rust&severity=critical&published=%3E%3DDESDE&per_page=100`
  - Repita as três com `updated=%3E%3DDESDE` no lugar de `published` para achar reclassificações e patches novos (🔄 ATUALIZAÇÃO).
- https://nodejs.org/en/blog/vulnerability
- https://github.com/vercel/next.js/security/advisories
- https://github.com/oven-sh/bun/releases
- https://rustsec.org/advisories/
- https://socket.dev/blog
Para cada candidato, confirme CVSS e versões no GHSA ou em `https://nvd.nist.gov/vuln/detail/<CVE>`. Use WebSearch só para completar.
JANELA: últimas 24h (estenda para 72h se não houver nada e sinalize isso).
CRITÉRIO DE CORTE: CVSS ≥ 9.0 (v3.1 ou v4). Inclua também, mesmo sem CVSS, pacotes maliciosos publicados, contas de maintainers comprometidas e worms de supply chain que afetem pacotes populares.
POR ITEM: pacote/produto → CVE/GHSA → CVSS → tipo de falha (RCE, auth bypass etc.) → versões afetadas → versão corrigida → se há exploração ativa ou PoC público → ação recomendada (comando de atualização ou mitigação) → link.
EVITE: vulnerabilidades abaixo de 9.0, repetir o mesmo CVE vindo de várias fontes, alarmismo sem confirmação.

## 4. Deduplicação

- Chave de segurança: CVE ou GHSA. Pacote malicioso sem CVE: `malicious:pacote@versão`.
- Chave de IA: `empresa/modelo-ou-recurso` (ex.: `openai/gpt-x`).
- Item já presente no estado: NÃO reporte de novo.
- Exceção: se houve mudança relevante desde `last_reported` (exploração ativa confirmada, PoC público, patch novo, CVSS reclassificado, versões afetadas ampliadas), reporte como "🔄 ATUALIZAÇÃO" explicando só o que mudou.

## 5. Formato de saída

- Comece com um TL;DR de no máximo 3 linhas: o que é mais importante hoje.
- Itens de segurança com exploração ativa vêm primeiro, marcados com 🚨.
- Seção sem nada relevante na janela: diga isso em uma linha. Não preencha com notícias fracas.
- Toda afirmação precisa de link da fonte.
- No máximo 5 itens de IA; todos os de segurança que passarem no corte.
- Mostre o briefing completo na resposta final da sessão também.

## 6. Depois de gerar

1. Adicione os itens novos ao estado e atualize `last_reported`/`status` dos que receberam atualização.
2. Remova do estado itens com `first_seen` há mais de 30 dias.
3. Salve o briefing em `outputs/daily-briefing/AAAA-MM-DD.md`.
4. Faça commit e push seguindo as regras do `CLAUDE.md`.

Formato dos itens no estado:

    {
      "security": [
        { "id": "CVE-2026-12345", "package": "next", "cvss": 9.8, "status": "patched", "first_seen": "2026-10-29", "last_reported": "2026-10-29" }
      ],
      "ai": [
        { "id": "openai/gpt-x", "type": "modelo novo", "first_seen": "2026-10-29" }
      ]
    }
