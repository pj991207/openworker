// Local evidence harness; not part of the submitted change.
import { writeFileSync } from "node:fs";
import { expect } from "@playwright/test";
import { test, seedSessionMessages } from "./fixtures";

test("measure returning from settings to 200 messages", async ({ page }) => {
  test.setTimeout(120_000);
  const label = process.env.PERF_LABEL || "before";
  await seedSessionMessages(page, "pinned-cowork-1", Array.from({ length: 200 }, (_, i) => ({
    role: i % 2 ? "assistant" : "user",
    content: i % 2
      ? `## Answer ${i}\n\nHere is the **project update** with a [reference](https://example.com).\n\n` +
        "- Review the implementation\n- Verify the results\n- Document the changes\n\n".repeat(4) +
        "| Task | Status |\n| --- | --- |\n| Rendering | Complete |\n| Tests | Passing |\n\n```ts\nconst result = await run();\n```"
      : `Question ${i}: please summarize the project progress.`,
    ts: 1_700_000_000 + i * 60,
  })));
  await page.goto("/");
  await expect(page.locator(".bubble-assistant")).toHaveCount(100);
  const measurements = [];
  for (let run = 0; run < 3; run++) {
    await page.getByTestId("account-row").click();
    await page.getByRole("button", { name: "Settings", exact: true }).click();
    await expect(page.getByRole("heading", { name: "General" })).toBeVisible();
    await page.evaluate(() => {
      const w = window as any;
      w.perfEntries = [];
      w.perfObserver = new PerformanceObserver((list) => {
        w.perfEntries.push(...list.getEntries().map(e => ({ start: e.startTime, duration: e.duration })));
      });
      w.perfObserver.observe({ type: "longtask", buffered: false });
    });
    await page.getByRole("button", { name: "Back to app", exact: false }).click();
    await expect(page.locator(".bubble-assistant")).toHaveCount(100);
    await page.waitForTimeout(2000);
    measurements.push(await page.evaluate(() => {
      const w = window as any;
      w.perfObserver.disconnect();
      return { longTasks: w.perfEntries.length, totalMs: w.perfEntries.reduce((s: number, e: any) => s + e.duration, 0), entries: w.perfEntries };
    }));
    if (run === 0) await page.screenshot({ path: `transcript-${label}.png` });
  }
  writeFileSync(`transcript-${label}.json`, JSON.stringify(measurements, null, 2));
  console.log(label, JSON.stringify(measurements));
});
