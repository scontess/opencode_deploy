# Progetto predefinito

## Cosa c'è

- `deploy_flask\` — app Flask (`app.py`, `templates\index.html`, `requirements.txt`, venv in `.venv\`)
- `Dashboard_Vendite\` — dashboard statica autonoma (`dashboard_vendite.html` + `vendite_2026.csv`)
- `netlify.toml` — config Netlify alla radice (`publish = "Dashboard_Vendite"`, redirect `/`)
- `render.yaml` — Blueprint Render per l'app Flask (✅ deployato)
- `opencode.jsonc` — config di progetto, inclusi i server MCP
- `.opencode\` — agenti, comandi, skill, plugin (+ `templates\` non scoperta)

Le due parti sono indipendenti: la dashboard **non** passa da Flask.

## Comandi

### Flask in locale

```powershell
cd deploy_flask
.\.venv\Scripts\python.exe app.py      # http://127.0.0.1:5000
```

- `GET /` → pagina, `GET /health` → `{"status":"ok"}`
- `FLASK_DEBUG=0` disattiva il reload automatico (su Render è già `0`)

### Ambiente virtuale

```powershell
cd deploy_flask
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Dashboard in locale

```powershell
cd Dashboard_Vendite
python -m http.server 8000            # http://localhost:8000/dashboard_vendite.html
```

Oppure apri l'HTML e usa "Collega vendite_2026.csv" (solo Chrome/Edge).

## Repository Git

- Remoto: **`https://github.com/scontess/opencode_deploy`** (pubblico, branch `main`)
- Stato al 26/11/2026: repo creato e **vuoto**; la cartella locale non è ancora un repo git
  (mancano `git init`, primo commit, `git remote add origin`).
- Da pushare: tutto tranne `.venv\`, `__pycache__\`, `.netlify\` (già in `.gitignore`).
- Su Render: Blueprint path `render.yaml` nella radice del repo; serve comunque collegare
  una volta l'account GitHub a Render per creare il servizio.

## Deploy

### Netlify — dashboard statica (✅ deployata)

- Sito: **https://dashboard-vendite.netlify.app** — progetto `dashboard-vendite`, id `694d8749-0e2f-400e-bddf-ec93132ea9f0`
- Primo deploy: 26/11/2026, deploy id `6b076ee847f72efaa74aff08`; verificato live (50 righe, 264.300 €, 0 errori console)
- MCP: `netlify` (remoto ufficiale, OAuth, già autenticato)
- `netlify.toml` sta alla **radice** con `publish = "Dashboard_Vendite"` (tiene fuori il venv) e redirect `/` → `/dashboard_vendite.html`
- Come si deploya: `deploy-site` dell'MCP **non carica i file**, restituisce un comando
  `npx -y @netlify/mcp@latest --site-id <id> --proxy-path <url>` da eseguire nella radice del progetto
  (su PowerShell serve `cmd /c npx ...`). Poi verificare l'URL pubblico.
- Fallback: `npx netlify-cli deploy --dir=Dashboard_Vendite --prod` con `NETLIFY_AUTH_TOKEN`.

### Render — app Flask (✅ deployata)

- Live: **https://deploy-flask-4wfz.onrender.com** — `/health` → `{"status":"ok"}`, `/` → pagina (0 errori console)
- Servizio `deploy-flask`, id `srv-dc3n573l550s73evfpr0`, Blueprint `exs-dc3n2ot6e07s73cvnfj0`,
  workspace `My Workspace` (`tea-dbk91sks728c73cfmfdg`), repo `scontess/opencode_deploy` branch `main`
- Primo deploy dal commit `a874594` (26/11/2026, trigger `blueprint_sync`)
- ✅ **Auto-deploy attivo**: `autoDeploy: yes` + `autoDeployTrigger: commit` → un `git push` su `main`
  crea da solo un deploy (trigger `new_commit`). Il pulsante "Manual sync" del Blueprint serve solo
  a riapplicare il `render.yaml`, non a deployare il codice.
- ⚠️ Piano free: sleep dopo ~15 min di inattività, primo accesso 30-60 s
- La pagina mostra indirizzo reale (`X-Forwarded-Proto` + `request.host`) e ora in `Europe/Rome`
  (`APP_TIMEZONE`, default `Europe/Rome`; `tzdata` in `requirements.txt` per Windows).
  Fix nel commit `9417d33`.
- `render.yaml` (root del repo): `rootDir: deploy_flask`, build `pip install -r requirements.txt`, start `gunicorn app:app --bind 0.0.0.0:$PORT`, health check `/health`, piano free, region frankfurt.
- MCP `render` **attivo** (Bearer `{env:RENDER_API_KEY}`, Read ovunque + Run su Deploys).
  Tool usati: `list_workspaces`, `list_services`, `list_deploys`, `trigger_deploy`, `list_logs`, `get_deploy`.
- **Limite noto dell'MCP**: `create_web_service` non espone né `rootDir` né il piano `free`
  (accetta solo starter/standard/pro…). Percorso corretto: **Blueprint**
  (`create_blueprint` → `plan_blueprint` → `approve_blueprint`), che legge `render.yaml`
  e quindi rispetta `rootDir: deploy_flask` e `plan: free`. In alternativa: dashboard → New → Blueprint.
- I tool Blueprint sono in **alpha pubblica**: contratti soggetti a cambiamenti.
- ⚠️ Nella stessa workspace/progetto c'è **`pianificazione_orario`** (id `srv-dbk98tec6qcc73dtm20g`,
  repo `scontess/pianificazione_orario`, URL pianificazione-orario.onrender.com): è un'altra app,
  **non toccarla** quando si lavora su `deploy-flask`. Nota: il servizio si chiama con `_` ma
  l'URL usa `-` (Render converte gli underscore nei sottodomini).

### Segreti

Mai nel repo. Solo variabili d'ambiente, referenziate come `{env:NOME}`:

```powershell
$cli = "$env:APPDATA\ai.opencode.desktop\cli\2.4.1-x64\opencode-cli.exe"
& $cli service set env RENDER_API_KEY rnd_...
& $cli service restart
```

⚠️ Non usare `git add -A` / `git add .` alla cieca: il 26/11/2026 un file locale
`apikey.txt` con la chiave Render è finito in un commit su repo **pubblico** (poi rimosso
con amend + force-push, chiave revocata). Ora `.gitignore` esclude `apikey.txt`, `*.key`,
`secrets*`, ma la regola resta: **stage per nome di file**.

## MCP configurati

| Nome | Tipo | Endpoint | Auth | Stato |
|---|---|---|---|---|
| `netlify` | remote | `https://mcp.netlify.com/mcp` | OAuth (`/mcps`) | ✅ connected |
| `render` | remote | `https://mcp.render.com/mcp` | Bearer `{env:RENDER_API_KEY}` | ✅ connected |

Alternativa locale Netlify: `npx -y @netlify/mcp` con `NETLIFY_PERSONAL_ACCESS_TOKEN` (commentata nel config).

## Vincoli noti

- `gunicorn` si installa su Windows ma **non parte**: in locale si usa `python app.py`.
- Render piano free: il servizio va in sleep dopo inattività (primo accesso lento).
- La dashboard è statica: nessuna route Flask la serve.
- La dashboard rilegge il CSV ogni 2 s; su Netlify il `Cache-Control: no-store` è già in `netlify.toml`.
- Agenti e regioni nel CSV sono in corrispondenza 1:1, quindi i due grafici sono ridondanti.

## Convenzioni

- Lingua: italiano (risposte, commenti, documentazione).
- Segreti solo in variabili d'ambiente, mai in file versionati.
- Il venv (`.venv\`) non si committa e non si deploya: su Render contano solo `requirements.txt`.
