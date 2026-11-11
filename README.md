# County Report

## Function
`get_county_report(county, start_date, end_date)`

Returns DataFrame:
product | total_orders | total_quantity | total_revenue_kes

## Example
get_county_report("Nairobi", "2024-01-01", "2024-01-31")
-> Maize Flour 2kg | 1 | 50 | 6000

## Empty result
If no orders in that county/date range, it prints:
"No results for {county} from {start_date} to {end_date}"
and returns an empty DataFrame.

## Pricing Note
Manual Monday report = ~1hr/week typing SQL = 52 hrs/year.
Automated function = 1 run, same output, no typos, no SQL injection risk because it uses `?` placeholders.
Value to client: saves time + prevents wrong totals from manual copy-paste.
