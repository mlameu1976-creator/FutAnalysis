// frontend/services/modelInfoService.js

export async function getModelInfo() {
  const response = await fetch("http://127.0.0.1:8000/model/info");

  if (!response.ok) {
    throw new Error("Erro ao buscar informações do modelo");
  }

  return response.json();
}
