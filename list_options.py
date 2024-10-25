#!/usr/bin/env python3
"""
List calls & put options for the specified ticker at some expiration date
"""

import argparse
import sys

import pandas as pd
import yfinance as yf  # type: ignore


def process_options(options: pd.DataFrame, expiration_date: str) -> pd.DataFrame:
    """
    Process options
    """
    options["expirationDate"] = expiration_date
    options["ITM/OTM"] = options["inTheMoney"].apply(lambda x: "ITM" if x else "OTM")
    # Convert implied volatility to a fixed-width percentage format
    options["IV"] = (options["impliedVolatility"] * 100).round(2)
    # Drop columns with all NaN values
    options.dropna(axis=1, how="all", inplace=True)
    return options


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

    all_calls = pd.DataFrame()
    all_puts = pd.DataFrame()

    expiration_dates = (
        stock.options if week_offset == -1 else [stock.options[week_offset]]
    )

    for expiration_date in expiration_dates:
        calls = process_options(
            stock.option_chain(expiration_date).calls, expiration_date
        )
        puts = process_options(
            stock.option_chain(expiration_date).puts, expiration_date
        )
        all_calls = pd.concat([all_calls, calls], ignore_index=True)
        all_puts = pd.concat([all_puts, puts], ignore_index=True)

    # Sort calls and puts by the specified sort key and reverse if needed
    all_calls = all_calls.sort_values(by=sort_key, ascending=not reverse)
    all_puts = all_puts.sort_values(by=sort_key, ascending=not reverse)

    keys = [
        "contractSymbol",
        "expirationDate",
        "ITM/OTM",
        "strike",
        "volume",
        "openInterest",
        "IV",
    ]

    # Select only the necessary columns
    all_calls = all_calls[keys].head(max_rows)
    all_puts = all_puts[keys].head(max_rows)

    # Print results
    print("Calls Options:\n", all_calls.to_string(index=False))
    print("Puts Options:\n", all_puts.to_string(index=False))


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
        help="week offset from the current week (0 = this week, 1 = next week, -1 = all weeks, etc)",
    )
    args = parser.parse_args()

    args.sort = args.sort.replace("OI", "openInterest")

    # Get options data
    print_options(args.ticker, args.week, args.sort, args.reverse, args.max_rows)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
