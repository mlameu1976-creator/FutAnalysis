const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// IMPORTAÇÃO DAS ROTAS
const opportunitiesRoutes = require("./routes/opportunities");

// ROTA BASE
app.use("/opportunities", opportunitiesRoutes);

// HEALTH CHECK (IMPORTANTE)
app.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend Running");
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🔥 Server running on port ${PORT}`);
});