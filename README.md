# One-shot zero-error communication with normal entanglement is Σ⁰₂-complete

Seth Douglas and Nidhal Mghirbi. Version 1.0.0, 3 November 2026.

**This is a preprint. It has not been peer reviewed.**

## Abstract

Can a finite classical channel require an infinite entangled resource to send a fixed number of messages without error? We classify the one-use feasibility problem for rational channels. With an arbitrary normal spatial resource it is Σ⁰₂-complete. The same classification holds when the resource must have finite marginal entropy. A separate channel admits a normal zero-error code, while every normal code achieving its specified message count has infinite marginal entropy on both sides.

The proof extends Mančinska's finite-dimensional game-to-channel correspondence to trace-class operators. For the game's channel, a normal code attaining the clique bound (one message per local question) corresponds to perfect play with summable Schmidt amplitudes. Four successive constraints, each doubling a ratio of Schmidt weights, are critical and exclude such a code; five suffice for both reductions. As a corollary of Mančinska's finite-dimensional correspondence and MIP*=RE, we obtain Σ⁰₁-completeness for finite-dimensional resources. We also prove Π⁰₁-completeness for commuting operators. Our capacity statements are upper computability bounds; the hardness results concern one use.

## Contents and reproduction

- `paper/main.pdf`: manuscript.
- `paper/`: LaTeX source, bibliography, plain-text abstract, source manifest, source archive and strict build driver.
- `verification/`: four finite checks, recorded outputs, bibliographic provenance and portability checks.
- `verification/SHA256SUMS`: SHA-256 hashes for public archive members except the checksum file itself. The containing archive is recorded in the release report, avoiding a recursive self-hash.

From the extracted source-bundle root:

1. Check the shipped hashes before rebuilding or running checks:
   `python verification/check_hashes.py`.
2. Install Python 3.10+ and `python -m pip install -r verification/requirements.txt`.
3. Run `python verification/run_all.py`. Each invocation uses a fresh output
   directory and exits nonzero on failure. Recorded results are in
   `verification/results/`.
4. Install pdfLaTeX and BibTeX (TeX Live or MiKTeX), then run
   `python paper/build.py`. The default uses a fresh temporary directory.
   An empty destination can be selected with `--output-directory PATH`.

The shipped manuscript is `paper/main.pdf`. Rebuilding preserves this file.
The build fixes SOURCE_DATE_EPOCH and FORCE_SOURCE_DATE and omits variable PDF
metadata. It rejects final LaTeX/BibTeX warnings, undefined references and
overfull/underfull diagnostics. Initial cross-reference bootstrap passes can
contain transient undefined-reference diagnostics; final logs must be clean.

The finite matrix programs check the known game-to-channel correspondence,
including a negative control. `exact_constants.py` checks bridge constants,
trace sums and entropy formulas symbolically. These finite checks support
the written proofs; they do not establish infinite-dimensional existence or
arithmetical hardness by sampling. `verification/attribution/` contains bibliographic
search records and is not required for the finite mathematical checks.

The source manifest lists source-file SHA-256 hashes and bibliographic
provenance by DOI or arXiv identifier. `verification/SHA256SUMS` is
LF-terminated and uses paths relative to the bundle root. The manifest and
hash list do not hash themselves recursively. The archive contains neither
build logs nor downloaded third-party papers.

For a fresh-extraction check run `python verification/verify_portable.py`.
It checks hashes, reruns all finite checks, builds in a fresh directory, and
checks again that the shipped hashes are unchanged.

## Citation and rights

See `CITATION.cff` for citation metadata.
Paper and documentation: CC BY 4.0. Scripts: MIT or Apache 2.0, at your option. See `RIGHTS.md`, the license files and `NOTICE`.
