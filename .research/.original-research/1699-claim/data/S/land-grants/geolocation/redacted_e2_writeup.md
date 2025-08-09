# Methodology Write-up – **E-2 (o3_ensemble5_redact)**

## Overview
The *E-2* condition (id `o3_ensemble5_redact`) is a privacy-aware variant of the five-call
ensemble introduced for our geolocation pipeline. The only change compared to the
winning ensemble (E-1 `o3_ensemble5`) is that, **before each model call, every patentee
name appearing at the start of the land-grant description is redacted**. This allows us to
quantify how strongly the model relies on direct name cues when geocoding colonial
Virginia land grants.

## Configuration (`methods.yaml` excerpt)
```yaml
- id: o3_ensemble5_redact     # E-2
  model: o3-2025-04-16
  pipeline: one_shot
  description: Five-call o3 ensemble with patentee names redacted
  enabled: true
  params:
    repeats: 5                  # run 5 independent LM calls
    reasoning_effort: low       # cheap implicit chain-of-thought
    service_tier: flex          # lowest latency tier
    consensus_rule: dbscan      # DB-0.5 consensus (see below)
    redact_names: true          # ***E-2 specific flag***
```

## Runtime behaviour (`run_experiment.py`)
1. **Name Redaction**  
   At the top of the main loop (≈ line 900) we copy the raw entry into
   `entry_text`.  If `params.get("redact_names")` is `True` the snippet
   ```python
   entry_text = re.sub(r"^[A-Z .:&'-]+(?=[,;])", "[NAME]", entry_text, 1)
   ```
   replaces the first comma/semicolon-terminated ALL-CAPS token sequence—i.e. the
   patentee(s)—with the placeholder `[NAME]`.

2. **Five-call Ensemble**  
   The method still issues `repeats = 5` independent *one-shot* calls to
   `o3-2025-04-16` using identical prompts (& redacted input).  Per-call usage
   and latency are aggregated.

3. **Consensus   (DB-0.5)**  
   After all calls finish, `ensemble_consensus()` is invoked with
   `consensus_rule == "dbscan"`.
   *   `find_clusters()` groups predictions that fall within 0.5 km.  
   *   The largest cluster containing ≥3 members is chosen.  
   *   Its spherical centroid (`compute_centroid`) becomes the final prediction.  
   *   Fallbacks: centroid of all points ➔ empty string.

4. **Token & Cost Accounting**  
   The total tokens and price are the *sum* of the five sub-calls.  Redaction
   itself is client-side and free.

## Motivation
Early experiments suggested that models occasionally memorise patentee ↔ county
associations seen in the few-shot examples. By erasing the names we can:
* Detect over-reliance on name cues (drop in accuracy → high leakage).
* Provide a privacy-preserving variant suitable for public release.

## Expected Impact
If the model truly infers location from the *descriptive* portion (e.g.
"on the North Fork of the Blackwater River in Isle of Wight Co."), performance
should remain close to E-1.  A large degradation would indicate name leakage
and motivate stronger prompt engineering.

---
*Document generated automatically by the assistant on 2025-06-20.* 