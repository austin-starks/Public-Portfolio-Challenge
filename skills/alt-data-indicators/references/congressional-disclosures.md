# Congressional disclosures (House Clerk PTR pipeline)

Congressional Periodic Transaction Reports (PTRs) — a candidate alt-data source. **Coverage first:**
a single politician covers ~1 of 21 names, so only an **all-Congress aggregate** can reach rank-grade
coverage. Otherwise it is a tilt/overlay only (sparse-series rule).

## Where the data lives (NOT sec_edgar)
`sec_edgar` is **corporate filings only** (10-K / 10-Q / 8-K, and Form 4 via `forms:["4"]`).
Congressional PTRs live at the **House Clerk**:
- Year index: `…/financial-pdfs/{YEAR}FD.zip` — a TSV index. Filter rows where `FilingType = "P"`
  (periodic transaction report) and read the `DocID`.
- The PDF: `…/ptr-pdfs/{YEAR}/{DocID}.pdf`.

## Pipeline (in a compute session)
1. Fetch the House Clerk year indexes for the years in scope.
2. Filter `FilingType = "P"`; collect `DocID`s.
3. Fetch each PTR PDF and text-extract it. **Count scanned-image PDFs you had to skip, honestly** —
   image-only filings can't be parsed and their omission is a coverage caveat.
4. Parse purchase rows for the 21 tickers; take the midpoint of each disclosed dollar range.
5. **Stamp every point at the FILING date, not the transaction date** — the STOCK Act lag is up to
   ~45 days, and the filing date is when the information became public (lookahead guarantee).

## Two shapes to build
- **(a)** buy-dollars per `{filing date, ticker}`.
- **(b)** recent-buys rolling window (e.g. trailing-6-month disclosed buys per ticker).

## Coverage verdict
If per-ticker coverage still comes back sparse across the 21 names, it is a **tilt/overlay candidate
only** — a rank built on it will trade ZERO. Say so and deprioritize. (A dollar-buys series covering
only ~1/21 names, e.g. one name like AVGO, is overlay-only.)
