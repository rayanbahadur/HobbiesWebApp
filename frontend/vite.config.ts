import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  base: mode == "development" ? "http://localhost:5173/" : "/static/api/spa/",
  build: {
    emptyOutDir: true,
    outDir: "../api/static/api/spa",
  },
  plugins: [vue()],
  server: {
    proxy: {
      "/login": "http://127.0.0.1:8000/",
      "/signup": "http://127.0.0.1:8000/",
      "/logout": "http://127.0.0.1:8000/",
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(
        path.dirname(new URL(import.meta.url).pathname),
        "./src"
      ),
    },
  },
}));
