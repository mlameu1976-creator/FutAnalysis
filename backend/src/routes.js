import express from "express";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

// 🔥 conexão postgres
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

// 🔥 rota raiz
router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

// 🔥 TESTE DE BANCO
router.get("/test-db", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW()");
    res.json(result.rows);
  } catch (error) {
    console.error("ERRO DB:", error);
    res.status(500).json({ error: error.message });
  }
});

// 🔥 OPORTUNIDADES
router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        m.id,
        m.home_team,
        m.away_team,
        l.name as league
      FROM matches m
      JOIN leagues l ON l.id = m.league_id
      LIMIT 20
    `);

    res.json(result.rows);

  } catch (error) {
    console.error("ERRO REAL:", error);
    res.status(500).json({ error: error.message });
  }
});

export default router;