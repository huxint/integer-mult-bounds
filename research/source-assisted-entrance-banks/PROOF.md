# Composition and verification scope

The pinned complex supplier is PR193 at
`187e1010ac8b259af8e9b5166f68b64bc27b4b47`. Its unchanged verifier reconstructs
the source-assisted word, exact local rational lifts and contract ledger. Its
saving is `219037/312500000`. No complex flow, word, pairing or bridge is changed.

The pinned bit supplier is PR187 at
`201737a1ec4f936e166e2481fb9e88104cb2ccc7`. Its unchanged full verifier reconstructs
the actual emitted word and checks all F2 source, target and arbitrary dirty
columns, the full inverse, every used prime frame, and integer inverse and
coefficient bounds. This is not an integer decoder identity claim. The emitted
word digest is
`3c188c2527b3b96443e241f2f0d07c120feb1e784c2ff7f49c3e1e10eaea5f0b`.

## Why the existing bank construction applies

The word has 19,348 logical auxiliary roles, with 1,760 disjoint compensated
donor/recipient splices, hence 17,588 physical streams. The recipients' rank-21
gauges are internal reads in those streams. They are not physical entrances.
The remaining 2,200 gauges are rank-20 entrances; 15,388 streams are undeferred.

`banks.certify` reconstructs the inherited high suffix independently. All 23,840
high operations agree, in order and under the actual `old_to_new` role map. All
gauge frames and targets agree. New original-X controls act only on low,
undeferred streams. Thus the entrance and completed-core contracts used in
PR186's bank construction are the same contracts on these actual streams.
The common weighted charts and orbit routing remain inherited assumptions.

For a projector P over any commutative ring, put

    S_P(x,y) = (x - Px + Py, y - Py + Px).

For disjoint projectors P and Q, direct expansion gives
`S_P S_Q = S_(P+Q)`; also `S_P^2 = I`. A disjoint projector partition of the
identity therefore gives the full swap on every incoming pair, with no
cleanliness assumption. Conjugation by the same invertible weighted chart
telescopes. This is PR186's retained completed-bank identity, not a new lemma
claimed by this package.

The coordinate partitions here are eighteen width-4 blocks and three width-24
blocks of a width-72 bank. The verifier checks disjointness, idempotence and
exhaustion, all 144 columns of the two-bank endpoint and its inverse over F2
and Z, and omission and repetition controls in both rings.

## Literal allocation and complete rank bill

Nine physical replicas make each of three stage-private bank families integral.
Per stage there are `9*2200/18 = 1100` selected banks and
`9*15388/3 = 46164` undeferred banks. Each stream in each replica and stage is
assigned exactly once; the complete ordered assignment has a pinned digest.
Including the source and target stock gives

    literal W = 3*(1100 + 46164) + 2*9*1760 = 173472,
    normalized W = 173472/9 = 57824/3.

Exactly one width-60 exterior per independent entrance disappears. Every
remaining child is charged, including internal aliases, original data
endpoints, copied centers and all source and target transitions:

    rank = 1517840 - 2200*60 = 1385840,
    72*W - rank = 1936,   maximum child = 22.

Three is the arithmetic scale clearing the normalized fractions; nine is the
physical replica count. They are not interchangeable.

## Paid moment and assembly

Two independent rational log/exp engines verify the full paid moment with bad
fraction `10^-16` and `32*72^2` fallback children per edge. They accept the coarse
saving `676537710350481/10^18` and reject its adjacent `10^-18` grid point.
The original ordinary leaf `384599/10^10` and a strictly positive atom/row toll
are retained. No finite-leaf bootstrap is used.

The verifier audits the literal replicas against the retained PR193 finite
envelope: full group stock, scalar and coefficient bounds, router `G=2^30000`,
semantic reserve `E=2^100000`, common precision `C0=2^210000`, and restored-row
coefficient 20161 with degree 1000000. It then checks all 47 strict assembly
constraints and seven margins, and rejects the next final `10^-18` grid point.
The bit branch binds at the stated conditional kappa.

These finite checks do not discharge the inherited uniform weighted compiler,
Clifford/shared-core transfer, stage routing, local-ring precision and recovery,
prime-supply, restored-row, all-size analytic or fixed-tape interfaces. The
complex branch retains PR193's local-flow scope. No unconditional integer
multiplication theorem or global optimum is asserted.
