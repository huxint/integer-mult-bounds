# Source-assisted entrance-bank checkpoint

The complete verifier reconstructs the pinned PR193 complex supplier, replays
the globally emitted PR187 bit word, applies PR186's completed entrance banks,
and certifies the conditional exponent saving

    kappa = 675649470782647 / 10^18 = 0.000675649470782647.

This is a reproducible research checkpoint, not a record claim. Concurrent
[PR197](https://github.com/CrocSwap/integer-mult-bounds/pull/197) uses a related
packing construction and a stronger finite leaf, and reports a higher value.
The present package keeps the original leaf and adapter toll unchanged.

From this repository checkout, with Python 3.13 or newer:

```sh
python3.13 -m venv .venv-banks
.venv-banks/bin/python -m pip install -r research/source-assisted/requirements-round13.txt
.venv-banks/bin/python -u -B research/source-assisted-entrance-banks/verify.py
```

The full check takes about three minutes. It requires no network after the
dependencies are installed. `--write` is the author command for regenerating
`SOURCE.json`, `certificate.json` and `RESULTS.md`; ordinary verification checks
their exact contents. Run without `-O` and without concurrent use of PR193's
`research/source-assisted-v4/.work` directory. Python 3.13+ is required because
the unchanged PR193 receipts pin its canonical gzip header.

`references/pr187-package` and the twelve `pr187-overlay` files reconstruct the
exact original PR187 source tree in temporary storage. Its source hashes and
full verifier are retained unchanged. No root-level copy of PR187's package is
needed. The bank proof, literal nine-copy accounting and limitations are in
[PROOF.md](PROOF.md); exact outcomes are in [RESULTS.md](RESULTS.md).

The result retains the inherited all-size compiler, routing, weighted-chart,
precision and analytic assumptions. In particular, the complex prerequisite
checks local exact flow lifts and contracts; it does not supply a globally
renumbered complex scalar transcript or a full Clifford/router replay.
