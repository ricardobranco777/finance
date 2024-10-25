#!/usr/bin/env python3
"""
List calls & put options for the specified ticker at some expiration date
"""

import argparse
import sys

import pandas as pd
import yfinance as yf  # type: ignore


def print_options(
    ticker: str,
    week_offset: int = 0,
    sort_key: str = "strike",
    reverse: bool = False,
    max_rows: int = 5,
) -> None:
    """
    Get options for ticker
    """
    stock = yf.Ticker(ticker)

    expiration_date = stock.options[week_offset]
    print(f"Expiration date: {expiration_date}")

    # Fetch call and put options data for the given expiration date
    calls = stock.option_chain(expiration_date).calls
    puts = stock.option_chain(expiration_date).puts

    # Use the inTheMoney key for ITM/OTM status
    calls["ITM/OTM"] = calls["inTheMoney"].apply(lambda x: "ITM" if x else "OTM")
    puts["ITM/OTM"] = puts["inTheMoney"].apply(lambda x: "ITM" if x else "OTM")

    # Convert implied volatility to percentage format and rename column to "IV"
    calls["IV"] = (calls["impliedVolatility"] * 100).round(2)
    puts["IV"] = (puts["impliedVolatility"] * 100).round(2)

    # Sort calls and puts by the specified sort key and reverse if needed
    calls = calls.sort_values(by=sort_key, ascending=not reverse)
    puts = puts.sort_values(by=sort_key, ascending=not reverse)

    # Select only the necessary columns
    calls = calls[
        ["contractSymbol", "ITM/OTM", "strike", "IV", "volume", "openInterest"]
    ].head(max_rows)
    puts = puts[
        ["contractSymbol", "ITM/OTM", "strike", "IV", "volume", "openInterest"]
    ].head(max_rows)

    # Print results
    print("Calls Options:\n", calls.to_string(index=False))
    print("Puts Options:\n", puts.to_string(index=False))


def main():
    """
    Main
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="list options for ticker",
    )
    parser.add_argument("ticker", type=str, help="Stock ticker symbol")
    parser.add_argument(
        "-n",
        "--max-rows",
        type=int,
        default=5,
        help="maximum number of rows to display",
    )
    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        choices=["strike", "volume", "OI"],
        default="strike",
        help="sorting key for the options",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="reverse the sorting order"
    )
    parser.add_argument(
        "-w",
        "--week",
        type=int,
        default=0,
        help="week offset from the current week (0 = this week, 1 = next week, etc)",
    )
    args = parser.parse_args()

    args.sort = args.sort.replace("OI", "openInterest")

    # Get options data
    print_options(
        args.ticker, args.week, args.sort, args.reverse, args.max_rows
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
