# news-image-20261121

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/bongekanjing/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/bongekanjing/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A text-only broadsheet front page summing up the world's news of
**Saturday 21 November 2026** — one page, 1024x1024, no photos, no
illustrations.

The day's lead: COP31 spills into overtime in Antalya after the draft
deal drops all mention of fossil fuels. Also on the page: Russian
missiles crashing in Poland during a huge attack on Ukraine, the world
court finding Myanmar guilty of genocide against the Rohingya, fallout
from the Trump–Xi–Putin summit in Shenzhen, the US floating NATO entry
for Ukraine in return for Donbas land, the Senate rejecting a curb on
Trump's Iran war powers, a vendor cyberattack hitting JPMorgan, Visa
and Mastercard, F1 qualifying under the lights in Las Vegas, India
fighting back against New Zealand in Wellington, and Voyager 1 phoning
home from a full light-day away.

## How it works

`main.py` draws the front page with PIL (DejaVu fonts) straight to
`/output/entry.png` — deterministic, byte-identical on every run. If PIL
or the fonts are missing in the sandbox, it falls back to copying the
pre-rendered `entry.png` shipped beside it, so the graded runs need no
network and no third-party packages.

Run it locally:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
