// @ts-check
const { test, expect } = require("@playwright/test");
const path = require("path");
const fileUrl = "file:///" + path.resolve(__dirname, "../docs/index.html").replace(/\\/g, "/");

test.beforeEach(async ({ page }) => {
  await page.goto(fileUrl);
  await page.waitForLoadState("domcontentloaded");
  await page.waitForFunction(() => document.querySelectorAll(".sticker").length > 0, null, { timeout: 15000 });
});

test("no existe botón de actualización", async ({ page }) => {
  expect(await page.locator("#updBtn").count()).toBe(0);
});

test("header y contador cambian rojo→verde→amarillo con +/-", async ({ page }) => {
  const firstSummary = page.locator("details summary").first();
  if (!(await page.locator("details[open]").count())) {
    await firstSummary.click();
  }
  const card = page.locator("details[open] .sticker").first();
  const header = card.locator(".sticker-header");
  const counter = card.locator(".rep-value");

  await card.scrollIntoViewIfNeeded();

  await expect(counter).toHaveText("0");
  await expect(card).not.toHaveClass(/\bhave\b/);
  let bg = await header.evaluate((el) => getComputedStyle(el).backgroundImage);
  expect(bg).toMatch(/229,\s*62,\s*62|155,\s*41,\s*41/);

  await card.locator(".plus").click();
  await expect(counter).toHaveText("1");
  await expect(card).toHaveClass(/\bhave\b/);
  await expect(card).not.toHaveClass(/\bdup\b/);
  bg = await header.evaluate((el) => getComputedStyle(el).backgroundImage);
  expect(bg).toMatch(/25,\s*179,\s*107|14,\s*122,\s*69/);

  await card.locator(".plus").click();
  await expect(counter).toHaveText("2");
  await expect(card).toHaveClass(/\bdup\b/);
  bg = await header.evaluate((el) => getComputedStyle(el).backgroundImage);
  expect(bg).toMatch(/246,\s*180,\s*14|194,\s*125,\s*0/);

  await card.locator(".minus").click();
  await expect(counter).toHaveText("1");
  await expect(card).not.toHaveClass(/\bdup\b/);
  await expect(card).toHaveClass(/\bhave\b/);

  await card.locator(".minus").click();
  await expect(counter).toHaveText("0");
  await expect(card).not.toHaveClass(/\bhave\b/);
});

test("tab 'Todas' muestra 20 chips por país", async ({ page }) => {
  await page.locator("#summaryBtn").click();
  await page.locator("#tabTodas").click();
  const firstCountry = page.locator("#sumTodas .sum-country").first();
  await expect(firstCountry.locator(".sum-chip")).toHaveCount(20);
});

test("ESCUDO/EQUIPO aparecen en bio de tarjetas tipo L y F", async ({ page }) => {
  // Abrir TODOS los details para que se rendericen las cards
  await page.evaluate(() => {
    document.querySelectorAll("details").forEach(d => d.open = true);
  });
  // Debe existir al menos un ESCUDO y al menos un EQUIPO
  const textos = await page.locator(".bio-title").allTextContents();
  expect(textos).toContain("ESCUDO");
  expect(textos).toContain("EQUIPO");
});
