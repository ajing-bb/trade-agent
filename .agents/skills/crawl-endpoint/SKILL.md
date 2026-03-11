---
name: crawl-endpoint
description: Create, explain, troubleshoot, or optimize Cloudflare Browser Rendering `/crawl` workflows. Use when Codex needs to start a crawl job, poll job status, paginate crawl results, cancel a crawl, choose `render`/`formats`/`source`/pattern filters, handle authenticated or JavaScript-heavy sites, or reason about `/crawl` limits, `robots.txt`, and `cancelled_due_to_limits`.
---

# Crawl Endpoint

Use this skill for Cloudflare Browser Rendering REST API `/crawl` work. Read [references/cloudflare-crawl-endpoint.md](references/cloudflare-crawl-endpoint.md) when you need exact defaults, limits, status values, or request examples from the official docs.

## Workflow

1. Confirm the user needs Cloudflare Browser Rendering `/crawl`, not a single-page endpoint such as `/content`, `/markdown`, or `/scrape`.
2. Start with the smallest valid `POST /crawl` body: a `url` plus only the parameters required for the site.
3. Model the async lifecycle explicitly:
   - `POST /crawl` to create the job and capture the job id.
   - `GET /crawl/{jobId}?limit=1` while polling so status checks stay lightweight.
   - `GET /crawl/{jobId}` without the polling limit once the job reaches a terminal state.
   - `DELETE /crawl/{jobId}` only when the user asks to cancel a running crawl.
4. When results are large, page with `cursor` until it disappears. Filter with result-query `status` only when the user asks for subsets such as `completed`, `skipped`, or `disallowed`.
5. Distinguish job status from per-record status when explaining results.

## Shape The Request

- Use `formats: ["markdown"]` for docs, RAG, summarization, and knowledge-base ingestion.
- Use `formats: ["json"]` with `jsonOptions` only for structured extraction. Call out that this uses Workers AI by default.
- Use `render: false` for static sites or server-rendered pages to reduce browser usage and cost.
- Use `gotoOptions` and `waitForSelector` for SPAs or pages that hydrate after load.
- Use `authenticate`, `cookies`, or `setExtraHTTPHeaders` for gated content.
- Use `source`, `depth`, `limit`, `includePatterns`, `excludePatterns`, `includeSubdomains`, `includeExternalLinks`, and `modifiedSince` to constrain scope.
- Use `rejectResourceTypes` to skip images, media, fonts, or stylesheets when they are not required for the target content.
- Use `maxAge` when repeated crawls can reuse cached results.

## Behavior Rules

- State that `/crawl` respects `robots.txt`, including `crawl-delay`.
- Do not claim that setting `userAgent` bypasses bot protection.
- Treat `excludePatterns` as higher priority than `includePatterns`.
- If the user is on Workers Free, check the free-plan crawl and browser limits before suggesting large `render: true` jobs.

## Troubleshooting

- Empty or mostly skipped results: inspect `robots.txt`, pattern filters, `source`, `depth`, and external/subdomain settings.
- Slow jobs: prefer `render: false`, lower `limit`, smaller batches, or `rejectResourceTypes`.
- `cancelled_due_to_limits`: recommend `render: false`, larger `maxAge`, smaller crawls, or a paid plan.
- `disallowed` records mean the crawler respected `robots.txt`.
- `skipped` records usually mean filters, scope settings, or `modifiedSince` excluded the URL.

## Output Expectations

- For code requests, provide a minimal `curl` example first. Add JavaScript `fetch` examples only when they materially help.
- For design or debugging questions, explain why each non-default parameter is present.
- When the user asks for exact limits or latest behavior, cite the official Cloudflare links listed in the reference file.
