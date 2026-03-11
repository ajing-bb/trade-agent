#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const TERMINAL_STATUSES = new Set([
  "completed",
  "cancelled_due_to_timeout",
  "cancelled_due_to_limits",
  "cancelled_by_user",
  "errored",
]);

function loadEnvFile(envPath) {
  if (!fs.existsSync(envPath)) return;

  const source = fs.readFileSync(envPath, "utf8");
  for (const rawLine of source.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;

    const eqIndex = line.indexOf("=");
    if (eqIndex === -1) continue;

    const key = line.slice(0, eqIndex).trim();
    let value = line.slice(eqIndex + 1).trim();

    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

function parseArgs(argv) {
  const options = {
    url: "",
    render: false,
    limit: 1,
    formats: ["html", "markdown"],
    pollMs: 10000,
    maxAttempts: 60,
    status: "",
    save: "",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--url") {
      options.url = argv[++i] ?? "";
      continue;
    }

    if (arg === "--render") {
      options.render = (argv[++i] ?? "false") === "true";
      continue;
    }

    if (arg === "--limit") {
      options.limit = Number(argv[++i] ?? "1");
      continue;
    }

    if (arg === "--formats") {
      options.formats = (argv[++i] ?? "")
        .split(",")
        .map((value) => value.trim().toLowerCase())
        .filter(Boolean);
      continue;
    }

    if (arg === "--poll-ms") {
      options.pollMs = Number(argv[++i] ?? "10000");
      continue;
    }

    if (arg === "--max-attempts") {
      options.maxAttempts = Number(argv[++i] ?? "60");
      continue;
    }

    if (arg === "--status") {
      options.status = argv[++i] ?? "";
      continue;
    }

    if (arg === "--save") {
      options.save = argv[++i] ?? "";
      continue;
    }

    if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    }

    if (!arg.startsWith("--") && !options.url) {
      options.url = arg;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  if (!options.url) {
    throw new Error("Missing target URL. Pass it with --url <https://example.com>.");
  }

  if (!Number.isFinite(options.limit) || options.limit <= 0) {
    throw new Error("--limit must be a positive number.");
  }

  if (!Number.isFinite(options.pollMs) || options.pollMs <= 0) {
    throw new Error("--poll-ms must be a positive number.");
  }

  if (!Number.isFinite(options.maxAttempts) || options.maxAttempts <= 0) {
    throw new Error("--max-attempts must be a positive number.");
  }

  if (options.formats.length === 0) {
    options.formats = ["html", "markdown"];
  }

  return options;
}

function printHelp() {
  console.log(`Usage:
  node scripts/cloudflare-crawl.mjs --url <https://example.com>

Options:
  --render <true|false>      Execute page JavaScript. Default: false
  --limit <n>                Max pages in the crawl. Default: 1
  --formats <csv>            html,markdown,json. Default: html,markdown
  --poll-ms <n>              Poll interval in ms. Default: 10000
  --max-attempts <n>         Poll attempt cap. Default: 60
  --status <value>           Filter final records by status
  --save <path>              Save the full final result JSON to a file
  --help                     Show this help
`);
}

function getRequiredEnv(name) {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(`Missing ${name} in environment or .env.`);
  }
  return value;
}

async function sleep(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function requestJson(url, init) {
  const response = await fetch(url, init);
  const text = await response.text();

  let payload;
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(`Non-JSON response from Cloudflare (${response.status}): ${text}`);
  }

  if (!response.ok || payload.success === false) {
    const detail =
      payload.errors?.map((item) => item.message || JSON.stringify(item)).join("; ") ||
      payload.messages?.join("; ") ||
      JSON.stringify(payload);
    throw new Error(`Cloudflare API error (${response.status}): ${detail}`);
  }

  return payload;
}

function summarizeRecords(records) {
  const counts = new Map();
  for (const record of records) {
    const key = record.status || "unknown";
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return Object.fromEntries([...counts.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

function pickPreview(record) {
  if (!record) return "No records returned.";
  if (typeof record.markdown === "string" && record.markdown.trim()) {
    return record.markdown.replace(/\s+/g, " ").slice(0, 280);
  }
  if (typeof record.html === "string" && record.html.trim()) {
    return record.html.replace(/\s+/g, " ").slice(0, 280);
  }
  if (record.json) {
    return JSON.stringify(record.json).slice(0, 280);
  }
  return JSON.stringify(record).slice(0, 280);
}

async function main() {
  loadEnvFile(path.resolve(".env"));

  const options = parseArgs(process.argv.slice(2));
  const accountId = getRequiredEnv("CLOUDFLARE_ACCOUNT_ID");
  const apiToken = getRequiredEnv("CLOUDFLARE_API_TOKEN");
  const baseUrl = `https://api.cloudflare.com/client/v4/accounts/${accountId}/browser-rendering/crawl`;
  const headers = {
    Authorization: `Bearer ${apiToken}`,
    "Content-Type": "application/json",
  };

  const createBody = {
    url: options.url,
    limit: options.limit,
    render: options.render,
    formats: options.formats,
  };

  console.log(`Starting crawl for ${options.url}`);
  console.log(`Request: ${JSON.stringify(createBody)}`);

  const createPayload = await requestJson(baseUrl, {
    method: "POST",
    headers,
    body: JSON.stringify(createBody),
  });

  const jobId = createPayload.result;
  if (typeof jobId !== "string" || !jobId) {
    throw new Error(`Unexpected create response: ${JSON.stringify(createPayload)}`);
  }

  console.log(`Job created: ${jobId}`);

  let job;
  for (let attempt = 1; attempt <= options.maxAttempts; attempt += 1) {
    const pollPayload = await requestJson(`${baseUrl}/${jobId}?limit=1`, {
      method: "GET",
      headers,
    });

    job = pollPayload.result;
    console.log(
      `Poll ${attempt}/${options.maxAttempts}: status=${job.status} finished=${job.finished ?? "?"}/${job.total ?? "?"}`,
    );

    if (TERMINAL_STATUSES.has(job.status)) {
      break;
    }

    await sleep(options.pollMs);
  }

  if (!job || !TERMINAL_STATUSES.has(job.status)) {
    throw new Error("Crawl job did not reach a terminal status before timeout.");
  }

  const allRecords = [];
  let cursor = "";
  let finalResult;

  do {
    const query = new URLSearchParams();
    if (cursor) query.set("cursor", cursor);
    if (options.status) query.set("status", options.status);

    const url = query.size > 0 ? `${baseUrl}/${jobId}?${query}` : `${baseUrl}/${jobId}`;
    const pagePayload = await requestJson(url, { method: "GET", headers });

    finalResult = pagePayload.result;
    allRecords.push(...(finalResult.records ?? []));
    cursor = finalResult.cursor ?? "";
  } while (cursor);

  if (!finalResult) {
    throw new Error("No final result returned from Cloudflare.");
  }

  const output = {
    ...finalResult,
    records: allRecords,
  };

  if (options.save) {
    fs.mkdirSync(path.dirname(options.save), { recursive: true });
    fs.writeFileSync(options.save, `${JSON.stringify(output, null, 2)}\n`, "utf8");
    console.log(`Saved result to ${options.save}`);
  }

  console.log("");
  console.log("Crawl summary");
  console.log(`  jobId: ${output.id}`);
  console.log(`  status: ${output.status}`);
  console.log(`  total: ${output.total}`);
  console.log(`  finished: ${output.finished}`);
  console.log(`  browserSecondsUsed: ${output.browserSecondsUsed ?? 0}`);
  console.log(`  recordStatusCounts: ${JSON.stringify(summarizeRecords(allRecords))}`);

  if (allRecords.length > 0) {
    const first = allRecords[0];
    console.log("");
    console.log("First record");
    console.log(`  url: ${first.url}`);
    console.log(`  status: ${first.status}`);
    console.log(`  title: ${first.metadata?.title ?? "(none)"}`);
    console.log(`  httpStatus: ${first.metadata?.status ?? "(none)"}`);
    console.log(`  preview: ${pickPreview(first)}`);
  }

  if (output.status !== "completed") {
    process.exitCode = 2;
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
