import json

from sec_api import QueryApi


# get the 13F filings from a couple days
queryApi = QueryApi(api_key="YOUR-API-KEY")
query = {
    "query": {
        "query_string": {
            "query": "formType:\"13F\" AND filedAt:[2022-10-18 TO 2022-10-20]"
        }
    },
    "from": "0",
    "size": "20",
    "sort": [{"filedAt": {"order": "desc"}}]
}
response = queryApi.get_filings(query)
# filings has all the filings, 0 is the first one and holdings narrows
# down to the holdings of the first filing
holdings_data = response["filings"][0]["holdings"]
print(json.dumps(holdings_data, indent=2))
# write to file
with open("test_sec_api_13f_data.json", "w") as f:
    json.dump(holdings_data, f, indent=2)
