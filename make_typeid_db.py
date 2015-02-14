from http.client import HTTPConnection
import json

def load_type_page(page, conn):
    conn.request("GET", "/types/?page=%d" % page)
    resp = conn.getresponse()
    assert(resp.status == 200)
    return json.loads(resp.read().decode())

def make_typeid_db(conn):
    page_json = load_type_page(1, conn)
    total_pages = page_json["pageCount"]
    items = page_json["items"]

    for page in range(2, total_pages):
        page_json = load_type_page(page, conn)
        items.extend(page_json["items"])
        print("Page:", page, "done.")

    name_typeid_map = dict([(item["name"], int(item["href"].split("/")[-2])) \
            for item in items])
    return name_typeid_map

if __name__ == "__main__":
    conn = HTTPConnection("public-crest.eveonline.com", 80)
    typeid_dict = make_typeid_db(conn)
    open("typeids.py", "w").write("typeid = %s" % typeid_dict.__repr__())
