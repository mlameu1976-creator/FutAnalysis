const express = require("express");
const cors = require("cors");

const routes = require("./routes");
const { runIngestion } = require("./services/dataIngestion");

const app = express();

app.use(cors());
app.use(express.json());

// 🔥 EXECUTA INGESTÃO REAL AO INICIAR
(async () => {
  console.log("🚀 INICIANDO SERVIDOR COM INGESTÃO REAL...");
  await runIngestion();
})();

app.use("/", routes);

const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`🔥 Server rodando na porta ${PORT}`);
});