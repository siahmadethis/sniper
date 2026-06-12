# Sniper — VIX / (10Y2Y Spread + 2.5) display

A single-page display for the market stress ratio:

```
        VIX
─────────────────────
 10Y2Y Spread + 2.5
```

- **VIX** — CBOE Volatility Index daily close (FRED series `VIXCLS`)
- **10Y2Y Spread** — 10-year minus 2-year Treasury constant-maturity yield,
  in percentage points (FRED series `T10Y2Y`)
- **+ 2.5** — offset that keeps the denominator positive through historical
  curve inversions

The ratio rises when volatility spikes and/or the yield curve flattens or
inverts, so higher readings indicate more market stress. With a calm market
(VIX ≈ 15, spread ≈ +0.5) the ratio sits near 5.

## Running it

```sh
python3 server.py          # serves on http://localhost:8000
```

Then open <http://localhost:8000>.

You can also open `index.html` directly in a browser — the page fetches FRED
data itself when possible. The server is only needed as a CORS/firewall
fallback (it proxies FRED's CSV endpoint at `/api/fred`). If no data source
is reachable at all, the page offers manual VIX/spread inputs.

## Features

- The formula rendered with live values substituted in
- Large color-coded readout with a Calm / Moderate / Elevated / Extreme zone
  label (thresholds at 6, 10, and 20 — illustrative only)
- Component cards for VIX, the spread, and the computed denominator
- Trailing 1-year chart of the ratio with hover inspection
- Refresh button and manual-input fallback

No build step, no dependencies — plain HTML/CSS/JS plus a stdlib-only
Python server.
