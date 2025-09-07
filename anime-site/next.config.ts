import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'css.yhdmtu.xyz',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'css.yhdmtu.xyz',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'yhdmtu.xyz',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'yhdmtu.xyz',
        port: '',
        pathname: '/**',
      },
    ],
  },
};

export default nextConfig;
