"""Compound Poisson risk process."""

from .process import simulate_claim_process, aggregate_loss_stats, ruin_probability_mc

__version__ = "0.2.0"
__all__ = ["simulate_claim_process", "aggregate_loss_stats", "ruin_probability_mc"]
