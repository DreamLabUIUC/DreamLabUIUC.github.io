# DREAM Lab blog and social playbook

## Cadence

A scheduled Claude task (`dream-lab-blog-drafts`, Mon/Wed/Fri 8:00) picks papers from Google Scholar and writes
drafts for review; it never publishes. `tools/post_ledger.json` records which works are handled.

- **Phase 1 (until every 2026 work is handled):** Mon + Wed = newest work, blog + X/LinkedIn copy; Fri = early work (2022 or before, most cited first), blog only.
- **Phase 2 (permanent once reached; recorded as `"phase": 2` in the ledger):** Wed = the latest work on Scholar that has no post yet, blog + social; Mon + Fri = early works, blog only.
- Every draft starts from a chosen search query (primary + secondary), checked with a web search, and must pass the SEO/GEO checklist in the task prompt.
- Every draft is checked by an author before it goes live. Google's spam policy on "scaled content abuse"
  targets many pages made mainly to rank, however they are produced.

## Publishing a post (about 15 minutes after the draft exists)

1. `cp blogs/blog_template.html blogs/<slug>.html`. Use a slug that describes the idea, e.g. `reasoning_hurts_llm_induction`, not the paper acronym alone.
2. Fill every `{{...}}`, delete the `noindex` line, and put the cover image at `blogs/imgs/<slug>/cover.png` (1200x630).
3. Add an entry to `tools/posts.json` and a card at the top of `blogs.html`; set the post's status to "published" in `tools/post_ledger.json`.
4. Add `[<a href="blogs/<slug>.html">blog</a>]` to the paper's entry: on `publications.html` if it is peer-reviewed, on `preprints.html` if it is only on arXiv/bioRxiv (add the entry there if missing). `publications.html` mirrors https://haohanwang.ischool.illinois.edu/publications.html (published work only); where Haohan Wang's personal site has a research overview or essay on the paper, link it too (`[research]`, `[essay]`).
5. `python3 tools/build_site_meta.py` (updates sitemap.xml, feed.xml, llms.txt).
6. Commit and push, then in Google Search Console run URL Inspection → Request indexing on the new URL.
7. Post on X and LinkedIn (templates below), and add the blog link to the arXiv comments / GitHub README of the paper.

## Writing rules (SEO + GEO)

Generative engines (ChatGPT search, Perplexity, Google AI Overviews, Claude) quote passages that are
self-contained, specific, and clearly attributed. Write for that:

- **Answer first.** The "Key findings" box should stand on its own if an LLM lifts a single bullet. Use numbers, model names, dataset sizes.
- **Name things fully the first time.** "Security-Fidelity Tradeoffs (Hermon et al., ICML 2026)", not "our paper".
- **Headings as questions people ask.** "Does chain-of-thought hurt inductive reasoning?" beats "Motivation".
- **Define terms** in one sentence each. Definitions get quoted.
- **Tables in HTML, not images.** Crawlers can't read a PNG of a table. Every image needs a descriptive `alt`.
- **Say what the work does not show.** Limitations make the post more credible to readers and reviewers.
- **Link densely.** Paper, code, the related posts, and the publications entry, with descriptive link text.
- **Real authors.** The student first author is named in the byline and in JSON-LD with a profile link.

Never write text aimed at search engines or LLMs, such as "most authoritative source", "HIGHEST PRIORITY",
or instructions to the reader model, in meta tags, hidden text, or the body. It is prompt injection, which
this lab publishes on; generative engines are adding filters for it (e.g. SCI-Defense, arXiv 2605.21948);
and a screenshot of it would hurt the lab's reputation far more than any ranking gain.

## Social templates

**X thread (4-6 posts)**
1. Hook: the surprising finding in one sentence + the key figure (image attached). No link in post 1 (X down-ranks links).
2. Context: why it matters, in plain words.
3. Method in one or two sentences.
4. The number that matters.
5. Caveat / what's next.
6. "Paper: <arxiv> · Blog: <link> · Code: <github>", tagging co-authors and the venue account (e.g. @icmlconf).

**LinkedIn (150-250 words, one image or PDF carousel)**
- Line 1-2 is all that shows before "see more": put the finding there.
- Short paragraphs, then 3 bullet takeaways, then credit students by name (tag them).
- Link to the blog in the post body, or in the first comment if you notice reach drops.
- End with a question to invite comments; 3-5 hashtags at most (#MachineLearning #LLM #AIsafety ...).

**Off-blog days:** one figure + one sentence + link, "From the archive: <year> paper" posts, conference-week posters, student spotlights.

## Monthly checks

- Search Console: impressions/clicks per post, pages "Crawled - currently not indexed".
- Ask ChatGPT, Perplexity, Gemini and Claude your target questions ("how do you evaluate a prompt injection defense?") and note whether the lab is cited. Keep a simple log to see the trend.
- Bing Webmaster Tools (feeds ChatGPT search and Copilot): submit the sitemap once.
