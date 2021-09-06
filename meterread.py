from readNEM import read_NEM
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description='Process NEM12 using Elysian billing model.')
parser.add_argument('NEM12file',
                    help='NEM12 file to be processed')
parser.add_argument('--headers', action="store_true", help = 'Allow NEM12 files with missing headers')
parser.add_argument('--sun', type=float, default=0.22, help = '"Sun" rate in $/kWh (default $0.22/kWh)')
parser.add_argument('--moon', type=float, default=0.11, help = '"Moon" rate in $/kWh (default $0.11/kWh)')
parser.add_argument('--suninc', type=int, default=150, help = 'Included "Sun" kWh (default 150kWh)')
parser.add_argument('--mooninc', type=int, default=100, help = 'Included "Moon" kWh (default 100kWh)')
parser.add_argument('--feedin', type=float, default=0.09, help = 'Feed in rate c/kWh (default $0.09c/kWh)')
parser.add_argument('--plan', type=int, default=80, help = 'Monthly plan cost (default $80)')

args = parser.parse_args()
try:
    m = read_NEM(args.NEM12file, args.headers)

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
        cost = args.plan + args.sun * sun + args.moon * moon - export * args.feedin
        total = total + cost
        print('{}\t{:.3f}kWh\t{:.3f}kWh\t{:.3f}kWh\t${:.2f}'.format(key,sun,moon,export,cost))
    print('\nTotal cost ${:.2f}'.format(total))
except FileNotFoundError:
    print("NEM file could not be read")
except Exception as e:
    print(e)