// Copia in .opencode\plugins\<nome>.ts  →  caricato in automatico.
// In alternativa: .opencode\plugins\<nome>\index.ts (+ eventuale package.json).
// Richiede la dipendenza @opencode/plugin nel progetto.
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "esempio",
  async setup(ctx) {
    // Qui si aggiungono hook, tool, comandi, agenti, integrazioni.
    // Esempio: stato persistente del plugin
    // await ctx.storage.set("loaded", true)
  },
})
