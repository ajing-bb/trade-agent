---
name: crawl-endpoint
description: Create, explain, execute, troubleshoot, or optimize Cloudflare Browser Rendering `/crawl` workflows. Use when Codex needs to start, reuse, resume, poll, paginate, or cancel a crawl job; choose `render`/`formats`/`jsonOptions`/`source`/pattern filters; handle authenticated or JavaScript-heavy sites; use the local helper script in this repo; or reason about `/crawl` limits, `robots.txt`, rate limits, and `cancelled_due_to_limits`.
---

# Crawl Endpoint

Use this skill for Cloudflare Browser Rendering REST API `/crawl` work. Read [references/cloudflare-crawl-endpoint.md](references/cloudflare-crawl-endpoint.md) when you need exact defaults, limits, status values, or request examples from the official docs and this repo's helper workflow.

## Workflow

1. Confirm the user needs Cloudflare Browser Rendering `/crawl`, not a single-page endpoint such as `/content`, `/markdown`, or `/scrape`.
2. If the user wants real execution in this repo, prefer the local helper script at `scripts/cloudflare-crawl.mjs` over ad hoc `curl`, because it already handles auth, job reuse, polling, paging, caching, and error messaging.
3. Reuse an existing crawl job before creating a new one:
   - Prefer an explicit `jobId` when the user already has one.
   - Prefer the local cache or `--cache-only` mode when a matching request was already run in this repo.
   - Use `POST /crawl` only when there is no reusable job or the user explicitly wants a refresh.
4. Model the async lifecycle explicitly:
   - `POST /crawl` to create the job and capture the job id.
   - `GET /crawl/{jobId}?limit=1` while polling so status checks stay lightweight.
   - `GET /crawl/{jobId}` without the polling limit once the job reaches a terminal state.
   - `DELETE /crawl/{jobId}` only when the user asks to cancel a running crawl.
5. When results are large, page with `cursor` until it disappears. Filter with result-query `status` only when the user asks for subsets such as `completed`, `skipped`, or `disallowed`.
6. Distinguish job status from per-record status when explaining results.

## Shape The Request

- Use `formats: ["markdown"]` for docs, RAG, summarization, and knowledge-base ingestion.
- Use `formats: ["json"]` with `jsonOptions` only for structured extraction. Call out that this uses Workers AI by default.
- When many uncommon or advanced fields are needed, prefer sending the full request body instead of forcing many small flags. In this repo, that means `--body-file`.
- Use `render: false` for static sites or server-rendered pages to reduce browser usage and cost.
- Use `gotoOptions` and `waitForSelector` for SPAs or pages that hydrate after load.
- Use `authenticate`, `cookies`, or `setExtraHTTPHeaders` for gated content.
- Use `source`, `depth`, `limit`, `includePatterns`, `excludePatterns`, `includeSubdomains`, `includeExternalLinks`, and `modifiedSince` to constrain scope.
- Use `rejectResourceTypes` to skip images, media, fonts, or stylesheets when they are not required for the target content.
- Use `maxAge` when repeated crawls can reuse cached results.

## Repo Helper

When working inside this repo, prefer `scripts/cloudflare-crawl.mjs` for execution.

- `--url <url>` runs a request and reuses a matching cached job when possible.
- `--job-id <uuid>` reads an existing job directly.
- `--cache-only` reuses cache or a provided `jobId` and never creates a new job.
- `--refresh` forces a fresh `POST /crawl`.
- `--body-file <path>` sends a full JSON request body for advanced cases.
- `--cancel` cancels an existing job.

## Behavior Rules

- State that `/crawl` respects `robots.txt`, including `crawl-delay`.
- Do not claim that setting `userAgent` bypasses bot protection.
- Treat `excludePatterns` as higher priority than `includePatterns`.
- If the user is on Workers Free, check the free-plan crawl and browser limits before suggesting large `render: true` jobs.
- Prefer reusing an existing job id or cache before suggesting a new `POST /crawl`, especially on Free plans.

## Troubleshooting

- Empty or mostly skipped results: inspect `robots.txt`, pattern filters, `source`, `depth`, and external/subdomain settings.
- Slow jobs: prefer `render: false`, lower `limit`, smaller batches, or `rejectResourceTypes`.
- `429 Rate limit exceeded`: reuse a cached job, use an explicit `jobId`, wait for the quota window to reset, or upgrade plans.
- A brief `404 Crawl job not found` right after `POST /crawl` can be transient; retry polling before assuming the job is gone.
- `cancelled_due_to_limits`: recommend `render: false`, larger `maxAge`, smaller crawls, or a paid plan.
- `disallowed` records mean the crawler respected `robots.txt`.
- `skipped` records usually mean filters, scope settings, or `modifiedSince` excluded the URL.

## Output Expectations

- For code requests, provide a minimal `curl` example first. Add JavaScript `fetch` examples only when they materially help.
- When the user is working in this repo and wants actual execution, prefer the local helper command instead of rewriting the workflow by hand.
- For design or debugging questions, explain why each non-default parameter is present.
- When the user asks for exact limits or latest behavior, cite the official Cloudflare links listed in the reference file.
