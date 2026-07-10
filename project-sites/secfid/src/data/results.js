// Result data for figures, taken from analysis/frontier_plot_data.csv,
// analysis/repair_vs_suppress.csv, analysis/reasoning_plot_data.csv, and
// analysis/fidelity_dpo_results.csv in the sec-fid repository.
// Values are percentages (security = 1 - exec, fidelity = 1 - ignore).

export const frontier = [
  { label: 'Claude Haiku 4.5', sec: 69.3, fid: 77.3, kind: 'closed' },
  { label: 'Claude Sonnet 4.6', sec: 81.8, fid: 68.8, kind: 'closed' },
  { label: 'Claude Opus 4.6', sec: 85.2, fid: 67.7, kind: 'closed', anchor: 'e' },
  { label: 'Gemini 3.1 Flash-Lite', sec: 54.5, fid: 89.9, kind: 'closed' },
  { label: 'Gemini 3 Flash', sec: 63.4, fid: 90.4, kind: 'closed' },
  { label: 'GPT-5.4 Nano', sec: 72.9, fid: 87.8, kind: 'closed' },
  { label: 'GPT-5.4 Mini', sec: 61.6, fid: 89.9, kind: 'closed' },
  { label: 'GPT-5.4', sec: 74.0, fid: 83.2, kind: 'closed', anchor: 'e' },
  { label: 'Gemma 3 12B', sec: 70.6, fid: 91.2, kind: 'open' },
  { label: 'Gemma 3 27B', sec: 72.7, fid: 91.6, kind: 'open' },
  { label: 'Llama 3.1 8B', sec: 50.9, fid: 92.3, kind: 'open', anchor: 'e' },
  { label: 'Llama 3.1 8B + ASIDE', sec: 94.3, fid: 75.3, kind: 'defense' },
  { label: 'Llama 3.1 8B + Def. tokens', sec: 98.1, fid: 46.3, kind: 'defense', anchor: 'w' },
  { label: 'Llama 3.1 8B + ISE', sec: 86.0, fid: 79.7, kind: 'defense' },
  { label: 'Llama 3.1 8B + SecAlign', sec: 99.3, fid: 73.9, kind: 'defense', anchor: 'w' },
  { label: 'Llama 3.3 70B', sec: 47.8, fid: 96.5, kind: 'open', anchor: 'e' },
  { label: 'Llama 3.3 70B + SecAlign', sec: 99.3, fid: 71.0, kind: 'defense', anchor: 'w' },
  { label: 'Qwen 2.5 7B', sec: 67.8, fid: 81.4, kind: 'open' },
  { label: 'Qwen 2.5 7B + ASIDE', sec: 92.5, fid: 73.0, kind: 'defense' },
  { label: 'Qwen 2.5 7B + Def. tokens', sec: 96.9, fid: 43.5, kind: 'defense', anchor: 'w' },
  { label: 'Qwen 2.5 7B + ISE', sec: 80.7, fid: 76.2, kind: 'defense' },
  { label: 'Qwen 2.5 14B', sec: 49.8, fid: 92.9, kind: 'open' },
  { label: 'Qwen 2.5 32B', sec: 66.0, fid: 89.6, kind: 'open' },
];

// What each defense does with the 574 examples the undefended
// Llama 3.1 8B executed (repair_vs_suppress.csv).
export const repairSuppress = [
  { label: 'SecAlign', sec: 99.3, repaired: 54.0, suppressed: 36.6, executed: 1.2, other: 8.2 },
  { label: 'ISE', sec: 86.0, repaired: 44.3, suppressed: 20.0, executed: 22.0, other: 13.8 },
  { label: 'ASIDE', sec: 94.3, repaired: 35.5, suppressed: 22.0, executed: 9.1, other: 33.4 },
  { label: 'Defensive tokens', sec: 98.1, repaired: 26.8, suppressed: 60.3, executed: 3.0, other: 9.9 },
];

// Reasoning trajectories, none -> low -> med -> high (reasoning_plot_data.csv).
export const reasoning = [
  { label: 'Claude Sonnet 4.6', path: [[81.8, 68.8], [79.3, 63.5], [82.4, 68.3], [86.0, 69.7]] },
  { label: 'Claude Opus 4.6', path: [[85.2, 67.7], [82.4, 62.8], [85.4, 66.6], [87.8, 69.3]] },
  { label: 'Gemini 3.1 Flash-Lite', path: [[54.5, 89.9], [53.4, 91.0], [54.8, 92.2], [67.6, 88.7]] },
  { label: 'Gemini 3 Flash', path: [[63.4, 90.4], [82.3, 92.1], [85.4, 88.7], [87.3, 88.0]] },
  { label: 'GPT-5.4 Nano', path: [[72.9, 87.8], [84.2, 84.3], [85.9, 83.9], [86.5, 84.6]] },
  { label: 'GPT-5.4 Mini', path: [[61.6, 89.9], [70.8, 88.8], [73.5, 88.1], [75.1, 87.2]] },
  { label: 'GPT-5.4', path: [[74.0, 83.2], [85.0, 86.0], [89.9, 85.0], [91.4, 83.8]] },
];

export const reasoningAverage = {
  label: 'Seven-model average',
  path: [[70.5, 82.5], [76.8, 81.2], [79.6, 81.8], [83.1, 81.6]],
};

// Fidelity-aware DPO on the held-out editing task, n = 273
// (fidelity_dpo_results.csv, edit_heldout split).
export const dpo = [
  { label: 'Llama 3.1 8B (base)', processed: 40.3, ignored: 16.1, executed: 55.3 },
  { label: '+ Defensive tokens', processed: 28.9, ignored: 65.6, executed: 1.1 },
  { label: '+ SecAlign', processed: 43.2, ignored: 53.5, executed: 1.1 },
  { label: '+ Fidelity-aware DPO', processed: 80.6, ignored: 16.8, executed: 0.7 },
];
