# Compound Poisson (improved)

Claim arrival process from the insurance problem in [mirkovicdev/stokmod](https://github.com/mirkovicdev/stokmod).

**New:** Monte Carlo aggregate loss stats + classical ruin probability estimator.

```python
from compound_poisson import simulate_claim_process, ruin_probability_mc
print(simulate_claim_process(1.5, 59))
print(ruin_probability_mc(u0=10, premium_rate=2, lambda_rate=1.5, T=30))
```

MIT.
