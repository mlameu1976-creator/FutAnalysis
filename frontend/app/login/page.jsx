"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleLogin(e) {
    e.preventDefault();

    console.log("LOGIN CLICKADO"); // 🔥 DEBUG

    if (email && password) {
      router.push("/dashboard");
    } else {
      alert("Preencha os campos");
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "#0B0B0B",
      color: "white"
    }}>
      <form
        onSubmit={handleLogin}
        style={{
          background: "#161616",
          padding: "30px",
          borderRadius: "10px",
          width: "300px"
        }}
      >
        <h1 style={{ marginBottom: "20px" }}>
          Login FutAnalysis 🔐
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", marginBottom: "10px", padding: "8px" }}
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", marginBottom: "10px", padding: "8px" }}
        />

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "10px",
            background: "green",
            color: "white",
            border: "none",
            cursor: "pointer"
          }}
        >
          Entrar
        </button>
      </form>
    </div>
  );
}