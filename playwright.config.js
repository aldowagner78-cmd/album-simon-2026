// @ts-check
const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30000,
  retries: 0,
  reporter: "line",
  use: {
    baseURL: "file:///C:/Users/usuario/Desktop/FIGUS%20MUNDIAL/docs/index.html",
    headless: true,
    channel: "chromium",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
