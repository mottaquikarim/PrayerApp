*** Settings ***

Resource  ./shared.robot

*** Test Cases ***
GET request to /location/{lat}/{lng} returns status code of 200
	Assert /${STAGE}/location/40.7127753/-74.0059728 Returns 200

GET request for location (40.7127753,-74.0059728) at 05/25/18 returns sunset=8:15pm
    ${sub_dict}=    evaluate    json.loads('''{"sunset": "8:15pm"}''')    json
	Assert /${STAGE}/location/40.7127753/-74.0059728?date=1527249151 Contains ${sub_dict}

GET request for location (40.7127753,-74.0059728) at 05/25/18 with time-format=24h returns sunset=20:15
    ${sub_dict}=    evaluate    json.loads('''{"sunset": "20:15"}''')    json
	Assert /${STAGE}/location/40.7127753/-74.0059728?date=1527249151&time-format=24h Contains ${sub_dict}

GET request for location (40.7127753,-74.0059728) at 05/25/18 with calc-method=Tehran returns maghrib=8:38pm
    ${sub_dict}=    evaluate    json.loads('''{"maghrib": "8:38pm"}''')    json
	Assert /${STAGE}/location/40.7127753/-74.0059728?date=1527249151&calc-method=Tehran Contains ${sub_dict}

GET request for location (40.7127753,-74.0059728) at 05/25/18 with default calc-method (ISNA) returns maghrib=8:15pm
    ${sub_dict}=    evaluate    json.loads('''{"maghrib": "8:15pm"}''')    json
	Assert /${STAGE}/location/40.7127753/-74.0059728?date=1527249151 Contains ${sub_dict}

GET request to /location/{lat}/{lng} with bogus lat/lng values returns status code of 400
	Assert /${STAGE}/location/a/-b Returns 400
