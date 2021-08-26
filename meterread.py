from nemreader import read_nem_file
from pprint import pprint

m = read_nem_file(
    '/Users/paulw/Downloads/REQ-46972-1_4311113637_20210811153538_INTEGP_INTERVAL_DET.csv')

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
for key in powerUsage:
    monthData = powerUsage[key]
    sun = max(0,monthData["sun"] - 150)
    moon = max(0,monthData["moon"] - 100)
    export = monthData["export"]
    cost = 80 + 0.22 * sun + 0.11 * moon - export * 0.09
    total = total + cost
    print('{} {:.3f}KWh {:.3f}KWh {:.3f}KWh ${:.2f}'.format(key,sun,moon,export,cost))
print('{:.2f}'.format(total))