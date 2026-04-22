# NSE Quant Mathematics Toolkit

**The 11 math concepts every quant needs — built from scratch in NumPy, with every formula visible.**

Most quant tutorials hand you a library and tell you to trust it. This repo does the opposite: each concept is implemented from first principles so you can see exactly what is happening inside `.mean()`, `.std()`, `np.corrcoef()`, and every other function you'd normally call.

Built as a transparent reference for anyone learning the math foundation of quantitative trading.

---

## The 11 topics

| # | Topic | What it answers |
|---|---|---|
| 1 | Percentages & Returns | Daily and period returns from price data |
| 2 | Mean (Simple & Weighted) | Portfolio average performance |
| 3 | Standard Deviation & Variance | How much a strategy's returns swing |
| 4 | Normal Distribution | The 68-95-99.7 rule, applied to returns |
| 5 | Correlation Matrix | How stocks move together (diversification) |
| 6 | Probability Basics | Win rate, loss rate, empirical probabilities |
| 7 | Expected Value | Is there an edge per trade, in expectation? |
| 8 | Compounding | Rule of 72, long-term growth math |
| 9 | Logarithmic Returns | Why quants prefer log returns over simple returns |
| 10 | Linear Algebra | Portfolio weights as a dot product |
| 11 | Calculus Concepts | Rate of change, momentum, derivatives of price |

Each topic is a self-contained Python function with inline comments explaining the formula.

---

## How to run

```bash
pip install numpy
python NSE_Quant_Maths_Toolkit.py
```

Output: a formatted report showing each of the 11 calculations applied to sample NSE stock data (RELIANCE, TCS, INFY, HDFCBANK, TATASTEEL over 20 trading days).

---

## Why this exists

You cannot backtest a strategy you do not understand the math of. You cannot size a position using Kelly if you cannot derive Kelly. You cannot interpret a Sharpe ratio if the Sharpe formula is a black box to you.

This toolkit is the foundation that every later tool in my portfolio — [trading-stats-analyzer](https://github.com/QuantShivam/trading-stats-analyzer), backtesting engines, risk calculators — is built on. Publishing the foundation separately is how I prove the foundation exists.

---

## About the author

**Shivam Tyagi** — CMT Level I charterholder. Python developer focused on quantitative tools for Indian markets. Available for freelance work on data automation, backtesting, and trading analytics projects.

[github.com/QuantShivam](https://github.com/QuantShivam) · [shivam@quantshivam.com](mailto:shivam@quantshivam.com) · [LinkedIn](https://www.linkedin.com/in/-shivam-tyagi-/)