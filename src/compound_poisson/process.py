"""Poisson arrivals + independent claim sizes."""

from __future__ import annotations

from typing import Optional

import numpy as np


def simulate_claim_process(
    lambda_rate: float,
    T: float,
    claim_dist: str = "exp",
    claim_param: float = 10.0,
    rng: Optional[np.random.Generator] = None,
) -> dict:
    rng = rng or np.random.default_rng()
    n = rng.poisson(lambda_rate * T)
    times = np.sort(rng.uniform(0, T, size=n))
    if claim_dist == "exp":
        sizes = rng.exponential(1.0 / claim_param, size=n)
    elif claim_dist == "fixed":
        sizes = np.full(n, claim_param, dtype=float)
    else:
        raise ValueError("claim_dist must be 'exp' or 'fixed'")
    cumulative = np.cumsum(sizes) if n else np.array([])
    return {
        "n_claims": int(n),
        "times": times,
        "sizes": sizes,
        "aggregate": float(sizes.sum()) if n else 0.0,
        "cumulative": cumulative,
        "T": T,
        "lambda": lambda_rate,
    }


def aggregate_loss_stats(
    lambda_rate: float,
    T: float,
    claim_dist: str = "exp",
    claim_param: float = 10.0,
    n_sims: int = 1000,
    seed: int = 0,
) -> dict:
    rng = np.random.default_rng(seed)
    totals = np.array(
        [
            simulate_claim_process(lambda_rate, T, claim_dist, claim_param, rng)["aggregate"]
            for _ in range(n_sims)
        ]
    )
    return {
        "mean": float(totals.mean()),
        "var": float(totals.var()),
        "p95": float(np.percentile(totals, 95)),
        "n_sims": n_sims,
    }


def ruin_probability_mc(
    u0: float,
    premium_rate: float,
    lambda_rate: float,
    T: float,
    claim_param: float = 10.0,
    n_sims: int = 2000,
    seed: int = 0,
) -> float:
    rng = np.random.default_rng(seed)
    ruin = 0
    for _ in range(n_sims):
        path = simulate_claim_process(lambda_rate, T, "exp", claim_param, rng)
        if path["n_claims"] == 0:
            continue
        capital = u0 + premium_rate * path["times"] - path["cumulative"]
        if np.any(capital < 0):
            ruin += 1
    return ruin / n_sims
