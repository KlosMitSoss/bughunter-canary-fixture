# Bughunter synthetic canary fixture

This repository is a deliberately small, self-owned test target for Bughunter
development canaries. It is **not** a deployed service, bridge, wallet, or
bug-bounty target. The balances are integers in memory; no funds, keys, network
endpoints, or third-party systems are involved.

`PayoutQueue` accepts a payout callback supplied by its caller. A callback may
run arbitrary Python before returning, including calling the queue again. The
intended invariant is that each withdrawal ticket can cause at most one payout
and that reserved and available balances remain nonnegative. The included
tests cover ordinary use; security-focused canaries may add their own local
behavioral tests and matched controls.

Run the existing tests with Python 3.11 or newer:

```sh
python -m unittest discover -s tests -v
```

Do not use this fixture to make a claim about a real program or production
deployment.
