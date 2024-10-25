#!/usr/bin/env python3
"""
List calls & put options for the specified ticker at some expiration date
"""

import argparse
import sys
from datetime import date, timedelta

import pandas as pd
import yfinance as yf  # type: ignore


def get_friday_of_week(week_offset: int) -> str:
    """
    Calculate the date of Friday for the specified week offset
    """
    today = date.today()
    # Calculate the number of days to add for the specified week
    days_to_friday = (4 - today.weekday()) + (week_offset * 7)  # 4 is Friday
    friday_date = today + timedelta(days=days_to_friday)
    return friday_date.isoformat()


def list_options(
    ticker: str,
    expiration_date: str,
    sort_key: str = "strike",
    reverse: bool = False,
    max_rows: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Get options for ticker
    """
    stock = yf.Ticker(ticker)

    if expiration_date not in stock.options:
        sys.exit(
            f"ERROR: Expiration date {expiration_date} is not available for {ticker}"
        )

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

    return calls, puts


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
        choices=["strike", "volume", "openInterest"],
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

    # Get the expiration date based on the week offset
    expiration_date = get_friday_of_week(args.week)

    # Get options data
    calls_data, puts_data = list_options(
        args.ticker, expiration_date, args.sort, args.reverse, args.max_rows
    )

    # Print results
    print("Calls Options:\n", calls_data.to_string(index=False))
    print("Puts Options:\n", puts_data.to_string(index=False))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
