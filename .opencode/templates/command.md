---
# Copia in .opencode\commands\<nome>.md  →  diventa il comando /<nome>
# Il corpo del file È il template del prompt.
description: Cosa fa questo comando
# agent: plan                  # agente usato quando parte il comando
# model: provider/model#variant
# subagent: true               # esegue in una sessione figlia in background
#
# Placeholder disponibili nel corpo:
#   $ARGUMENTS  → tutti gli argomenti come digitati
#   $1, $2 ...  → argomenti posizionali (l'ultimo prende il resto)
#   !`comando`  → inserisce l'output dello shell prima del prompt
---

Rivedi $ARGUMENTS e riporta prima i bug, poi i test mancanti.
