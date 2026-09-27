import { $, bars, fail, int, kpis, load, num, seg, table } from './kit.js';

const signed = (v, d = 2) => `${v > 0 ? '+' : v < 0 ? '−' : ''}${Math.abs(v).toFixed(d)}`;
try {
  const { summary, detail, outputs_per_model: perModel } = await load();
  const C = summary.criteria, names = Object.keys(C);
  const atCeiling = names.filter((c) => Math.min(C[c].agreement.kappa.judge_mturk, C[c].agreement.kappa.judge_scale) >= C[c].agreement.kappa.mturk_scale - 0.02);
  const sp = names.filter((c) => C[c].self_preference.interval[0] > 0);
  kpis($('#kpis'), [
    { label: 'Outputs, each rated three ways', value: int(summary.outputs), note: 'GPT-4 judge, MTurk pool, Scale pool' },
    { label: 'Judge as close as people get', value: `${atCeiling.length} of ${names.length}`, note: 'criteria where the judge agrees with both pools as well as they agree with each other (within 0.02)' },
    { label: 'Self-preference found', value: `${sp.length} of ${names.length}`, note: sp.length ? `${sp.join(', ')}; up to ${signed(Math.max(...sp.map((c) => C[c].self_preference.effect)))} on a 1–5 scale` : 'no interval leaves out zero' },
    { label: 'Quantile map on Helpfulness', value: `${num(C.Helpfulness.calibration.raw.kappa, 2)} → ${num(C.Helpfulness.calibration.quantile.kappa, 2)}`, note: 'kappa against the unseen human pool' },
  ]);

  let crit = 'Helpfulness', pool = 'mturk';
  function draw() {
    const a = C[crit].agreement, other = pool === 'mturk' ? 'scale' : 'mturk', label = { mturk: 'MTurk', scale: 'Scale' };
    $('#agree').innerHTML = `<div>Judge vs ${label[pool]}<b>${num(a.kappa[`judge_${pool}`], 2)}</b><span class="muted small">kappa</span></div>` +
      `<div>MTurk vs Scale<b>${num(a.kappa.mturk_scale, 2)}</b><span class="muted small">the human ceiling</span></div>` +
      `<div>Mean score<b>${num(a.mean.judge, 2)} / ${num(a.mean[pool], 2)}</b><span class="muted small">judge / ${label[pool]} (${label[other]}: ${num(a.mean[other], 2)})</span></div>`;
    const cells = detail[crit].grid[pool], cols = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], max = Math.max(...cells.map((x) => x[2]));
    const get = (j, h) => (cells.find((x) => x[0] === j && x[1] === h) || [0, 0, 0])[2];
    $('#heat').innerHTML = `<div class="scroll"><table class="heat"><thead><tr><th>Judge ↓ · ${label[pool]} →</th>${cols.map((h) => `<th class="num">${h}</th>`).join('')}</tr></thead><tbody>` +
      [5, 4, 3, 2, 1].map((j) => `<tr><th>${j}</th>${cols.map((h) => { const n = get(j, h); return `<td class="num" style="background:color-mix(in srgb, var(--accent) ${n ? Math.round(8 + (82 * n) / max) : 0}%, transparent)${Math.abs(j - h) < 0.01 ? ';outline:1px solid var(--text);outline-offset:-1px' : ''}" title="judge ${j}, ${label[pool]} ${h}: ${n}">${n || ''}</td>`; }).join('')}</tr>`).join('') +
      '</tbody></table></div><p class="small muted">Outlined: the same score from both.</p>';
    const m = detail[crit].models;
    $('#famSub').textContent = `${crit}: GPT-4 as the judge, and each human pool. Outputs per model: ${Object.entries(perModel).map(([k, v]) => `${k} ${v}`).join(', ')}.`;
    table($('#fam'), [
      { key: 'model', label: 'Model' },
      { key: 'gpt4', label: 'Judge', num: true, fmt: (v) => num(v, 2) },
      { key: 'mturk', label: 'MTurk', num: true, fmt: (v) => num(v, 2) },
      { key: 'scale', label: 'Scale', num: true, fmt: (v) => num(v, 2) },
      { key: 'gap', label: 'Judge − people', num: true, fmt: (v) => signed(v) },
    ], Object.entries(m).map(([model, x]) => ({ model, ...x, gap: x.gpt4 - (x.mturk + x.scale) / 2 })));
    const cal = C[crit].calibration, names2 = { raw: 'raw judge', quantile: 'quantile map', isotonic: 'isotonic', 'isotonic+length+family': 'isotonic + features' };
    const best = Object.keys(cal).reduce((x, y) => (cal[y].kappa > cal[x].kappa ? y : x));
    bars($('#cal'), Object.entries(cal).map(([k, v]) => ({ label: names2[k] || k, value: Math.max(0, v.kappa), text: `${num(v.kappa, 2)} (${num(v.mae, 2)})`, color: k === best ? 'var(--accent)' : 'var(--c6)' })), { max: 0.7 });
  }
  seg($('#crit'), names, crit, (v) => { crit = v; draw(); });
  seg($('#pool'), [['mturk', 'MTurk'], ['scale', 'Scale']], pool, (v) => { pool = v; draw(); });

  table($('#bias'), [
    { key: 'c', label: 'Criterion' },
    { key: 'lj', label: 'Length: judge', num: true, fmt: (v) => signed(v) },
    { key: 'lh', label: 'Length: humans', num: true, fmt: (v) => signed(v) },
    { key: 'fe', label: "Judge's family effect", num: true, fmt: (v) => signed(v) },
    { key: 'sp', label: 'Self-preference', num: true, fmt: (v) => signed(v) },
    { key: 'ci', label: '95% interval', num: true, fmt: (v) => `${signed(v[0])} to ${signed(v[1])}` },
  ], names.map((c) => ({ c, lj: C[c].length_bias.judge, lh: C[c].length_bias.humans, fe: C[c].self_preference.judge_family_effect, sp: C[c].self_preference.effect, ci: C[c].self_preference.interval })),
  { cls: (r) => (r.ci[0] > 0 || r.ci[1] < 0 ? 'bad' : '') });
} catch (err) {
  fail(err);
}
