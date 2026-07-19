# Smart Energy Billing System

A Python console application that tracks household electricity consumption per appliance, calculates bills with separate peak and normal tariff rates, visualizes usage patterns, and forecasts next month's consumption and cost using linear regression.

## Features

- **Multi-user management** — add and remove users, each with their own appliance set, usage records, and bill
- **Appliance catalog** — 10 preloaded household appliances with realistic power ratings (75 W ceiling fan to 1500 W air conditioner), with per-appliance kWh calculation from usage hours
- **Usage tracking** — record daily usage hours per appliance across any period (1–365 days), with high-usage warnings when a day exceeds the overload threshold
- **Dual-tariff billing** — separate peak (Rs. 25/kWh) and normal (Rs. 15/kWh) rates, both adjustable at runtime; peak-hour usage is currently simulated via random flagging (~30% of records)
- **Four visualizations** (matplotlib, saved as 300 dpi PNGs):
  - Per-appliance monthly consumption (bar chart)
  - Daily consumption trend with average line
  - Peak vs. normal usage per day (stacked bars)
  - 30-day consumption forecast with trend line
- **Consumption forecasting** — fits a scikit-learn linear regression to daily consumption and extrapolates the next 30 days, estimating the upcoming bill using the observed peak/normal ratio
- **CSV exports** — per-user usage logs, itemized bills, and a system-wide summary report

## Tech stack

Python 3.8+ · NumPy · matplotlib · scikit-learn

## Setup

```bash
git clone https://github.com/Bushra31/smart-energy-billing
cd smart-energy-billing
pip install -r requirements.txt
python main.py
```

Output folders (`data/`, `reports/`, `visualizations/`) are created automatically on first run.

## How the prediction works

Daily totals are aggregated from the usage records, a linear regression is fit on day index vs. kWh, and the model extrapolates 30 days forward (clamped at zero). The predicted total is split into peak and normal shares using the historical peak ratio, then priced at the current tariff rates to estimate next month's bill.

## Project structure

```
main.py     — menu loop and input validation
system.py   — data model (Appliance, User, SystemInfo), billing,
              simulation, visualization, prediction, CSV export
```

## Possible improvements

- Time-of-day based peak detection instead of simulated peak flagging
- Persisting users and usage data between sessions
- Auto-generated usage mode for faster demos and testing
