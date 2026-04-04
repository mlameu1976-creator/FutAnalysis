import express from "express";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

// 🔥 TESTE BRUTO (SEM FILTRO)
router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT *
      FROM matches
      LIMIT 20
    `);

    res.json(result.rows);

  } catch (error) {
    console.error("ERRO:", error);
    res.status(500).json({ error: error.message });
  }
});

export default router;