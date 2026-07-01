import { test, expect } from "@playwright/test";

test("customer can view account settings", async ({ page }) => {
  await page.goto("https://portal.staging.identitysec.internal");
  await expect(page.getByText("Manage your account")).toBeVisible();
});
