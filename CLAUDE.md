# Repositório de routines

Este repositório guarda a lógica de todas as routines (scheduled tasks) do Claude Code.
Cada routine é uma skill em `.claude/skills/<nome>/SKILL.md`, com estado em
`state/<nome>.json` e saídas em `outputs/<nome>/`.

## Regras para toda execução de routine

1. Escreva SOMENTE nos arquivos da sua routine: `state/<nome>.json` e `outputs/<nome>/`.
   Nunca altere arquivos de outra routine, skills ou este CLAUDE.md.
2. Trabalhe direto na branch `main`. Não crie branches `claude/` nem abra PR.
3. Ao terminar:
   - `git add state/<nome>.json outputs/<nome>/`
   - `git commit -m "<nome>: AAAA-MM-DD"`
   - `git pull --rebase origin main`
   - `git push origin main`
   - Se o push falhar por conflito, repita pull --rebase + push até 3 vezes.
4. Datas sempre no fuso America/Sao_Paulo, formato AAAA-MM-DD.
5. Se algo impedir a execução (rede bloqueada, fonte fora do ar), registre o problema
   no topo do output do dia em vez de falhar em silêncio.
