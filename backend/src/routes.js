import express from "express";

const router = express.Router();

// 🔥 TESTE
router.get("/", (req, res) => {
  res.send("API funcionando 🚀");
});

// 🔥 NOVA ROTA DE OPORTUNIDADES
router.get("/opportunities", async (req, res) => {
  try {
    // 🔥 MOCK INICIAL (depois vamos ligar no banco)
    const data = [
      {
        home_team: "Arsenal",
        away_team: "Chelsea",
        league: "Premier League",
        confidence_score: 78,
        ev: 12.5,
      },
      {
        home_team: "Barcelona",
        away_team: "Real Madrid",
        league: "La Liga",
        confidence_score: 82,
        ev: 15.2,
      },
    ];

    res.json(data);
  } catch (error) {
    console.error("Erro opportunities:", error);
    res.status(500).json({ error: "Erro interno" });
  }
});

export default router;