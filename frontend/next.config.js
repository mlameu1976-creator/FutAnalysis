/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/opportunities",
        destination: "http://127.0.0.1:8000/opportunities",
      },
    ];
  },
};

module.exports = nextConfig;
