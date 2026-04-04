import express from "express";
import { getMatchProbability } from "./services/statsService.js";

const router = express.Router();

/* 🔥 TESTE */
router.get("/test", (req, res) => {
  res.json({ status: "API funcionando" });
});

/* 🔥 PROBABILIDADE */
router.get("/probability", getMatchProbability);

export default router;