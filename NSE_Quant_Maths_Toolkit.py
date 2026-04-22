"""
╔══════════════════════════════════════════════════════════════════╗
║         NSE QUANT MATHEMATICS TOOLKIT                          ║
║         Risk & Return Analytics for Indian Markets             ║
╠══════════════════════════════════════════════════════════════════╣
║  Author  : Shivam Tyagi                                       ║
║  GitHub  : github.com/QuantShivam                              ║
║  Date    : March 2026                                          ║
║  Module  : Mathematics Foundation (11 Topics)                  ║
╚══════════════════════════════════════════════════════════════════╝

Every calculation a quant trader needs — built from scratch using
only NumPy. No black-box libraries. Every formula is visible,
every number is verified by hand first.

Topics Covered:
  1.  Percentages & Returns
  2.  Mean (Simple & Weighted)
  3.  Standard Deviation & Variance
  4.  Normal Distribution & Probability Zones
  5.  Correlation Matrix
  6.  Probability Basics (Empirical)
  7.  Expected Value & Edge Detection
  8.  Compounding (Simple vs Compound Interest)
  9.  Logarithmic Returns
  10. Linear Algebra (Portfolio Weights & Dot Product)
  11. Calculus Concepts (Rate of Change & Gradient)
"""

import numpy as np
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════
#  ✏️  CUSTOMISE HERE — Edit your own stocks & prices
#  ─────────────────────────────────────────────────────────────────
#  HOW TO USE:
#  1. Replace stock names (e.g. "RELIANCE") with your own
#  2. Replace the price lists with 20 daily closing prices
#  3. You need exactly 20 prices per stock (in order, oldest first)
#  4. You can add or remove stocks — just keep the same format
#  5. Run: python NSE_Quant_Maths_Toolkit.py
# ═══════════════════════════════════════════════════════════════════

STOCKS = {
    "RELIANCE": [
        2928.10, 2935.45, 2910.20, 2955.80, 2970.15,
        2948.30, 2962.75, 2989.00, 2975.40, 2998.60,
        3012.50, 2985.20, 3001.75, 3025.40, 3018.90,
        3042.15, 3058.30, 3035.70, 3065.80, 3078.25,
    ],
    "TCS": [
        3845.00, 3872.30, 3830.15, 3898.50, 3920.75,
        3885.40, 3910.60, 3945.20, 3922.80, 3960.50,
        3978.30, 3942.15, 3965.80, 3990.40, 3975.60,
        4010.25, 4035.50, 4005.80, 4048.90, 4062.15,
    ],
    "INFY": [
        1580.25, 1595.40, 1568.80, 1610.50, 1625.30,
        1602.15, 1618.40, 1645.70, 1630.20, 1658.90,
        1672.50, 1648.30, 1665.80, 1688.40, 1675.20,
        1695.60, 1712.80, 1698.50, 1725.30, 1738.60,
    ],
    "HDFCBANK": [
        1685.50, 1690.20, 1678.40, 1698.80, 1705.30,
        1692.50, 1700.15, 1712.60, 1706.40, 1718.90,
        1725.30, 1715.80, 1722.50, 1730.40, 1726.80,
        1735.60, 1742.30, 1738.50, 1748.20, 1752.60,
    ],
    "TATASTEEL": [
        152.30, 155.80, 148.50, 160.20, 165.40,
        158.70, 162.30, 170.50, 164.80, 172.60,
        176.40, 168.90, 173.50, 179.80, 175.20,
        182.30, 188.50, 180.40, 190.20, 195.60,
    ],
}

RISK_FREE_RATE_ANNUAL = 6.5
TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE_DAILY = RISK_FREE_RATE_ANNUAL / TRADING_DAYS_PER_YEAR


# ═══════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def section(title, number):
    print(f"\n{'═' * 70}")
    print(f"  TOPIC {number} │ {title}")
    print(f"{'═' * 70}")


def subsection(title):
    print(f"\n  ── {title} {'─' * (50 - len(title))}")


def compute_simple_returns(prices):
    prices = np.array(prices)
    returns = ((prices[1:] - prices[:-1]) / prices[:-1]) * 100
    return returns


def compute_log_returns(prices):
    prices = np.array(prices)
    returns = np.log(prices[1:] / prices[:-1]) * 100
    return returns


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 1: PERCENTAGES & RETURNS
# ═══════════════════════════════════════════════════════════════════

def topic_1_returns():
    section("PERCENTAGES & RETURNS", 1)
    print("\n  Daily returns show how much a stock moved each day.")
    print("  Formula: Return = (Today - Yesterday) / Yesterday × 100\n")
    subsection("Daily Returns (Last 19 Trading Days)")
    print(f"  {'Stock':12} {'Min':>8} {'Max':>8} {'First':>8} {'Last':>8} {'Period Return':>14}")
    print(f"  {'─' * 60}")
    all_returns = {}
    for stock, prices in STOCKS.items():
        returns = compute_simple_returns(prices)
        all_returns[stock] = returns
        period_return = ((prices[-1] - prices[0]) / prices[0]) * 100
        print(f"  {stock:12} {returns.min():>+7.2f}% {returns.max():>+7.2f}% "
              f"{returns[0]:>+7.2f}% {returns[-1]:>+7.2f}% {period_return:>+13.2f}%")
    subsection("Biggest Movers")
    for stock, returns in all_returns.items():
        best_day = returns.argmax() + 1
        worst_day = returns.argmin() + 1
        print(f"  {stock:12} Best: Day {best_day:>2} ({returns.max():>+.2f}%)  "
              f"Worst: Day {worst_day:>2} ({returns.min():>+.2f}%)")
    return all_returns


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 2: MEAN (SIMPLE & WEIGHTED)
# ═══════════════════════════════════════════════════════════════════

def topic_2_mean(all_returns):
    section("MEAN RETURN (Simple & Weighted)", 2)
    print("\n  Mean return = average daily move.")
    print("  A positive mean suggests the stock trends upward.\n")
    subsection("Simple Mean — Daily Returns")
    print(f"  {'Stock':12} {'Mean Daily':>12} {'Annualized*':>14}")
    print(f"  {'─' * 42}")
    means = {}
    for stock, returns in all_returns.items():
        mean_daily = np.mean(returns)
        mean_annual = mean_daily * TRADING_DAYS_PER_YEAR
        means[stock] = mean_daily
        print(f"  {stock:12} {mean_daily:>+11.4f}% {mean_annual:>+13.2f}%")
    print(f"\n  * Annualized = Daily Mean × {TRADING_DAYS_PER_YEAR} trading days")
    subsection("Weighted Portfolio Mean")
    weights = {"RELIANCE": 0.30, "TCS": 0.25, "INFY": 0.20, "HDFCBANK": 0.15, "TATASTEEL": 0.10}
    weighted_mean = sum(weights[s] * means[s] for s in weights)
    print(f"  Portfolio Allocation:")
    for stock, weight in weights.items():
        print(f"    {stock:12} {weight * 100:>5.0f}% × {means[stock]:>+.4f}% = {weight * means[stock]:>+.4f}%")
    print(f"  {'─' * 50}")
    print(f"  {'Weighted Mean':12} {'':>18} {weighted_mean:>+.4f}% / day")
    print(f"  {'Annualized':12} {'':>18} {weighted_mean * 252:>+.2f}%")
    return means, weights


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 3: STANDARD DEVIATION & VARIANCE
# ═══════════════════════════════════════════════════════════════════

def topic_3_std_dev(all_returns, means):
    section("STANDARD DEVIATION & VARIANCE", 3)
    print("\n  Std Dev measures how wildly a stock swings.")
    print("  Higher std dev = more risk = more unpredictable.\n")
    subsection("Risk Comparison")
    print(f"  {'Stock':12} {'Mean':>9} {'Std Dev':>9} {'Variance':>10} {'Risk Level':>12}")
    print(f"  {'─' * 56}")
    stds = {}
    for stock, returns in all_returns.items():
        std = np.std(returns)
        var = np.var(returns)
        stds[stock] = std
        risk = "LOW" if std < 0.5 else ("MEDIUM" if std < 1.0 else "HIGH")
        print(f"  {stock:12} {means[stock]:>+8.4f}% {std:>8.4f}% {var:>9.4f}  {risk:>10}")
    subsection("Volatility Ranking")
    sorted_stds = sorted(stds.items(), key=lambda x: x[1], reverse=True)
    for i, (stock, std) in enumerate(sorted_stds, 1):
        bar = "█" * int(std * 20)
        label = " ← MOST VOLATILE" if i == 1 else (" ← LEAST VOLATILE" if i == len(sorted_stds) else "")
        print(f"  {i}. {stock:12} {std:.4f}% {bar}{label}")
    return stds


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 4: NORMAL DISTRIBUTION & PROBABILITY ZONES
# ═══════════════════════════════════════════════════════════════════

def topic_4_normal_distribution(all_returns, means, stds):
    section("NORMAL DISTRIBUTION & PROBABILITY ZONES", 4)
    print("\n  68% of days fall within ±1 std dev of the mean")
    print("  95% of days fall within ±2 std devs")
    print("  99.7% of days fall within ±3 std devs\n")
    subsection("Probability Zones (68-95-99.7 Rule)")
    for stock, returns in all_returns.items():
        mean = means[stock]
        std = stds[stock]
        within_1 = np.sum(np.abs(returns - mean) <= std) / len(returns) * 100
        within_2 = np.sum(np.abs(returns - mean) <= 2 * std) / len(returns) * 100
        within_3 = np.sum(np.abs(returns - mean) <= 3 * std) / len(returns) * 100
        print(f"\n  {stock}")
        print(f"    ±1σ: {mean-std:>+.2f}% to {mean+std:>+.2f}%  → {within_1:>5.1f}% of days")
        print(f"    ±2σ: {mean-2*std:>+.2f}% to {mean+2*std:>+.2f}%  → {within_2:>5.1f}% of days")
        print(f"    ±3σ: {mean-3*std:>+.2f}% to {mean+3*std:>+.2f}%  → {within_3:>5.1f}% of days")
    subsection("Outlier Detection (Beyond ±2σ)")
    found_outlier = False
    for stock, returns in all_returns.items():
        mean = means[stock]
        std = stds[stock]
        outliers = np.where(np.abs(returns - mean) > 2 * std)[0]
        if len(outliers) > 0:
            found_outlier = True
            for idx in outliers:
                print(f"  {stock:12} Day {idx+1:>2}: {returns[idx]:>+.2f}%")
    if not found_outlier:
        print("  No outliers detected beyond ±2σ in this sample.")


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 5: CORRELATION MATRIX
# ═══════════════════════════════════════════════════════════════════

def topic_5_correlation(all_returns):
    section("CORRELATION MATRIX", 5)
    print("\n  +1.0 = perfect sync | 0.0 = no relationship | -1.0 = opposite\n")
    stock_names = list(all_returns.keys())
    n = len(stock_names)
    returns_matrix = np.array([all_returns[s] for s in stock_names])
    corr_matrix = np.corrcoef(returns_matrix)
    subsection("Pairwise Correlation")
    print(f"  {'':12} " + " ".join(f"{s:>10}" for s in stock_names))
    print(f"  {'─' * (14 + 11 * n)}")
    for i, stock in enumerate(stock_names):
        row = f"  {stock:12} "
        for j in range(n):
            row += f"{corr_matrix[i][j]:>10.4f} "
        print(row)
    pairs = [(stock_names[i], stock_names[j], corr_matrix[i][j])
             for i in range(n) for j in range(i+1, n)]
    pairs_sorted = sorted(pairs, key=lambda x: x[2], reverse=True)
    subsection("Key Pairs")
    print(f"  Highest: {pairs_sorted[0][0]} ↔ {pairs_sorted[0][1]} ({pairs_sorted[0][2]:+.4f})")
    print(f"  Lowest : {pairs_sorted[-1][0]} ↔ {pairs_sorted[-1][1]} ({pairs_sorted[-1][2]:+.4f})")
    return corr_matrix


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 6: PROBABILITY BASICS
# ═══════════════════════════════════════════════════════════════════

def topic_6_probability(all_returns):
    section("PROBABILITY BASICS (Empirical)", 6)
    print("\n  Empirical probability = count outcomes / total outcomes\n")
    subsection("Win/Loss Probability per Stock")
    print(f"  {'Stock':12} {'Days':>5} {'Up':>5} {'Down':>5} {'P(Up)':>8} {'P(Down)':>8}")
    print(f"  {'─' * 50}")
    for stock, returns in all_returns.items():
        n = len(returns)
        up = np.sum(returns > 0)
        down = np.sum(returns < 0)
        print(f"  {stock:12} {n:>5} {up:>5} {down:>5} {up/n*100:>7.1f}% {down/n*100:>7.1f}%")


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 7: EXPECTED VALUE & EDGE DETECTION
# ═══════════════════════════════════════════════════════════════════

def topic_7_expected_value(all_returns):
    section("EXPECTED VALUE & EDGE DETECTION", 7)
    print("\n  EV = (Win Rate × Avg Win) - (Loss Rate × Avg Loss)")
    print("  Positive EV = you have an EDGE.\n")
    subsection("Edge Analysis")
    print(f"  {'Stock':12} {'WinRate':>8} {'AvgWin':>9} {'AvgLoss':>9} {'EV/Day':>9} {'Edge?':>8}")
    print(f"  {'─' * 60}")
    for stock, returns in all_returns.items():
        wins = returns[returns > 0]
        losses = returns[returns < 0]
        win_rate = len(wins) / len(returns)
        loss_rate = len(losses) / len(returns)
        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = abs(np.mean(losses)) if len(losses) > 0 else 0
        ev = (win_rate * avg_win) - (loss_rate * avg_loss)
        edge = "✓ YES" if ev > 0 else "✗ NO"
        print(f"  {stock:12} {win_rate*100:>7.1f}% {avg_win:>+8.3f}% "
              f"{avg_loss:>8.3f}% {ev:>+8.4f}% {edge:>8}")


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 8: COMPOUNDING
# ═══════════════════════════════════════════════════════════════════

def topic_8_compounding():
    section("COMPOUNDING — The 8th Wonder of the World", 8)
    principal = 50000
    annual_rate = 0.15
    years = [1, 3, 5, 10, 20]
    subsection(f"Growth of ₹{principal:,.0f} at {annual_rate*100:.0f}% Annual Return")
    print(f"  {'Years':>6} {'Simple':>18} {'Compound':>20} {'Difference':>14}")
    print(f"  {'─' * 62}")
    for t in years:
        simple = principal * (1 + annual_rate * t)
        compound = principal * (1 + annual_rate) ** t
        diff = compound - simple
        print(f"  {t:>4} yr  ₹{simple:>14,.2f}   ₹{compound:>16,.2f}   +₹{diff:>10,.2f}")
    subsection("Rule of 72")
    for rate in [6.5, 10, 12, 15, 20]:
        approx = 72 / rate
        exact = np.log(2) / np.log(1 + rate / 100)
        print(f"    {rate:>5.1f}% → ~{approx:.1f} years (exact: {exact:.2f} years)")


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 9: LOGARITHMIC RETURNS
# ═══════════════════════════════════════════════════════════════════

def topic_9_log_returns(all_returns):
    section("LOGARITHMIC RETURNS", 9)
    print("\n  Log Return = ln(P_today / P_yesterday) × 100")
    print("  Key advantage: time-additive (can sum across days)\n")
    subsection("Simple vs Log Returns")
    print(f"  {'Stock':12} {'Simple Mean':>13} {'Log Mean':>11} {'Difference':>12}")
    print(f"  {'─' * 52}")
    for stock, prices in STOCKS.items():
        simple_mean = np.mean(compute_simple_returns(prices))
        log_mean = np.mean(compute_log_returns(prices))
        print(f"  {stock:12} {simple_mean:>+12.5f}% {log_mean:>+10.5f}% {simple_mean-log_mean:>+11.5f}%")


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 10: LINEAR ALGEBRA
# ═══════════════════════════════════════════════════════════════════

def topic_10_linear_algebra(all_returns, means, stds):
    section("LINEAR ALGEBRA — Portfolio Mathematics", 10)
    print("\n  Portfolio return = dot product of weights and returns.\n")
    stock_names = list(all_returns.keys())
    portfolios = {
        "Equal Weight" : np.array([0.20, 0.20, 0.20, 0.20, 0.20]),
        "Tech Heavy"   : np.array([0.15, 0.30, 0.30, 0.10, 0.15]),
        "Conservative" : np.array([0.35, 0.20, 0.15, 0.25, 0.05]),
    }
    mean_vec = np.array([means[s] for s in stock_names])
    std_vec  = np.array([stds[s]  for s in stock_names])
    subsection("Portfolio Comparison")
    print(f"  {'Portfolio':16} {'Mean':>9} {'Risk':>9} {'Return/Risk':>12}")
    print(f"  {'─' * 50}")
    for name, weights in portfolios.items():
        port_return = np.dot(weights, mean_vec)
        port_risk   = np.sqrt(np.dot(weights ** 2, std_vec ** 2))
        rr_ratio    = port_return / port_risk if port_risk > 0 else 0
        print(f"  {name:16} {port_return:>+8.4f}% {port_risk:>8.4f}% {rr_ratio:>11.3f}")


# ═══════════════════════════════════════════════════════════════════
#  TOPIC 11: CALCULUS CONCEPTS
# ═══════════════════════════════════════════════════════════════════

def topic_11_calculus(all_returns):
    section("CALCULUS CONCEPTS — Rate of Change", 11)
    print("\n  Derivative ≈ rate of change ≈ momentum of the stock.\n")
    subsection("Momentum Detection")
    for stock in ["RELIANCE", "TATASTEEL"]:
        returns = all_returns[stock]
        roc = np.diff(returns)
        print(f"  {stock}")
        print(f"    Accelerating: {np.sum(roc > 0)}/{len(roc)} days")
        print(f"    Decelerating: {np.sum(roc < 0)}/{len(roc)} days")
        print(f"    Avg accel   : {np.mean(roc):>+.4f}% per day²\n")
    subsection("Cumulative Returns (Integration)")
    for stock in ["RELIANCE", "TATASTEEL"]:
        cumulative = np.cumsum(all_returns[stock])
        print(f"  {stock} → Day 1: {cumulative[0]:>+.2f}% | "
              f"Day 10: {cumulative[9]:>+.2f}% | Day 19: {cumulative[-1]:>+.2f}%")


# ═══════════════════════════════════════════════════════════════════
#  FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════

def print_final_summary(all_returns, means, stds):
    print(f"\n{'═' * 70}")
    print(f"  FINAL SUMMARY — MODULE 2 COMPLETE")
    print(f"{'═' * 70}")
    rr = {s: means[s] / stds[s] if stds[s] > 0 else 0 for s in means}
    sorted_by_rr = sorted(rr.items(), key=lambda x: x[1], reverse=True)
    print(f"\n  Best risk-adjusted stock: {sorted_by_rr[0][0]}")
    print(f"  A quant trader doesn't chase highest return —")
    print(f"  they chase highest RETURN PER UNIT OF RISK.")
    print(f"\n  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Author    : Shivam Tyagi  |  github.com/QuantShivam")
    print(f"  Module    : Mathematics Foundation — 11/11 Topics")
    print(f"{'═' * 70}\n")


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║         NSE QUANT MATHEMATICS TOOLKIT                          ║")
    print("║         Risk & Return Analytics for Indian Markets             ║")
    print("║  5 NSE Stocks  ×  20 Trading Days  ×  11 Math Topics          ║")
    print("║  Author: Shivam Tyagi  |  github.com/QuantShivam              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    all_returns      = topic_1_returns()
    means, weights   = topic_2_mean(all_returns)
    stds             = topic_3_std_dev(all_returns, means)
    topic_4_normal_distribution(all_returns, means, stds)
    topic_5_correlation(all_returns)
    topic_6_probability(all_returns)
    topic_7_expected_value(all_returns)
    topic_8_compounding()
    topic_9_log_returns(all_returns)
    topic_10_linear_algebra(all_returns, means, stds)
    topic_11_calculus(all_returns)
    print_final_summary(all_returns, means, stds)


if __name__ == "__main__":
    main()