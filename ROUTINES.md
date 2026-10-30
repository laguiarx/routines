# Manifesto das routines

A configuração de cada routine fica na conta do claude.ai (claude.ai/code/routines),
não neste repo. Este arquivo é a receita para recriá-las.

## daily-briefing

- Horário: diário, 07:50 (America/Sao_Paulo), preset Daily
- Repositório: laguiarx/routines
- Ambiente: Default (se der 403 host_not_allowed, mudar para Custom/Full)
- Conectores: nenhum
- Prompt salvo na routine:

  > Execute a skill daily-briefing deste repositório, seguindo as regras do CLAUDE.md.

---

## Nova routine (checklist)

1. Criar `.claude/skills/<nome>/SKILL.md`
2. Criar `state/<nome>.json` e `outputs/<nome>/.gitkeep`
3. Push na main
4. Criar a routine em claude.ai/code/routines com o prompt:
   "Execute a skill <nome> deste repositório, seguindo as regras do CLAUDE.md."
5. Registrar aqui horário, conectores e ambiente
