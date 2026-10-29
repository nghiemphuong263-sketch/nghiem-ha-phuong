# Field notes: research-led publishing rules

Site: https://nghiemhaphuongportfolio.netlify.app/blog/
Repository: `nghiemphuong263-sketch/nghiem-ha-phuong`, branch `main`.
The owner authorizes public publication here and the existing Netlify site. Read current files before writes, preserve existing posts and unrelated code, and use the current blob SHA. Netlify runs `python3 blog/build.py`.

## Weekly mix and timing
One English article per local date, at most one how-to per ISO week in Asia/Ho_Chi_Minh. Monday is the normal how-to slot; Tuesday–Sunday publish research-led analysis. Check existing articleType and publication dates first. The existing 29 October 2026 how-to counts for that week; do not add another. If a how-to already exists in the week, publish research analysis instead. Never fill evidence gaps to meet the schedule. The 09:00 schedule starts research; publishing follows verification and deployment.

Categories: sustainable-finance-carbon-markets; logistics-supply-chain; research-methods; applied-ai; personal-development. Rotate reasonably across all five, subject to timely evidence. Research-led personal-development pieces must use measured outcomes and credible research, not generic advice.

## Freshness and research standard
Write around 800–1,200 words for research analysis and 700–1,000 for how-to, adjusting to substance. Lead with a research question, what the latest evidence shows, and why it matters now. Search globally for developments from the past 7 days. Prefer a new official release or study; widen to 30 days only when relevant, clearly dated and not already covered. Older foundational sources are allowed for definitions and context, not as fresh news. If data lag the event, use the most recent verified release, identify BOTH release date and observation period, and explain the lag. Do not treat an old report as new because a webpage was recently updated. Verify publication dates, not search snippets alone. Compare developments, quantify changes with explicit units and denominators, explain plausible mechanisms without presenting them as proven causal effects, discuss counterevidence and limitations, and relate findings to a concrete decision.

This is analysis of published research or secondary data, not a claim of conducting original peer-reviewed research. Never invent author experience, interviews, studies, experiments, qualifications, results or manual review. Do not reuse a topic merely by changing its headline.

## Data and figures
Every research article MUST include at least one meaningful quantitative chart; usually 1–3. Use verified published numerical observations and preserve the data in the post. Do not use AI-generated charts or made-up illustrative values. Keep units, currency, geographic scope, frequency, base year and sample consistent. Explain transformations and formulas, percentage versus percentage-point changes, and revisions when relevant. Avoid misleading axes. Charts have a title, period, unit, linked Harvard source citations, methodology and an accessible data table. The standard-library generator renders SVG bar/line charts directly from the stored numbers. A photograph is decorative and does not satisfy the chart requirement. If no defensible dataset exists, choose a different timely topic or report a blocker.

## Harvard citations and references
Use consistent author–date Harvard style: (World Bank, 2026), (Miao and Holmes, 2023), or (Autio et al., 2024). Add page/section locators in prose for precise source passages where useful. The JSON uses [1], [2] only as internal source keys; the template renders them as linked AUTHOR–DATE citations, never numbered footnotes. Each source MUST include author (reference-list form), citeAuthor (short in-text form), year (with a/b suffix when needed, or n.d. if genuinely undated), title, publisher, url and accessed (actual date read). References are alphabetized by author and include italic title, publisher, Available at URL, and Accessed date. Verify actual authors/year; do not silently substitute a corporate author for known personal authors. Full author lists are preferred in references. Match every citation to its source. Never fabricate an access date or imply reading inaccessible full text.

Browse and open 3–5 relevant primary sources where possible: original papers, official datasets, governments, central banks, universities, regulators, multilateral institutions and official documentation. Check the exact passage supporting each claim. Distinguish source findings from interpretation. Respect source quotation and summary limits. Original analysis must add value rather than closely rewrite a report. Keep evidenceAsOf as the actual evidence check date.

## Photography and discovery
Use only real Pexels photographs, never generated images. Open the exact photo page, verify credit/license and inspect the image. Record its exact images.pexels.com URL, Pexels page, photographer and descriptive alt text. Do not invent image IDs. Do not imply a stock image depicts a reported event or location.

Follow official Google/Bing guidance: useful original content, crawlable static HTML, clean URLs, natural titles/descriptions, visible sources, internal links, accurate schema and sitemap. No ranking or AI-citation promises, hidden prompts, keyword stuffing, special AI schema or fake FAQ/credentials. Preserve the current design and site behavior.

## JSON content schema
Append to blog/posts.json. Content is plain text, escaped by the template. [n] is a source key rendered as Harvard author–date. Actual timestamp must include +07:00; retain original publishedAt on edits and set updatedAt.
Required keys: slug, title, category, description, excerpt, answer, publishedAt, published, articleType ("how-to" or "research"), image {src,page,photographer,alt}, sections [{heading,paragraphs,bullets?}], sources [{author,citeAuthor,year,title,publisher,url,accessed}].
Research articles also REQUIRE evidenceAsOf (YYYY-MM-DD) and charts:
```json
{
 "type":"bar",
 "title":"Specific measurement and comparison",
 "unit":"Exact measurement unit",
 "period":"Actual observation period, distinct from release date",
 "method":"State data extraction, calculations, coverage and any limitations.",
 "sourceIds":[1],
 "labels":["Verified category or period A","Verified category or period B"],
 "values":[0,0]
}
```
The zeroes above are SCHEMA PLACEHOLDERS, not publishable data. Populate only from verified sources. Use type "bar" or "line", 2–12 matching labels/numeric values, sourceIds matching sources. For multiple series use separate well-explained charts. Cite data in prose as well as figure captions.

## Validation and publication
If an executor is available, run python3 blog/build.py. Validate JSON, dates, weekly how-to count, chart data/source correspondence, arithmetic, Harvard metadata, duplicate angles, photo attribution, static HTML, canonical/schema and sitemap. Publish only the content update via GitHub with its current SHA; do not overwrite generated HTML or the root portfolio. Check the live article URL and sitemap after Netlify builds. Report the real status and link. If research, photo, authorization or deployment is blocked, say what failed; never claim success from a commit alone or publish filler.

Official guidance:
https://developers.google.com/search/docs/appearance/ai-features
https://developers.google.com/search/docs/fundamentals/creating-helpful-content
https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a
https://www.pexels.com/license/
