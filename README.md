# Eleysian Billing
Analyse NEM12 data to provide billing estimates for Elysian Energy plans

This is a simple Python program to apply [Eleysian Energy's(https://eleysianenergy.com.au) Sun/Moon electricity billing to NEM12 meter data.  

You can request your metering data from your electricity retailer or distributor.  You need to have an interval ('smart') reader installed to get the billing data you need;  A non-interval meter will not have the timestamped readings that are required.

The actual rates for your plan will vary based on your location.  You can specify the various rates using command line arguments

```
usage: meterread.py [-h] [--sun SUN] [--moon MOON] [--suninc SUNINC]
                    [--mooninc MOONINC] [--feedin FEEDIN] [--plan PLAN]
                    NEM12file

Process NEM12 using Elysian billing model.

positional arguments:
  NEM12file          NEM12 file to be processed

optional arguments:
  -h, --help         show this help message and exit
  --sun SUN          "Sun" rate in c/kWh (default 22c/kWh)
  --moon MOON        "Moon" rate in c/kWh (default 11c/kWh)
  --suninc SUNINC    Included "Sun" kWh (default 150kWh)
  --mooninc MOONINC  Included "Moon" kWh (default 100kWh)
  --feedin FEEDIN    Feed in rate c/kWh (default 9c/kWh)
  --plan PLAN        Monthly plan cost (default $80)
  ```