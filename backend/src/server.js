const express = require("express");
const cors = require("cors");
const db = require("./db");

const { importMatches } = require("./services/dataIngestion");
const opportunitiesRoute = require("./routes/opportunities");

const app = express();
app.use(cors());
app.use(express.json());

// =============================
// 🔥 RESET + INGESTÃO FORÇADA
// =============================
async function start() {
  try {
    console.log("🔥 LIMPANDO BANCO...");

    await db.query("DELETE FROM matches");

    console.log("🚀 IMPORTANDO JOGOS...");

    await importMatches();

    console.log("✅ INGESTÃO FINALIZADA");
  } catch (err) {
    console.error("❌ ERRO START:", err);
  }
}

// 🔥 EXECUTA AO INICIAR
start();

// =============================
app.use("/opportunities", opportunitiesRoute);

// =============================
const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`🔥 Server running on port ${PORT}`);
});