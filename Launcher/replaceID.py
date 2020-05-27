import os
import random
import json
import string

# replacing history ID with a random one
for i in os.listdir("../allure-results"):
	if (i.endswith("-result.json")):
		newHistoryID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
		with open("../allure-results/" + i, "r") as res_json:
			results = json.load(res_json)
			results["historyId"] = newHistoryID
		with open("../allure-results/" + i, "w") as res_json:
			json.dump(results, res_json)