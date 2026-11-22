# news-image-20261121

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/bongekanjing/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/bongekanjing/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A square one-page newspaper (1024x1024) summing up the world's news
of **Saturday 21 November 2026** — 35 stories, 7 regions, every story
with a clear illustration. Twelve breaking stories from **Sunday 22
November** are woven into the page as ordinary stories, not a separate
section.

The three leads: Mexico captures the FBI most-wanted cartel boss "El
Chapo Isidro" in Sinaloa; the AI sell-off sinks markets (S&P 500
−3.7%, Nikkei −5.06%) while Anthropic debuts at a $2T market cap, the
biggest ever; and COP31 runs past its deadline in Antalya with no deal
on fossil fuels. Also on the page: the Trump–Xi–Putin peace
declaration in Shenzhen, the world court finding Myanmar guilty of
genocide against the Rohingya, Russian missiles landing in Poland,
Denmark backing the US Greenland deal 109–0, Ukraine hitting the Kerch
Bridge a third time, Iran striking a US base in Kuwait, a magnitude 6.9
quake in Peru's Andes, Estonia closing its border with Russia, and a
"where it happened" map plus a date check.

## How it works

The page was composed as HTML/CSS in `news-20261121.html` (shipped in
this repo) and rendered to `entry.png` with a headless browser, so
every headline, number and illustration sits exactly as designed.
`main.py` does not redraw the page: it copies the rendered `entry.png`
to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`) and
exits 0. Pure standard library, no network, no randomness — two runs
produce byte-identical output.

Run it locally:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
