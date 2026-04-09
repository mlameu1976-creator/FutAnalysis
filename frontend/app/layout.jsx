import "./globals.css";

export const metadata = {
  title: "FutAnalysis",
  description: "Análise de apostas esportivas",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" translate="no">
      <body>{children}</body>
    </html>
  );
}