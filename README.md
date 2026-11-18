# Running SWAP-SSS-MF6 at national scale: multi-year comparison, 2015–2018

Slides for DSD 2026: SWAP-SSS-MF6 run on the Netherlands Hydrological Model (LHM) next to MetaSWAP-MF6, 2015–2018.
Mateusz Zawadzki, Robert Leander, Hendrik Kok, Ab Veldhuizen, Marius Heinen, Timo Kroon.

**Slides:** <https://swap-model.github.io/dsd26-swap-sss-metaswap/>, published from `main` by
`.github/workflows/pages.yml`.

## Running order

| # | slide | notes |
|---|---|---|
| 1 | Title | |
| 2–3 | Why move towards a SWAP-based framework? · Sequential Steady State (SSS): the idea | Ab Veldhuizen's introduction (his slides of 2026-11-17, text as written) |
| 4 | Project milestones | four milestones, one per click |
| 5 | System schematics | repositories and the VM |
| 6 | Model comparison set-up | what is the same in both, then the table of differences |
| 7 | Run time and resources | machine, table, conclusion |
| 8 | From the LHM to your own simulation | the case files of De Raam 2018 |
| 9–10 | Running in the VM · Variables used in the comparison | |
| 11 | Daily heads, 2015–2018 | animated map, press play |
| 12 | Head difference over all columns | by groundwater depth |
| 13 | Comparison exercise: implausible values | three checks on the heads, both models |
| 14 | Conclusions | two statements, one per click |
| 15 | Next phase: SWAP-SSS as the LHM default | two groups, one item per click; earlier items blur, the last click clears them |
| 16 | Thank you | the title slide's layout |

## Figures

The figures in `figures/` are Plotly fragments written by notebooks of `swap-sss-runs` (`~/code/swap-sss-runs`,
on top of commit `78520b2`), copied here on 2026-11-18. Runs: `nl1518_sss_l4l` r01 and `nl1518_msw_l4l` r01 (LHM,
2015–2018, like-for-like switches); daily heads from SWAP-SSS `gwl` and MetaSWAP `Hgwmodf`, from
`workflow/compare_runs.py`.

| file | slide | notebook (in `swap-sss-runs/analysis/`) |
|---|---|---|
| `nl1518_heads_animation.md` | 11 | `04-2026-11-12-mz-heads-animation.py` (every third day on the map; carries plotly.js for the slides after it) |
| `nl1518_head_diff_bands.md` | 12 | `04-2026-11-13-mz-head-diff-bands.py` |
| `nl1518_implausible_summary.md` | 13 | `04-2026-11-13-mz-implausible-values.py` (2016–2018; 2015 is the warm-up year); the notebook writes six checks, the deck keeps the first three (storage-coefficient, ET and storage-change rows removed by hand) |

To update a figure: rerun its notebook there (`RUNS=nl1518`, the default) and copy the `.md` from
`output/figures/` into `figures/`.

## Render and preview

```bash
pixi run render      # _site/index.html, one self-contained file, as the Pages workflow does
pixi run preview     # live reload at http://localhost:4303/index.html (forward the port over ssh)
```

The theme is `soil-column.scss` (on top of `custom.scss`); the title slide uses `partials/title-slide.html` for the
logo row. Diagrams are Graphviz cells rendered by Quarto.
