
import math
from scipy.stats import norm

def compute_greeks(S, K, T, r, sigma, option_type):
    try:
        d1 = (math.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type == "CE":
            delta = norm.cdf(d1)
            theta = -((S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))) - r * K * math.exp(-r * T) * norm.cdf(d2)
        else:
            delta = -norm.cdf(-d1)
            theta = -((S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))) + r * K * math.exp(-r * T) * norm.cdf(-d2)

        gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
        vega = S * norm.pdf(d1) * math.sqrt(T)

        return {
            "delta": round(delta, 4),
            "gamma": round(gamma, 4),
            "vega": round(vega, 4),
            "theta": round(theta / 365, 4),  # per day
            "iv": round(sigma, 4)
        }
    except Exception as e:
        return {
            "delta": 0.0,
            "gamma": 0.0,
            "vega": 0.0,
            "theta": 0.0,
            "iv": sigma
        }
