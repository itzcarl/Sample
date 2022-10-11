import requests
import json

#Your jenkins URL and credentials goes here
url = 'https://jenkins-server.com/job/folder/job/Jobname/api/json'
username = 'username'
password = 'you access token'


#Use the 'auth' parameter to send requests with HTTP Basic Auth:
#Accessing the Job page to get the latest Build ran.
response = requests.post(url, auth = (username, password),verify=False)

try:
    buildnumberJson = json.loads(response.text)
except:
    print ("Failed to parse json")

if "lastBuild" in buildnumberJson:  
    totalbuilds = buildnumberJson["lastBuild"]
    runs = totalbuilds["number"]
    
else:
    print ("Failed to get build")

#Iterate over the job build runs to get the build status for each

totalsuccess = totalfailure = totalmissing = 0

for build in range(1,runs):
    buildurl= 'https://jenkins-server.com/job/folder/job/Jobname/api/json' + str(build) + '/api/json'
    print(buildurl)
    buildstatus = []
    try:
        response = requests.post(buildurl, auth = (username, password),verify=False)
        buildstatus = json.loads(response.text)
    except Exception as e:
        totalmissing =  totalmissing + 1  
    if "result" in buildstatus:
        if buildstatus["result"] == "SUCCESS" :
            totalsuccess = totalsuccess + 1
        if buildstatus["result"] == "FAILURE" :
            totalfailure = totalfailure + 1


#Generate Output numbers

print(f"total builds:{runs}")
print(f"total succeeded builds:{totalsuccess}")
print(f"total failed builds:{totalfailure}")
print(f"total skipped builds:{totalmissing}")