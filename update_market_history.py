import os
import json
from http.client import HTTPConnection

THE_FORGE_REGION_ID = 10000002
PI_MARKET_GROUP = 1332

def get_history_for_typeid(typeid, regionid, conn):
    conn.request("GET", "/market/%d/types/%d/history/" % (regionid, typeid))
    resp = conn.getresponse()
    assert(resp.status == 200)
    return resp.read().decode()

if __name__ == "__main__":
    if not os.path.exists("market_history"):
        os.mkdir("market_history")

    conn = HTTPConnection("public-crest.eveonline.com", 80)

    conn.request("GET",
    "/market/types/?group=http://public-crest.eveonline.com/market/groups/%d/"
    % PI_MARKET_GROUP)

    resp = conn.getresponse()
    assert(resp.status == 200)
    body = json.loads(resp.read().decode())

    for item in body["items"]:
        typeid = item["type"]["id"]
        hist = get_history_for_typeid(typeid, THE_FORGE_REGION_ID, conn)
        open("market_history/%d.json" % typeid, "w").write(hist)
        print("Updated", item["type"]["name"], "(%d)" % typeid)
