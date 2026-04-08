const express = require("express");
const cors = require("cors");
const db = require("./db");

const routes = require("./routes");
const { runIngestion } = require("./services/dataIngestion");

const app = express();

app.use(cors());
app.use(express.json());

console.log("🔥 SERVER NOVO RODANDO");

// ===============================
// ROTAS
// ===============================
app.use("/", routes);

// ===============================
// START
// ===============================
async function start() {
  try {
    await db.query("SELECT 1");

    console.log("🔥 DB conectado");

    // 🚀 roda ingestão ao subir
    await runIngestion();

    app.listen(8080, () => {
      console.log("🚀 Server rodando na porta 8080");
    });
  } catch (err) {
    console.error("❌ ERRO START:", err);
  }
}

start();