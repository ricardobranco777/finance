
## Requirements

- Python 3
- pandas
- yfinance

## [list_options](list_options.py)

Example:

```
# List options expiring Friday next week for Amazon sorted by volume:
list_options.py -w 1 -s volume -r AMZN
Calls Options:
      contractSymbol ITM/OTM  strike    IV  volume  openInterest
AMZN241101C00190000     OTM   190.0 59.78    5453         11430
AMZN241101C00195000     OTM   195.0 58.17    4908         21940
AMZN241101C00200000     OTM   200.0 56.40    3806         18816
AMZN241101C00205000     OTM   205.0 53.91    2868          8547
AMZN241101C00210000     OTM   210.0 53.32    2052          6108
Puts Options:
      contractSymbol ITM/OTM  strike    IV  volume  openInterest
AMZN241101P00180000     OTM   180.0 54.30    2790          5505
AMZN241101P00190000     ITM   190.0 53.53    1394          5635
AMZN241101P00175000     OTM   175.0 54.13     899          7108
AMZN241101P00170000     OTM   170.0 54.59     606          6019
AMZN241101P00185000     OTM   185.0 54.24     596          6313
```

```
usage: list_options.py [-h] [-n MAX_ROWS] [-s {strike,volume,openInterest}] [-r] [-w WEEK] ticker

list options for ticker

positional arguments:
  ticker                Stock ticker symbol

options:
  -h, --help            show this help message and exit
  -n MAX_ROWS, --max-rows MAX_ROWS
                        maximum number of rows to display (default: 5)
  -s {strike,volume,OI}, --sort {strike,volume,OI}
                        sorting key for the options (default: strike)
  -r, --reverse         reverse the sorting order (default: False)
  -w WEEK, --week WEEK  week offset from the current week (0 = this week, 1 = next week, etc) (default: 0)
```
