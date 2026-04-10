const express = require("express");
const cors = require("cors");
const db = require("./db");

const { runIngestion } = require("./services/dataIngestion");

const app = express();

app.use(cors());
app.use(express.json());

console.log("🔥 SERVER RODANDO");

// ===============================
// TESTE
// ===============================
app.get("/", (req, res) => {
  res.send("FutAnalysis API rodando 🚀");
});

// ===============================
// START
// ===============================
async function start() {
  try {
    await db.query("SELECT 1");

    console.log("🔥 DB conectado");

    // 🚨 FORÇA LIMPEZA TOTAL
    await db.query("DELETE FROM matches");

    // 🚨 FORÇA NOVA INGESTÃO
    await runIngestion();

    app.listen(8080, () => {
      console.log("🚀 Server rodando na porta 8080");
    });
  } catch (err) {
    console.error("❌ ERRO START:", err);
  }
}

start();