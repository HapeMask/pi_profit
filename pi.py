import sys
import json
import datetime

from typeids import typeid
from schematics import tiers, schematics

N_HIST_DAYS = 10

def avg_price_for_typeid(typeid, days):
    trans = json.load(open("market_history/%d.json" % typeid, "r"))["items"]
    trans = sorted(trans,
            key =
                lambda i : datetime.datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S")
                )[::-1][:days]

    total_volume = float(sum(item["volume"] for item in trans))
    return sum([item["avgPrice"] * item["volume"] / total_volume for item in trans])

def schematic_stats(schematic, factory_mode, history_days = N_HIST_DAYS):
    output_qty, output = schematic["output"]
    output_price = avg_price_for_typeid(typeid[output], days = history_days)
    input_costs = []

    if factory_mode:
        qtys, names = zip(*schematic["inputs"])
        avg_prices = [avg_price_for_typeid(typeid[name], days = history_days) for name in names]
        input_costs = list(zip(names, avg_prices))

        profit = output_qty * output_price - sum(qty * ap for qty, ap in zip(qtys, avg_prices))
    else:
        profit = output_price * output_qty

    return (output, profit, output_price, input_costs)

def print_chart(factory_mode=True, show_prices=True):
    for tier in tiers:
        print("----[%s%s]----" % (tier, "(w/ purchased inputs)" if factory_mode else ""))
        results = []
        for schematic in schematics[tier]:
            results.append(schematic_stats(schematic, factory_mode))

        maxlen = max(len(r[0]) for r in results)

        for output, profit, o_price, i_costs in sorted(results, key = lambda res : res[1])[::-1]:
            if show_prices:
                print(("\t{:<%d} Profit: {:.2f} (Sell at: {:.2f})" % maxlen).format(output, profit, o_price))
                print("\t\t" + "\n\t\t".join(["%s : %0.2f" % ic for ic in i_costs]))
                print()
            else:
                print(("\t{:<%d} Profit: {:.2f}" % maxlen).format(output, profit))

if __name__ == "__main__":
    sp = "-p" in sys.argv
    fm = "-f" in sys.argv
    print_chart(fm, sp)
