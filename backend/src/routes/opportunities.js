const express = require("express");
const router = express.Router();

router.get("/", async (req, res) => {
  return res.json([
    { status: "BACKEND ATUALIZADO COM SUCESSO 🚀" }
  ]);
});

module.exports = router;