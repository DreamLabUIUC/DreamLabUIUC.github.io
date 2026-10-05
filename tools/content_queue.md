# Blog content queue

> Superseded for scheduling by the Google Scholar-driven task (see BLOG_PLAYBOOK.md, Cadence). Keep as a list of ideas, e.g. for synthesis posts.

Work top to bottom. When a post ships, move its row to "Published" and add it to `tools/posts.json`.
Slots: **Mon** = recent paper explainer, **Wed** = classic paper revisited, **Fri** = synthesis / how-to that links several papers.

## Recent papers (Mon)

| # | Paper | Venue | Search angle (what people actually type) | Links to |
|---|-------|-------|-------------------------------------------|----------|
| 1 | ~~Reasoning can hurt the inductive abilities of LLMs~~ | NeurIPS 2025 | Already covered by `when_more_reasoning_is_actually_less.html`. Don't write a second post (it would compete with the first); instead add the arXiv link 2505.24225 and a citation block to that post. | |
| 2 | (skipped by author) GenoTEX: an LLM agent benchmark for automated gene expression analysis ([2406.15341](https://arxiv.org/abs/2406.15341)) | MLCB 2025 | "LLM agents for bioinformatics", "benchmark for AI gene expression analysis" | PSB 2026 paper, software.html (GenePrep) |
| 3 | Discovery of disease relationships via transcriptomic signatures, powered by agentic AI ([2508.04742](https://arxiv.org/abs/2508.04742)) | PSB 2026 | "agentic AI disease discovery", "AI finds links between diseases" | GenoTEX post |
| 4 | Vulnerability of content moderation guardrails via ... ([2505.18556](https://arxiv.org/abs/2505.18556)) | EMNLP Findings 2025 | "how LLM guardrails fail", "content moderation bypass research" | SecFid, cipher-character paper |
| 5 | Revolve: optimizing AI systems by tracking response evolution ([2412.03092](https://arxiv.org/abs/2412.03092)) | ICML 2025 | "TextGrad alternative", "textual gradient optimization" | evolution_of_prompt_optimization |
| 6 | CrossWordBench ([2504.00043](https://arxiv.org/abs/2504.00043)) | COLM 2025 | "crossword benchmark LLM", "LLM puzzle reasoning" | reasoning posts |
| 7 | Examining alignment of LLMs through representative heuristics: political stereotypes ([2501.14294](https://arxiv.org/abs/2501.14294)) | ICLR 2025 | "are LLMs politically biased" | ethics survey |
| 8 | Dataset distillation via the Wasserstein metric ([2311.18531](https://arxiv.org/abs/2311.18531)) | ICCV 2025 | "dataset distillation explained" | privacy-preserving distillation (ICCV 2025) |

## Classics worth revisiting (Wed)

Frame each as "N years later: what held up, what didn't". These already have citations and inbound links, so posts about them rank faster.

| # | Paper | Venue | Angle |
|---|-------|-------|-------|
| 1 | High-frequency component helps explain the generalization of CNNs | CVPR 2020 Oral | Do today's vision transformers and VLMs still rely on high-frequency shortcuts? |
| 2 | Language Agent Tree Search (LATS) | ICML 2024 | Tree search for agents, two years into the reasoning-model era |
| 3 | Robust Prompt Optimization against jailbreaking ([2401.17263](https://arxiv.org/abs/2401.17263)) | NeurIPS 2024 | Pair with SecFid: defenses and what they cost |
| 4 | Self-Challenging improves cross-domain generalization (RSC) | ECCV 2020 Oral | Domain generalization before and after foundation models |
| 5 | Learning robust representations by projecting superficial statistics out (HEX) | ICLR 2019 Oral | Shortcut learning, the idea that keeps coming back |
| 6 | Learning robust global representations by penalizing local predictive power (PAR) | NeurIPS 2019 | Same thread as HEX; could be one combined post |
| 7 | Measure and improve robustness in NLP models: a survey | NAACL 2022 | What changed for robustness once LLMs arrived |
| 8 | Jailbreaking LLMs against moderation guardrails via cipher characters ([2405.20413](https://arxiv.org/abs/2405.20413)) | NeurIPS 2024 | Pair with the EMNLP 2025 guardrail paper |
| 9 | On the origin of deep learning ([1702.07800](https://arxiv.org/abs/1702.07800)) | arXiv 2017 | A history of deep learning, revisited for the LLM era |
| 10 | Deep learning for genomics: a concise overview ([1802.00810](https://arxiv.org/abs/1802.00810)) | arXiv 2018 | What an update would look like in the age of genomic foundation models |

## Synthesis / how-to (Fri)

1. How to evaluate a prompt injection defense (SecFid + RPO + guardrail papers)
2. A reading list on shortcut learning and robustness, 2019 to 2026 (HEX, PAR, HFC, RSC, alignment regularization)
3. Using LLM agents for gene expression analysis: a practical guide (GenoTEX, GenePrep, PSB 2026)
4. When should an LLM think longer? A decision guide (reasoning papers + CrossWordBench)
5. Dataset distillation: robustness, privacy, and efficiency (AAAI 2025, ICCV 2025 x2)

## Published
- Agent Primitives (ICML 2026), SecFid (ICML 2026), CORE (4 posts), When more reasoning is less, Evolution of prompt optimization, 1000 ideas for trustworthy ML
