import express from "express";
import cors from "cors";
import routes from "./routes.js";

const app = express();

app.use(cors());
app.use(express.json());

/* 🔥 ROTA TESTE (IMPORTANTE) */
app.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

/* 🔥 ROTAS PRINCIPAIS */
app.use("/api", routes);

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
  console.log(`🚀 Backend rodando na porta ${PORT}`);
});