import express from "express";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// 🔍 listar tabelas
router.get("/tables", async (req, res) => {
  const result = await pool.query(`
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public'
  `);

  res.json(result.rows);
});

// 🔍 ver colunas de matches
router.get("/columns/:table", async (req, res) => {
  const { table } = req.params;

  const result = await pool.query(`
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = $1
  `, [table]);

  res.json(result.rows);
});

// 🚀 teste simples
router.get("/opportunities", async (req, res) => {
  const result = await pool.query(`SELECT * FROM matches LIMIT 10`);
  res.json(result.rows);
});

export default router;