# Backend Coding Challenge – Order Book Aggregator

## Objective

Build a BTC-USD order book aggregator that pulls live data from multiple crypto exchanges and calculates the best execution price to buy or sell a given quantity of Bitcoin. This test evaluates your ability to work with real-world APIs, reason about raw data, and write clean, functional Python code.

## Real-World Scenario

You're building a pricing engine for a crypto platform that sources liquidity from multiple exchanges. Your goal is to determine how much it would cost a customer to buy or sell 10 BTC using the best available offers across these exchanges.

## Task Requirements

Create a Python script (not a class-based module) that:

1. **Fetches order books from two exchanges**:

   * Coinbase Pro: `https://api.exchange.coinbase.com/products/BTC-USD/book?level=2`
   * Gemini: `https://api.gemini.com/v1/book/BTCUSD`

2. **❗ No documentation is provided** — you'll need to inspect and reverse-engineer the responses yourself. This is intentional and simulates working with undocumented or legacy systems.

3. Parses the order book responses and normalizes them into two lists:

```text
bids = [[price, size], ...]  # sorted descending
asks = [[price, size], ...]  # sorted ascending
```

4. **Simulates exchange rate limiting**:
   * Each exchange can be called at most once every 2 seconds.
   * Build your own RateLimiter using a decorator, a closure, or other approach. No `time.sleep()` delays allowed in core logic.

5. **Calculates execution prices**:
   * To buy, walk down the asks (lowest prices first) and sum the cost of acquiring 10 BTC.
   * To sell, walk up the bids (highest prices first) and sum the revenue from selling 10 BTC.
   * Use liquidity from both exchanges as needed.

6. **Supports command-line parameter `--qty`** to set quantity (default: 10 BTC).

7. **Prints the output in this format**:

```text
To buy 10 BTC: $XXX,XXX.XX
To sell 10 BTC: $YYY,YYY.YY
```
