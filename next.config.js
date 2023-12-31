/** @type {import('next').NextConfig} */
let API_URL = 'http://127.0.0.1:5000'

if (process.env.API_URL) {
  API_URL = process.env.API_URL
}

const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',

  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${API_URL}/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
