# Field notes publishing guide

Site: https://nghiemhaphuongportfolio.netlify.app/blog/
Exact repository: `nghiemphuong263-sketch/nghiem-ha-phuong`, branch `main`.

The owner authorizes one original English article per run and public publication through this repository and the connected Netlify deployment. Read the current files before writing. Preserve unrelated files and existing articles. Update `blog/posts.json` with its current blob SHA through the connected GitHub tool. Netlify runs `python3 blog/build.py` to render the pages; do not edit generated HTML or overwrite the root portfolio.

## Topics and voice

Rotate fairly across these category IDs, prioritizing the least recently covered:

- `sustainable-finance-carbon-markets`
- `logistics-supply-chain`
- `research-methods`
- `applied-ai`
- `personal-development`

Write in clear English, sentence case, usually 700–1,000 words. One practical question per article, a direct short answer, meaningful headings, a worked illustrative example where useful, limitations, and a practical takeaway. Avoid generic introductions, forced contrasts, marketing language and keyword stuffing. Never invent the author's experience, qualifications, interviews, experiments, results or review. The author is Nghiêm Hà Phương. AI assistance is disclosed by the template.

## Evidence and originality

Search and open sources before writing. Prefer 3–5 relevant primary sources: original papers, official standards, governments, universities, regulators, multilateral institutions and official product documentation. Check dates, jurisdiction and whether a source directly supports the nearby claim. Put `[1]`, `[2]` etc. in paragraphs next to factual claims and include matching source objects. Distinguish source findings from original editorial analysis. A DOI proves a record's identity, not the validity of a claim. Do not fabricate references or claims of reading inaccessible full texts. Respect quotation and source-summary limits; write original analysis instead of closely rewriting sources. Inspect existing post titles and angles to avoid duplication. If current news is weak, choose an evergreen question; if evidence or image verification fails, report the blocker rather than publishing filler.

## Photography

Use an actual photograph from Pexels only; no generated images. Open the specific Pexels photo page, verify photographer and license, inspect that the image fits the article, and use its verified images.pexels.com image URL. Record the exact photo page, photographer and descriptive alt text. Do not invent image IDs or credits. No Pexels API key is required for a public photo-page lookup. Do not imply that a stock photograph depicts a real case or specific location unless verified.

## Search and AI discovery

Follow Google's official Search/AI-feature guidance and Bing webmaster guidelines, rechecking when they change. Answer the reader's actual question; use a natural descriptive title, useful description, visible citations, specific terminology and internal links. Do not promise rankings, indexing or AI citations. There is no special AI schema or magic keyword format. The generator creates HTML at `/blog/<slug>/`, canonical URLs, Article and breadcrumb JSON-LD, topic pages, sitemap and RSS. Preserve those features. Do not introduce hash-based article URLs, hidden AI instructions, fake FAQ schema, fake author credentials or manufactured statistics.

## Post format

Append an object to the JSON array. All content fields are plain text; HTML is escaped. `[n]` citations become links to the source list. Use the actual publication timestamp in Asia/Ho_Chi_Minh with its UTC offset. One publication per local date; if one already exists, report it and do not duplicate it.

```json
{
  "slug": "unique-descriptive-kebab-case",
  "title": "A specific question in sentence case",
  "category": "applied-ai",
  "description": "An accurate search description, usually around 140–160 characters.",
  "excerpt": "A concise explanation of what the reader will learn.",
  "answer": "A direct answer to the article's main question. [1]",
  "publishedAt": "2026-10-30T09:00:00+07:00",
  "published": true,
  "image": {
    "src": "https://images.pexels.com/photos/VERIFIED_ID/VERIFIED_FILENAME.jpeg?auto=compress&cs=tinysrgb&w=1600",
    "page": "https://www.pexels.com/photo/VERIFIED-PHOTO-PAGE/",
    "photographer": "Verified photographer name",
    "alt": "What the photograph actually shows"
  },
  "sections": [
    {"heading": "A useful section heading", "paragraphs": ["Plain text with a relevant citation. [1]"], "bullets": ["Optional practical point."]}
  ],
  "sources": [
    {"title": "Exact source title", "publisher": "Actual source organization", "url": "https://official.example/verified-page", "date": "Verified date or omit the date key"}
  ]
}
```

## Checks and delivery

Run `python3 blog/build.py` if an executor is available. Validate JSON, unique slugs, category, citations, timestamps, photographer, source links and image decoding. Inspect generated static HTML, canonical URL, schema and mobile layout where browser QA is available. Publish via the connected GitHub API using the current file SHA. After the commit, verify the live clean article URL returns the new title and article body; check `/sitemap.xml` includes it. Do not claim live publication from a commit alone. If Netlify is pending or failed, report that accurately. Deliver the live article link and a short factual status. Start time is scheduled; completion can follow later because research and deployment take time.

## Official guidance

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a
- https://www.pexels.com/license/
