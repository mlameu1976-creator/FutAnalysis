FutAnalysis - Projeto completo gerado automaticamente

Como usar (com Docker - recomendado):
1. Extraia este ZIP em uma pasta.
2. Abra terminal e vá para backend/:
   cd futanalysis_full/backend
3. Copie .env.example para .env e ajuste senhas:
   cp .env.example .env   (Linux/Mac)  OR  copy .env.example .env (Windows)
4. Execute:
   docker-compose up --build
5. Abra outro terminal e vá para frontend/:
   cd ../frontend
   npm install
   npm run dev
6. Acesse frontend: http://localhost:5173
   API docs: http://localhost:8000/docs

Usuário admin padrão: admin / adminpass  (troque imediatamente)
