from nemreader import read_nem_file
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description='Process NEM12 using Elysian billing model.')
parser.add_argument('NEM12file', type=read_nem_file,
                    help='NEM12 file to be processed')
parser.add_argument('--sun', type=int, default=22, help = '"Sun" rate in c/kWh (default 22c/kWh)')
parser.add_argument('--moon', type=int, default=11, help = '"Moon" rate in c/kWh (default 11c/kWh)')
parser.add_argument('--suninc', type=int, default=150, help = 'Included "Sun" kWh (default 150kWh)')
parser.add_argument('--mooninc', type=int, default=100, help = 'Included "Moon" kWh (default 100kWh)')
parser.add_argument('--feedin', type=int, default=9, help = 'Feed in rate c/kWh (default 9c/kWh)')
parser.add_argument('--plan', type=int, default=80, help = 'Monthly plan cost (default $80)')

args = parser.parse_args()

m = args.NEM12file

powerUsage = {}

for nmi in m.readings:
    consumption = 'E1'
    for reading in m.readings[nmi][consumption]:
        key = reading.t_start.strftime('%Y-%m')
        monthData = powerUsage.get(key, { "sun": 0, "moon": 0, "export":0})
        if reading.t_start.hour >= 7 and reading.t_start.hour < 19:
            monthData["sun"] = monthData["sun"] + reading.read_value
        else:
            monthData["moon"] = monthData["moon"] + reading.read_value
        powerUsage[key] = monthData

    export = 'B1'
    for reading in m.readings[nmi][export]:
        key = reading.t_start.strftime('%Y-%m')
        monthData = powerUsage.get(key, { "sun": 0, "moon": 0, "export":0})
        monthData["export"] = monthData["export"] + reading.read_value
        powerUsage[key] = monthData

total = 0
print('Period\tSun usage\tMoon usage\tExport\t\tPeriod cost')
for key in powerUsage:
    monthData = powerUsage[key]
    sun = max(0,monthData["sun"] - args.suninc)
    moon = max(0,monthData["moon"] - args.mooninc)
    export = monthData["export"]
    cost = args.plan + args.sun/100 * sun + args.moon/100 * moon - export * args.feedin / 100
    total = total + cost
    print('{}\t{:.3f}kWh\t{:.3f}kWh\t{:.3f}kWh\t${:.2f}'.format(key,sun,moon,export,cost))
print('\nTotal cost ${:.2f}'.format(total))