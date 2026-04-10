const express = require("express");
const cors = require("cors");
const db = require("./db");

const routes = require("./routes");
const { runIngestion } = require("./services/dataIngestion");

const app = express();

app.use(cors());
app.use(express.json());

app.use("/", routes);

console.log("🔥 SERVER INICIANDO");

// ===============================
// START
// ===============================
async function start() {
  try {
    await db.query("SELECT 1");
    console.log("✅ DB conectado");

    // 🚨 NÃO BLOQUEIA MAIS O SERVER
    runIngestion()
      .then(() => console.log("✅ INGESTÃO OK"))
      .catch((err) => console.error("❌ ERRO INGESTÃO:", err.message));

    app.listen(8080, () => {
      console.log("🚀 Server rodando na porta 8080");
    });
  } catch (err) {
    console.error("❌ ERRO START:", err);
  }
}

start();