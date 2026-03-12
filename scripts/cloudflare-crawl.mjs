#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DEFAULT_CACHE_PATH = path.resolve(".tmp/cloudflare-crawl-jobs.json");
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
    bodyFile: "",
    jobId: "",
    cancel: false,
    render: false,
    renderProvided: false,
    limit: 1,
    depth: null,
    source: "",
    maxAge: null,
    modifiedSince: null,
    formats: ["html", "markdown"],
    jsonPrompt: "",
    jsonSchemaFile: "",
    jsonResponseFormatFile: "",
    jsonOptionsFile: "",
    jsonCustomAiFile: "",
    includeSubdomains: false,
    includeExternalLinks: false,
    includePatterns: [],
    excludePatterns: [],
    headers: [],
    cookies: [],
    basicAuth: "",
    userAgent: "",
    gotoWaitUntil: "",
    gotoTimeout: null,
    waitForSelector: "",
    waitForSelectorTimeout: null,
    waitForSelectorVisible: false,
    rejectResourceTypes: [],
    pollMs: 10000,
    maxAttempts: 60,
    status: "",
    save: "",
    refresh: false,
    cache: DEFAULT_CACHE_PATH,
    cacheOnly: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--url") {
      options.url = argv[++i] ?? "";
      continue;
    }

    if (arg === "--body-file") {
      options.bodyFile = path.resolve(argv[++i] ?? "");
      continue;
    }

    if (arg === "--render") {
      options.renderProvided = true;
      options.render = (argv[++i] ?? "false") === "true";
      continue;
    }

    if (arg === "--job-id") {
      options.jobId = argv[++i] ?? "";
      continue;
    }

    if (arg === "--cancel") {
      options.cancel = true;
      continue;
    }

    if (arg === "--limit") {
      options.limit = Number(argv[++i] ?? "1");
      continue;
    }

    if (arg === "--depth") {
      options.depth = Number(argv[++i] ?? "0");
      continue;
    }

    if (arg === "--source") {
      options.source = (argv[++i] ?? "").trim();
      continue;
    }

    if (arg === "--max-age") {
      options.maxAge = Number(argv[++i] ?? "0");
      continue;
    }

    if (arg === "--modified-since") {
      options.modifiedSince = Number(argv[++i] ?? "0");
      continue;
    }

    if (arg === "--formats") {
      options.formats = (argv[++i] ?? "")
        .split(",")
        .map((value) => value.trim().toLowerCase())
        .filter(Boolean);
      continue;
    }

    if (arg === "--json-prompt") {
      options.jsonPrompt = argv[++i] ?? "";
      continue;
    }

    if (arg === "--json-schema-file") {
      options.jsonSchemaFile = path.resolve(argv[++i] ?? "");
      continue;
    }

    if (arg === "--json-response-format-file") {
      options.jsonResponseFormatFile = path.resolve(argv[++i] ?? "");
      continue;
    }

    if (arg === "--json-options-file") {
      options.jsonOptionsFile = path.resolve(argv[++i] ?? "");
      continue;
    }

    if (arg === "--json-custom-ai-file") {
      options.jsonCustomAiFile = path.resolve(argv[++i] ?? "");
      continue;
    }

    if (arg === "--include-subdomains") {
      options.includeSubdomains = true;
      continue;
    }

    if (arg === "--include-external-links") {
      options.includeExternalLinks = true;
      continue;
    }

    if (arg === "--include-pattern") {
      options.includePatterns.push(argv[++i] ?? "");
      continue;
    }

    if (arg === "--exclude-pattern") {
      options.excludePatterns.push(argv[++i] ?? "");
      continue;
    }

    if (arg === "--header") {
      options.headers.push(argv[++i] ?? "");
      continue;
    }

    if (arg === "--cookie") {
      options.cookies.push(argv[++i] ?? "");
      continue;
    }

    if (arg === "--basic-auth") {
      options.basicAuth = argv[++i] ?? "";
      continue;
    }

    if (arg === "--user-agent") {
      options.userAgent = argv[++i] ?? "";
      continue;
    }

    if (arg === "--goto-wait-until") {
      options.gotoWaitUntil = argv[++i] ?? "";
      continue;
    }

    if (arg === "--goto-timeout") {
      options.gotoTimeout = Number(argv[++i] ?? "0");
      continue;
    }

    if (arg === "--wait-for-selector") {
      options.waitForSelector = argv[++i] ?? "";
      continue;
    }

    if (arg === "--wait-for-selector-timeout") {
      options.waitForSelectorTimeout = Number(argv[++i] ?? "0");
      continue;
    }

    if (arg === "--wait-for-selector-visible") {
      options.waitForSelectorVisible = true;
      continue;
    }

    if (arg === "--reject-resource-type") {
      options.rejectResourceTypes.push((argv[++i] ?? "").trim());
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

    if (arg === "--refresh") {
      options.refresh = true;
      continue;
    }

    if (arg === "--cache") {
      options.cache = path.resolve(argv[++i] ?? DEFAULT_CACHE_PATH);
      continue;
    }

    if (arg === "--cache-only") {
      options.cacheOnly = true;
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

  if (!options.url && !options.bodyFile && !options.jobId) {
    throw new Error(
      "Missing target URL, body file, or job id. Pass --url <https://example.com>, --body-file <path>, or --job-id <uuid>.",
    );
  }

  if (!Number.isFinite(options.limit) || options.limit <= 0) {
    throw new Error("--limit must be a positive number.");
  }

  if (options.depth !== null && (!Number.isFinite(options.depth) || options.depth < 0)) {
    throw new Error("--depth must be zero or a positive number.");
  }

  if (options.maxAge !== null && (!Number.isFinite(options.maxAge) || options.maxAge < 0)) {
    throw new Error("--max-age must be zero or a positive number.");
  }

  if (
    options.modifiedSince !== null &&
    (!Number.isFinite(options.modifiedSince) || options.modifiedSince < 0)
  ) {
    throw new Error("--modified-since must be zero or a positive Unix timestamp.");
  }

  if (
    options.gotoTimeout !== null &&
    (!Number.isFinite(options.gotoTimeout) || options.gotoTimeout <= 0)
  ) {
    throw new Error("--goto-timeout must be a positive number.");
  }

  if (
    options.waitForSelectorTimeout !== null &&
    (!Number.isFinite(options.waitForSelectorTimeout) || options.waitForSelectorTimeout <= 0)
  ) {
    throw new Error("--wait-for-selector-timeout must be a positive number.");
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

  if (options.cacheOnly && options.refresh) {
    throw new Error("--cache-only and --refresh cannot be used together.");
  }

  if (options.bodyFile && options.url) {
    throw new Error("--body-file cannot be combined with --url.");
  }

  if (options.source && !["all", "sitemaps", "links"].includes(options.source)) {
    throw new Error("--source must be one of: all, sitemaps, links.");
  }

  if (
    options.jsonOptionsFile &&
    (options.jsonPrompt || options.jsonSchemaFile || options.jsonResponseFormatFile || options.jsonCustomAiFile)
  ) {
    throw new Error(
      "--json-options-file cannot be combined with --json-prompt, --json-schema-file, --json-response-format-file, or --json-custom-ai-file.",
    );
  }

  if (
    options.gotoWaitUntil &&
    !["load", "domcontentloaded", "networkidle0", "networkidle2"].includes(options.gotoWaitUntil)
  ) {
    throw new Error("--goto-wait-until must be one of: load, domcontentloaded, networkidle0, networkidle2.");
  }

  if (
    (options.waitForSelector ||
      options.gotoWaitUntil ||
      options.gotoTimeout !== null ||
      options.waitForSelectorTimeout !== null ||
      options.waitForSelectorVisible ||
      options.rejectResourceTypes.length > 0) &&
    !options.renderProvided
  ) {
    options.render = true;
  }

  return options;
}

function printHelp() {
  console.log(`Usage:
  node scripts/cloudflare-crawl.mjs --url <https://example.com>
  node scripts/cloudflare-crawl.mjs --body-file <crawl-body.json>
  node scripts/cloudflare-crawl.mjs --job-id <uuid>

Options:
  --body-file <path>         Full POST /crawl JSON body file
  --job-id <uuid>            Read an existing crawl job without creating a new one
  --cancel                   Cancel an existing crawl job and exit
  --render <true|false>      Execute page JavaScript. Default: false
  --limit <n>                Max pages in the crawl. Default: 1
  --depth <n>                Max crawl depth
  --source <value>           all, sitemaps, or links
  --max-age <seconds>        Reuse cached crawl results when possible
  --modified-since <unix>    Only crawl pages modified after this timestamp
  --formats <csv>            html,markdown,json. Default: html,markdown
  --json-prompt <text>       Prompt for formats=json extraction
  --json-schema-file <path>  JSON Schema file, wrapped as response_format
  --json-response-format-file <path>
                            Full response_format JSON file
  --json-custom-ai-file <path>
                            custom_ai array JSON file
  --json-options-file <path> Full jsonOptions JSON file
  --include-subdomains       Follow subdomains
  --include-external-links   Follow external domains
  --include-pattern <glob>   Include-only URL pattern, repeatable
  --exclude-pattern <glob>   Exclude URL pattern, repeatable
  --header "K: V"            Extra HTTP header, repeatable
  --cookie "a=b; Domain=x"   Cookie for authenticated pages, repeatable
  --basic-auth user:pass     HTTP Basic Auth credentials
  --user-agent <value>       Override the default crawler user agent
  --goto-wait-until <value>  load, domcontentloaded, networkidle0, networkidle2
  --goto-timeout <ms>        Navigation timeout for render mode
  --wait-for-selector <css>  Wait for a selector before extraction
  --wait-for-selector-timeout <ms>
                            Selector wait timeout
  --wait-for-selector-visible
                            Require the selector to be visible
  --reject-resource-type <kind>
                            Block resource types like image, media, font, stylesheet
  --poll-ms <n>              Poll interval in ms. Default: 10000
  --max-attempts <n>         Poll attempt cap. Default: 60
  --status <value>           Filter final records by status
  --save <path>              Save the full final result JSON to a file
  --refresh                  Force a new POST /crawl even if a cached job exists
  --cache <path>             Cache file path. Default: .tmp/cloudflare-crawl-jobs.json
  --cache-only               Reuse cache or --job-id only; never POST /crawl
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
    const retryAfterHeader = response.headers.get("retry-after");
    const retryAfterSeconds = retryAfterHeader ? Number(retryAfterHeader) : Number.NaN;
    const error = new Error(`Cloudflare API error (${response.status}): ${detail}`);
    error.status = response.status;
    error.detail = detail;
    error.retryAfterMs = Number.isFinite(retryAfterSeconds) ? retryAfterSeconds * 1000 : null;
    throw error;
  }

  return payload;
}

function isRateLimitError(error) {
  return (
    error instanceof Error &&
    "status" in error &&
    Number(error.status) === 429
  );
}

function getRetryDelayMs(error, fallbackMs) {
  if (
    error instanceof Error &&
    "retryAfterMs" in error &&
    typeof error.retryAfterMs === "number" &&
    Number.isFinite(error.retryAfterMs) &&
    error.retryAfterMs > 0
  ) {
    return error.retryAfterMs;
  }

  return fallbackMs;
}

function shouldRetryRateLimit(error, fallbackMs) {
  const delayMs = getRetryDelayMs(error, fallbackMs);
  return delayMs <= 30000;
}

function extractJobId(payload) {
  if (typeof payload.result === "string" && payload.result) {
    return payload.result;
  }

  if (
    payload.result &&
    typeof payload.result === "object" &&
    typeof payload.result.id === "string" &&
    payload.result.id
  ) {
    return payload.result.id;
  }

  throw new Error(`Unexpected create response: ${JSON.stringify(payload)}`);
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

function readCache(cachePath) {
  if (!fs.existsSync(cachePath)) {
    return { entries: [] };
  }

  try {
    const value = JSON.parse(fs.readFileSync(cachePath, "utf8"));
    if (!value || typeof value !== "object" || !Array.isArray(value.entries)) {
      return { entries: [] };
    }
    return value;
  } catch {
    return { entries: [] };
  }
}

function writeCache(cachePath, cache) {
  fs.mkdirSync(path.dirname(cachePath), { recursive: true });
  fs.writeFileSync(cachePath, `${JSON.stringify(cache, null, 2)}\n`, "utf8");
}

function getRequestFingerprint(options) {
  return JSON.stringify(buildCreateBody(options));
}

function findCachedJob(cache, options) {
  if (!options.url && !options.bodyFile) return null;

  const fingerprint = getRequestFingerprint(options);
  const match = [...cache.entries]
    .reverse()
    .find((entry) => entry.fingerprint === fingerprint && typeof entry.jobId === "string");

  return match ?? null;
}

function upsertCacheEntry(cache, entry) {
  const nextEntries = cache.entries.filter((item) => item.jobId !== entry.jobId);
  nextEntries.push(entry);
  cache.entries = nextEntries.slice(-50);
}

function buildCacheEntry({ jobId, options, status, sourceUrl }) {
  return {
    jobId,
    url: sourceUrl || options.url || "",
    fingerprint: options.url || options.bodyFile ? getRequestFingerprint(options) : "",
    render: options.render,
    limit: options.limit,
    formats: options.formats,
    status,
    updatedAt: new Date().toISOString(),
  };
}

function buildRateLimitGuidance(options) {
  const hints = [
    "Cloudflare rejected POST /crawl with 429 Rate limit exceeded.",
    "Use an existing job via --job-id <uuid> if you already have one.",
    `Reuse the local cache by keeping ${options.cache} and rerunning the same --url.`,
    "Or wait for the account quota window to reset before creating a new crawl job.",
  ];

  if (options.url) {
    hints.push(`For read-only reuse, run: node scripts/cloudflare-crawl.mjs --url ${options.url} --cache-only`);
  }

  return hints.join(" ");
}

function parseHeader(value) {
  const separatorIndex = value.indexOf(":");
  if (separatorIndex === -1) {
    throw new Error(`Invalid --header value: ${value}. Expected "Name: Value".`);
  }

  const name = value.slice(0, separatorIndex).trim();
  const headerValue = value.slice(separatorIndex + 1).trim();
  if (!name || !headerValue) {
    throw new Error(`Invalid --header value: ${value}. Expected "Name: Value".`);
  }

  return [name, headerValue];
}

function parseBasicAuth(value) {
  const separatorIndex = value.indexOf(":");
  if (separatorIndex === -1) {
    throw new Error(`Invalid --basic-auth value: ${value}. Expected "username:password".`);
  }

  const username = value.slice(0, separatorIndex);
  const password = value.slice(separatorIndex + 1);
  if (!username || !password) {
    throw new Error(`Invalid --basic-auth value: ${value}. Expected "username:password".`);
  }

  return { username, password };
}

function parseCookie(value) {
  const parts = value
    .split(";")
    .map((part) => part.trim())
    .filter(Boolean);

  const first = parts.shift();
  if (!first) {
    throw new Error(`Invalid --cookie value: ${value}. Expected "name=value; Domain=example.com; Path=/".`);
  }

  const separatorIndex = first.indexOf("=");
  if (separatorIndex === -1) {
    throw new Error(`Invalid --cookie value: ${value}. Expected "name=value; Domain=example.com; Path=/".`);
  }

  const cookie = {
    name: first.slice(0, separatorIndex).trim(),
    value: first.slice(separatorIndex + 1).trim(),
  };

  if (!cookie.name) {
    throw new Error(`Invalid --cookie value: ${value}. Cookie name is required.`);
  }

  for (const part of parts) {
    const [rawKey, ...rawValueParts] = part.split("=");
    const key = rawKey.trim().toLowerCase();
    const attrValue = rawValueParts.join("=").trim();

    if (key === "domain" && attrValue) cookie.domain = attrValue;
    if (key === "path" && attrValue) cookie.path = attrValue;
    if (key === "secure") cookie.secure = true;
  }

  return cookie;
}

function readJsonFile(filePath, label) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to read ${label} at ${filePath}: ${reason}`);
  }
}

function buildCreateBody(options) {
  if (options.bodyFile) {
    const body = readJsonFile(options.bodyFile, "crawl body file");
    if (!body || typeof body !== "object" || Array.isArray(body)) {
      throw new Error("--body-file must contain a JSON object.");
    }
    if (!body.url || typeof body.url !== "string") {
      throw new Error("--body-file JSON must contain a string url field.");
    }
    return body;
  }

  const body = {
    url: options.url,
    limit: options.limit,
    render: options.render,
    formats: options.formats,
  };

  if (options.depth !== null) body.depth = options.depth;
  if (options.source) body.source = options.source;
  if (options.maxAge !== null) body.maxAge = options.maxAge;
  if (options.modifiedSince !== null) body.modifiedSince = options.modifiedSince;
  if (options.userAgent) body.userAgent = options.userAgent;

  const wantsJson = body.formats.includes("json");
  if (wantsJson) {
    let jsonOptions;

    if (options.jsonOptionsFile) {
      jsonOptions = readJsonFile(options.jsonOptionsFile, "jsonOptions file");
    } else {
      jsonOptions = {};
      if (options.jsonPrompt) {
        jsonOptions.prompt = options.jsonPrompt;
      }
      if (options.jsonResponseFormatFile) {
        jsonOptions.response_format = readJsonFile(
          options.jsonResponseFormatFile,
          "JSON response_format file",
        );
      } else if (options.jsonSchemaFile) {
        jsonOptions.response_format = {
          type: "json_schema",
          schema: readJsonFile(options.jsonSchemaFile, "JSON schema file"),
        };
      }
      if (options.jsonCustomAiFile) {
        jsonOptions.custom_ai = readJsonFile(options.jsonCustomAiFile, "custom_ai file");
      }
    }

    const hasJsonExtractionConfig = Boolean(
      jsonOptions &&
        typeof jsonOptions === "object" &&
        (jsonOptions.prompt || jsonOptions.response_format || jsonOptions.custom_ai),
    );

    if (!hasJsonExtractionConfig) {
      throw new Error(
        'formats includes "json" but no jsonOptions were provided. Use --json-prompt, --json-schema-file, --json-response-format-file, --json-custom-ai-file, or --json-options-file.',
      );
    }

    body.jsonOptions = jsonOptions;
  }

  if (options.basicAuth) {
    body.authenticate = parseBasicAuth(options.basicAuth);
  }

  if (options.headers.length > 0) {
    body.setExtraHTTPHeaders = Object.fromEntries(options.headers.map(parseHeader));
  }

  if (options.cookies.length > 0) {
    body.cookies = options.cookies.map(parseCookie);
  }

  if (options.gotoWaitUntil || options.gotoTimeout !== null) {
    body.gotoOptions = {};
    if (options.gotoWaitUntil) body.gotoOptions.waitUntil = options.gotoWaitUntil;
    if (options.gotoTimeout !== null) body.gotoOptions.timeout = options.gotoTimeout;
  }

  if (options.waitForSelector) {
    body.waitForSelector = { selector: options.waitForSelector };
    if (options.waitForSelectorTimeout !== null) {
      body.waitForSelector.timeout = options.waitForSelectorTimeout;
    }
    if (options.waitForSelectorVisible) {
      body.waitForSelector.visible = true;
    }
  }

  if (options.rejectResourceTypes.length > 0) {
    body.rejectResourceTypes = options.rejectResourceTypes;
  }

  const crawlOptions = {};
  if (options.includeExternalLinks) crawlOptions.includeExternalLinks = true;
  if (options.includeSubdomains) crawlOptions.includeSubdomains = true;
  if (options.includePatterns.length > 0) crawlOptions.includePatterns = options.includePatterns;
  if (options.excludePatterns.length > 0) crawlOptions.excludePatterns = options.excludePatterns;
  if (Object.keys(crawlOptions).length > 0) {
    body.options = crawlOptions;
  }

  return body;
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
  const cache = readCache(options.cache);
  const createBody = options.url || options.bodyFile ? buildCreateBody(options) : null;

  async function createCrawlJob() {
    console.log(`Starting crawl for ${options.url}`);
    console.log(`Request: ${JSON.stringify(createBody)}`);

    let createPayload;
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        createPayload = await requestJson(baseUrl, {
          method: "POST",
          headers,
          body: JSON.stringify(createBody),
        });
        break;
      } catch (error) {
        if (
          !isRateLimitError(error) ||
          !shouldRetryRateLimit(error, 10000) ||
          attempt === 3
        ) {
          if (isRateLimitError(error)) {
            throw new Error(buildRateLimitGuidance(options));
          }
          throw error;
        }

        const delayMs = getRetryDelayMs(error, 10000);
        console.log(`Create hit rate limit, retrying in ${delayMs}ms`);
        await sleep(delayMs);
      }
    }

    const nextJobId = extractJobId(createPayload);
    upsertCacheEntry(cache, buildCacheEntry({ jobId: nextJobId, options, status: "created" }));
    writeCache(options.cache, cache);
    console.log(`Job created: ${nextJobId}`);
    return nextJobId;
  }

  let jobId = options.jobId;
  let reusedCachedJob = false;
  if (!jobId && !options.refresh) {
    const cached = findCachedJob(cache, options);
    if (cached) {
      jobId = cached.jobId;
      reusedCachedJob = true;
      console.log(`Using cached job: ${jobId}`);
    }
  }

  if (!jobId && (options.cacheOnly || options.cancel)) {
    throw new Error(
      `No cached crawl job matched this request in ${options.cache}. Pass --job-id <uuid>, remove --cache-only, or recreate the crawl later.`,
    );
  }

  if (!jobId) {
    jobId = await createCrawlJob();
  } else {
    console.log(`Reading crawl job ${jobId}`);
  }

  if (options.cancel) {
    await requestJson(`${baseUrl}/${jobId}`, {
      method: "DELETE",
      headers,
    });
    upsertCacheEntry(cache, buildCacheEntry({ jobId, options, status: "cancelled_by_user" }));
    writeCache(options.cache, cache);
    console.log(`Cancelled crawl job ${jobId}`);
    return;
  }

  let job;
  for (let attempt = 1; attempt <= options.maxAttempts; attempt += 1) {
    let pollPayload;
    try {
      pollPayload = await requestJson(`${baseUrl}/${jobId}?limit=1`, {
        method: "GET",
        headers,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (
        isRateLimitError(error) &&
        shouldRetryRateLimit(error, options.pollMs) &&
        attempt < options.maxAttempts
      ) {
        const delayMs = getRetryDelayMs(error, options.pollMs);
        console.log(`Poll ${attempt}/${options.maxAttempts}: rate limited, retrying in ${delayMs}ms`);
        await sleep(delayMs);
        continue;
      }

      const isTransientNotFound =
        message.includes("Cloudflare API error (404)") &&
        message.includes("Crawl job not found") &&
        !options.jobId &&
        attempt < options.maxAttempts;

      if (reusedCachedJob && attempt === 1 && message.includes("Crawl job not found")) {
        console.log("Cached job expired or missing, creating a fresh crawl job");
        jobId = await createCrawlJob();
        reusedCachedJob = false;
        continue;
      }

      if (!isTransientNotFound) {
        throw error;
      }

      console.log(
        `Poll ${attempt}/${options.maxAttempts}: job not visible yet, retrying in ${options.pollMs}ms`,
      );
      await sleep(options.pollMs);
      continue;
    }

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
    let pagePayload;
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        pagePayload = await requestJson(url, { method: "GET", headers });
        break;
      } catch (error) {
        if (
          !isRateLimitError(error) ||
          !shouldRetryRateLimit(error, 10000) ||
          attempt === 3
        ) {
          throw error;
        }

        const delayMs = getRetryDelayMs(error, 10000);
        console.log(`Fetch page hit rate limit, retrying in ${delayMs}ms`);
        await sleep(delayMs);
      }
    }

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

  const sourceUrl = allRecords[0]?.url || output.url || options.url;
  upsertCacheEntry(cache, buildCacheEntry({ jobId, options, status: output.status, sourceUrl }));
  writeCache(options.cache, cache);

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
