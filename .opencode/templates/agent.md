---
# Copia in .opencode\agents\<nome>.md  →  l'ID dell'agente è il nome del file.
# Il corpo (sotto il secondo ---) diventa il system prompt dell'agente.
description: Breve descrizione che il modello legge per scegliere l'agente
mode: subagent        # primary | subagent | all
# model: provider/model#variant
# steps: 8            # numero massimo di passi del modello
# hidden: true        # nasconde l'agente dagli elenchi
# color: "#ff6b6b"
permissions:
  - action: edit
    resource: "*"
    effect: deny      # allow | ask | deny
  - action: shell
    resource: "git *"
    effect: ask
---

Sei un revisore di codice. Elenca i problemi in ordine di gravità con
riferimenti file:riga. Non modificare i file.
