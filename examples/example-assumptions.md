# ASSUMPTIONS: SciProof

> Companion to [example-dna.md](example-dna.md). Everything here is a **hypothesis** — something we believe but could discover to be wrong. Invariants live in `DNA.md` and change only through formal mutation; these change as they get tested. That's normal work, not a crisis.

**Last updated:** 2026-08-18

---

## How to read this file

| Field | Meaning |
|-------|---------|
| **Statement** | What we currently believe |
| **Consequence** | What in the project depends on this being true |
| **How to check** | The concrete test that would settle it |
| **Status** | `VERIFIED` / `UNVERIFIED` / `FAILED` |

The test that puts something here rather than in DNA: **what would have to happen for this to stop being true?** If the answer is "nothing, it's a property of the domain" — it belongs in DNA. If it's "we might discover we were wrong" — it belongs here.

---

## A-01. OCR quality for Russian geological texts

**Statement:** Available OCR reaches ≥95% character accuracy on typical Soviet-era geological reports without domain-specific training.

**Consequence:** The extraction pipeline assumes it can work directly from OCR output. If accuracy is materially lower, a correction stage becomes mandatory and the per-document cost estimate roughly doubles.

**How to check:** Run OCR on 20 pages sampled across three publication decades; compare against manual transcription.

**Status:** `FAILED` — measured 87% on 1960s-1970s typewritten reports with hand-drawn diagrams. Modern offset-printed publications reach 97%. Correction stage added to the pipeline for pre-1985 sources.

---

## A-02. Corpus size

**Statement:** The working corpus stays within 10²–10⁴ publications for the foreseeable project lifetime.

**Consequence:** DNA §5.2 (scale) and the entire storage/indexing approach. If the corpus grows two orders of magnitude, the "deep analysis over broad indexing" economic model needs revisiting — which is a DNA mutation, not a tuning exercise.

**How to check:** Track corpus growth quarterly against the projection.

**Status:** `UNVERIFIED` — currently 340 publications after 9 months. Growth rate consistent with the assumption, but the observation window is short.

---

## A-03. Reviewer throughput

**Statement:** A domain expert can review extracted facts at roughly 2 seconds per grain measurement when the interface is responsive.

**Consequence:** The review UI performance budget (DNA §4.2, responsiveness dilemma) is calibrated against this figure. If real throughput is much slower, the bottleneck is expert attention rather than interface latency, and optimizing the UI is wasted effort.

**How to check:** Instrument the review interface; measure actual per-item time across five reviewers over a full session.

**Status:** `VERIFIED` — median 1.8 sec/item across 5 reviewers, 2,400 items. Tail is heavy (95th percentile 6.2 sec) on items with ambiguous provenance, which is expected.

---

## A-04. Terminology mapping between schools

**Statement:** Russian and Western geomorphological terminology can be mapped with a curated correspondence table of manageable size (< 500 term pairs).

**Consequence:** The Term ≠ Concept distinction (DNA §2.2) is implementable as a lookup rather than requiring contextual inference per occurrence. A much larger or fundamentally ambiguous mapping would push this toward a model-based approach.

**How to check:** Build the table for one subdomain (aeolian deposits); measure coverage against a held-out set of publications.

**Status:** `UNVERIFIED` — table at 180 pairs covering aeolian deposits, coverage not yet measured on held-out data.

---

## A-05. Coordinate system metadata availability

**Statement:** Most publications state their coordinate reference system explicitly, or it can be inferred from publication date and institution.

**Consequence:** Automated transformation to modern coordinate systems is feasible. If CRS is frequently absent and uninferable, spatial features become manual-entry only.

**How to check:** Sample 50 publications across decades; record how many state CRS explicitly, how many are inferable, how many are ambiguous.

**Status:** `UNVERIFIED` — not yet sampled. Flagged as the highest-risk open assumption for the spatial features roadmap.

---

## Retired assumptions

Kept for the record — these were resolved and no longer constrain decisions.

| ID | Statement | Outcome |
|----|-----------|---------|
| A-00 | Publication PDFs are mostly text-layer, not scanned images | `FAILED` — 70% are scanned. Drove the OCR pipeline decision entirely. |
