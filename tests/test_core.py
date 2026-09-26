from compound_poisson import simulate_claim_process, aggregate_loss_stats, ruin_probability_mc

def test_sim():
    p = simulate_claim_process(1.5, 59, claim_param=10.0)
    assert p["aggregate"] >= 0
    assert len(p["times"]) == p["n_claims"]

def test_stats():
    s = aggregate_loss_stats(1.5, 10, n_sims=200, seed=0)
    assert s["mean"] > 0

def test_ruin():
    p = ruin_probability_mc(u0=5.0, premium_rate=2.0, lambda_rate=1.5, T=20, n_sims=300, seed=0)
    assert 0 <= p <= 1
