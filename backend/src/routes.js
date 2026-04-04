import express from "express";
import { importLeague } from "./services/importData.js";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// 🚀 ROOT
router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

// 🔥 IMPORTAR DADOS
router.get("/import/:leagueId", async (req, res) => {
  const { leagueId } = req.params;

  await importLeague(leagueId);

  res.json({ message: "Importação concluída" });
});

// 🔥 TESTE
router.get("/opportunities", async (req, res) => {
  const result = await pool.query(`SELECT * FROM matches LIMIT 20`);
  res.json(result.rows);
});

export default router;