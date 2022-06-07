from fee_sys.auth import *
import requests


# Branch request
url = branch_url
payload = payload
headers = headers
branches = requests.request("GET", url, headers=headers, data=payload).json()['data']


# Member category request
url = member_category_url
payload = payload
headers = headers
member_categories = requests.request("GET", url, headers=headers, data=payload).json()['data']

# Group request
url = group_url
payload = payload
headers = headers
groups = requests.request("GET", url, headers=headers, data=payload).json()['data']


# SubGroup request
url = subgroup_url
payload = payload
headers = headers
subgroups = requests.request("GET", url, headers=headers, data=payload).json()['data']

# Member request
url = members_url
payload = payload
headers = headers
members = requests.request("GET", url, headers=headers, data=payload).json()['results']
