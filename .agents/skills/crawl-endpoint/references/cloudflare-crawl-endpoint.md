# Cloudflare Browser Rendering `/crawl`

Last checked: 2026-03-12

Official sources:

- `/crawl` guide: https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/
- `/crawl` markdown source: https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/index.md
- Browser Rendering limits: https://developers.cloudflare.com/browser-rendering/limits/
- Limits markdown source: https://developers.cloudflare.com/browser-rendering/limits/index.md
- Browser Rendering API reference landing page: https://developers.cloudflare.com/api/resources/browser_rendering/

## Endpoint Lifecycle

- Create job: `POST https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl`
- Read job: `GET https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl/<job_id>`
- Cancel job: `DELETE https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl/<job_id>`
- Auth: `Authorization: Bearer <apiToken>`
- Required request field: `url`

The endpoint is asynchronous:

1. `POST` returns a job id.
2. Poll `GET .../<job_id>?limit=1` until the job status is no longer `running`.
3. Fetch full results with `GET .../<job_id>`.
4. Page through results with `cursor` when present.

Job-level terminal states:

- `completed`
- `cancelled_due_to_timeout`
- `cancelled_due_to_limits`
- `cancelled_by_user`
- `errored`

Record-level statuses you can filter with the `GET` query string:

- `queued`
- `completed`
- `disallowed`
- `skipped`
- `errored`
- `cancelled`

Operational limits from the docs:

- Crawl jobs can run for up to 7 days.
- Completed job results are retained for 14 days.
- If a response exceeds 10 MB, Cloudflare returns a `cursor` for pagination.

## Core Query Parameters

`GET /crawl/{jobId}` supports:

- `cursor`: fetch the next result page.
- `limit`: cap returned records.
- `status`: filter records by record status.

Use `?limit=1` during polling to avoid downloading records before the crawl finishes.

## Request Parameters

Key parameters documented on the `/crawl` page:

| Parameter | Type | Notes |
| - | - | - |
| `limit` | number | Default `10`, max `100000` pages. |
| `depth` | number | Default `100000`, max `100000`. |
| `source` | string | `all` (default), `sitemaps`, or `links`. |
| `formats` | string[] | Default output is HTML; also supports Markdown and JSON. |
| `render` | boolean | Default `true`; `false` skips JS execution and performs a fast HTML fetch. |
| `jsonOptions` | object | Required when `formats` includes `json`; mirrors `/json` endpoint options. |
| `maxAge` | number | Default `86400`, max `604800` seconds. Cache only hits when URL and parameters match exactly. |
| `modifiedSince` | number | Unix timestamp in seconds; crawl only pages modified since that time. |
| `options.includeExternalLinks` | boolean | Follow external domains when `true`. Default `false`. |
| `options.includeSubdomains` | boolean | Follow subdomains when `true`. Default `false`. |
| `options.includePatterns` | string[] | Include-only wildcard patterns. |
| `options.excludePatterns` | string[] | Exclude wildcard patterns; higher priority than include patterns. |

Useful advanced parameters shown by the docs:

- `authenticate`: HTTP basic auth credentials.
- `cookies`: cookie-based auth/session support.
- `setExtraHTTPHeaders`: custom headers such as API keys.
- `gotoOptions`: browser navigation tuning such as `waitUntil` and `timeout`.
- `waitForSelector`: wait for hydrated content before extraction.
- `rejectResourceTypes`: skip `image`, `media`, `font`, `stylesheet`, and similar resource types.
- `userAgent`: override the page-level user agent.

Wildcard behavior:

- `*` matches any characters except `/`.
- `**` matches any characters including `/`.
- `excludePatterns` wins over `includePatterns`.

## Discovery Behavior

With `source: "all"` the crawler processes URLs in this order:

1. Starting URL
2. Sitemap URLs
3. Page links discovered during crawling

Use `source: "sitemaps"` when the site already publishes a reliable sitemap.
Use `source: "links"` when you want discovery to follow only in-page navigation.

## Format And Cost Guidance

- `formats: ["markdown"]` is the best default for documentation ingestion and RAG.
- `formats: ["json"]` uses Workers AI by default and should be paired with a clear extraction prompt and schema.
- `render: true` launches a headless browser and uses Browser Rendering pricing.
- `render: false` runs on Workers instead of a browser.
- During the `/crawl` beta, `render: false` crawls are not billed. Cloudflare states they will be billed under Workers pricing after beta.

## Robots, Bot Protection, And User Agent

- `/crawl` respects `robots.txt`, including `crawl-delay`.
- URLs blocked by `robots.txt` appear as records with `status: "disallowed"`.
- Cloudflare bot controls still apply to Browser Rendering crawls.
- Setting `userAgent` can change page content selection, but it does not bypass bot protection. Cloudflare states Browser Rendering requests are still identified as bot traffic.

## Plan Limits

Workers Free plan limits relevant to `/crawl`:

- Browser time: 10 minutes per day
- REST API rate: 6 requests per minute, effectively 1 request every 10 seconds
- `/crawl` jobs: 5 per day
- `/crawl` maximum pages per job: 100

Workers Paid plan limits relevant to REST API:

- Browser time: no fixed cap in the limits table
- REST API rate: 600 requests per minute, effectively 10 requests per second

If a crawl returns `cancelled_due_to_limits`, Cloudflare recommends:

- Upgrading to a paid plan
- Using `render: false` for static content
- Increasing `maxAge`
- Reducing `limit`

## Troubleshooting Cues

If the crawl returns no useful records:

- Check the target site's `robots.txt`.
- Remove `includePatterns` and `excludePatterns` temporarily.
- Try `source: "sitemaps"` if the start page has poor link discovery.
- Enable `includeSubdomains` or `includeExternalLinks` only when you actually need that broader scope.

If the crawl stays `running` too long:

- Use `render: false` if the page content exists in initial HTML.
- Lower `limit` and split the crawl into multiple smaller jobs.
- Block unneeded resources with `rejectResourceTypes`.
- Expect slowdown if the site enforces rate limits; Cloudflare documents backoff and `crawl-delay` compliance.

## Practical Notes For This Repo

The local helper script lives at `scripts/cloudflare-crawl.mjs` and wraps the REST lifecycle:

- Create: `node scripts/cloudflare-crawl.mjs --url https://example.com`
- Read an existing job: `node scripts/cloudflare-crawl.mjs --job-id <uuid>`
- Cache-only reuse: `node scripts/cloudflare-crawl.mjs --url https://example.com --cache-only`
- Force a fresh create: `node scripts/cloudflare-crawl.mjs --url https://example.com --refresh`
- Full advanced body: `node scripts/cloudflare-crawl.mjs --body-file .tmp/crawl-body.json`

Observed behavior in this repo on 2026-03-12:

- A just-created job may briefly return `404 Crawl job not found` during the first poll. Treat this as transient and retry.
- A Workers Free account may return `429 Rate limit exceeded` on `POST /crawl` after quota is consumed. Reusing an existing `jobId` still works as long as the result has not expired.
- Reusing an old `jobId` avoids creating a new crawl job, but `GET` requests still count against the REST API rate limit.

If JSON extraction looks wrong:

- Tighten the extraction prompt.
- Add a schema via `response_format`.
- Consider a custom model if the default Workers AI model is not sufficient.

## Minimal Request Templates

Create job:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl" \
  -H "Authorization: Bearer <apiToken>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","formats":["markdown"]}'
```

Poll status:

```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl/<job_id>?limit=1" \
  -H "Authorization: Bearer <apiToken>"
```

Fetch completed records:

```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl/<job_id>?status=completed&limit=100" \
  -H "Authorization: Bearer <apiToken>"
```

Cancel job:

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/<account_id>/browser-rendering/crawl/<job_id>" \
  -H "Authorization: Bearer <apiToken>"
```
