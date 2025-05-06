import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    allowedHosts: [
      'localhost',
      '0ffd-41-90-234-99.ngrok-free.app' // Add your ngrok host here
    ]
  }
});