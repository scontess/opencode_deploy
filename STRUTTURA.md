# Struttura del progetto

```text
Progetto predefinito\
├── AGENTS.md                  istruzioni di progetto (caricate sempre)
├── STRUTTURA.md               questa mappa
├── opencode.jsonc             config progetto + server MCP (render, netlify)
├── render.yaml                Blueprint Render per l'app Flask (pronto, spento)
├── netlify.toml               config Netlify (publish = "Dashboard_Vendite")
├── .gitignore                 venv, cache, .netlify, segreti
│
├── deploy_flask\              APP FLASK (deploy su Render)
│   ├── app.py                 GET / e GET /health
│   ├── requirements.txt       flask + gunicorn
│   ├── templates\index.html   pagina minima
│   └── .venv\                 ambiente virtuale (NON committare, NON deployare)
│
├── Dashboard_Vendite\         DASHBOARD STATICA (deploy su Netlify)
│   ├── dashboard_vendite.html pagina + CSS/JS inline
│   ├── vendite_2026.csv       50 vendite 2026
│   └── netlify.toml           publish = "." + no-store sul CSV
│
└── .opencode\                 tutto ciò che OpenCode scopre in automatico
    ├── agents\                agenti custom        →  *.md
    ├── commands\              comandi slash        →  *.md
    ├── skills\                skill               →  <id>\SKILL.md
    ├── plugins\               plugin locali       →  *.ts / *.js / cartelle
    └── templates\             NON scoperta: solo esempi da copiare
        ├── agent.md
        ├── command.md
        ├── plugin.ts
        └── skill\SKILL.md
```

I file `.gitkeep` tengono in vita le cartelle vuote in git e non vengono letti
da OpenCode (non sono `.md`).

## Due deploy indipendenti

| Cartella | Destino | Cosa pubblica | File di config |
|---|---|---|---|
| `deploy_flask\` | **Render** (web service python) | app Flask via gunicorn | `render.yaml` (root del repo) |
| `Dashboard_Vendite\` | **Netlify** (static site) | HTML + CSV così come sono | `netlify.toml` alla radice (`publish`) |

Sito live: **https://dashboard-vendite.netlify.app** (`/` → `dashboard_vendite.html`).
Il venv `.venv\` serve solo in locale: su Render si ricostruisce da `requirements.txt`, su Netlify non viene pubblicato.

## Cosa va dove (parte OpenCode)

| Cosa | Percorso progetto | Percorso globale | Formato |
|---|---|---|---|
| Istruzioni | `AGENTS.md` | `C:\Users\silva\.config\opencode\AGENTS.md` | Markdown |
| Config | `opencode.jsonc` (o `.opencode\opencode.jsonc`) | `~\.config\opencode\opencode.jsonc` | JSONC |
| Agenti | `.opencode\agents\<nome>.md` | `~\.config\opencode\agents\<nome>.md` | MD + frontmatter |
| Comandi | `.opencode\commands\<nome>.md` | `~\.config\opencode\commands\<nome>.md` | MD + frontmatter |
| Skill | `.opencode\skills\<id>\SKILL.md` | `~\.config\opencode\skills\<id>\SKILL.md` | MD + frontmatter |
| Plugin | `.opencode\plugins\<nome>.ts` o `\<nome>\index.ts` | `~\.config\opencode\plugins\` | TypeScript/JS |
| MCP | voce `mcp.servers` in `opencode.jsonc` | idem, nel config globale | JSON |

Note:

- Le skill accettano anche `.opencode\skills\<nome>.md` (file singolo) e
  `~\.claude\skills`, `~\.agents\skills` per compatibilità.
- Gli agenti in sottocartelle prendono un ID composto:
  `.opencode\agents\team\reviewer.md` → `team/reviewer`.
- I comandi in sottocartelle diventano `/team/reviewer`.
- Un MCP non è un plugin e non ha una cartella: esiste solo nel config.

## Precedenza (chi vince)

```text
globale (~\.config\opencode\...)   →  base
progetto (.opencode\...)           →  sovrascrive a parità di nome/ID
```

Stessa cosa tra skill: una skill di progetto con lo stesso ID sostituisce quella
globale. `templates\` è esclusa dalla scoperta, quindi puoi tenerci esempi
senza che diventino attivi.

## Come attivare un elemento

1. Copia il template da `.opencode\templates\` nella cartella giusta.
2. Rinominalo con l'ID/nome che vuoi (`reviewer.md`, `release\SKILL.md`, ...).
3. Compila il frontmatter (in particolare `description`).
4. Salva: OpenCode lo rileva e ricarica da solo. Se non compare, usa `/reload`.

## Verifica

- Agenti/comandi/skill attivi: `Ctrl+P` → lista agenti, `/` → lista comandi.
- MCP: `opencode-cli mcp list` (in questo PC il binario è in
  `%APPDATA%\ai.opencode.desktop\cli\2.4.1-x64\opencode-cli.exe`) oppure `/mcps`.
- Flask: `http://127.0.0.1:5000/` e `/health`.
