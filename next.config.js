const { PHASE_DEVELOPMENT_SERVER, PHASE_PRODUCTION_SERVER, PHASE_PRODUCTION_BUILD } = require('next/constants')
let API_URL = 'http://127.0.0.1:5000'

module.exports = async (phase, { defaultConfig }) => {
  if (phase === PHASE_PRODUCTION_SERVER || phase === PHASE_PRODUCTION_BUILD) {
    API_URL = 'http://quant_exchange_api:5000'
  }

  /** @type {import('next').NextConfig} */
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
    eslint: {
      // Warning: This allows production builds to successfully complete even if
      // your project has ESLint errors.
      ignoreDuringBuilds: true,
    },
    typescript: {
      // !! WARN !!
      // Dangerously allow production builds to successfully complete even if
      // your project has type errors.
      // !! WARN !!
      ignoreBuildErrors:true,
    }
  }

  return nextConfig
}
