import json

headers = {
  'Authorization': 'Token 062c3943a61676d3910c6ea96afa2e6d7d4ec8966c50a094ecb74a03419b3fd4',
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=Ly8oYWb8c70C2CDUYfFd0poVjCL91Octs99w3q6rGjSu8L2SaPVDoGPvJ4tKQIda; sessionid=4zyr1pvz9r6hyu8sqvuh0gqqxsymo56n'
}

payload = json.dumps({
  "phone_email": "gideon@123.com",
  "password": "@t@@p3w.com"
})

base_url = "http://api.akwaabaapp.com"

# URLS
branch_url = base_url + "/clients/branch"
member_category_url = base_url + "/members/groupings/member-category"
group_url = base_url + "/members/groupings/group"
subgroup_url = base_url + "/members/groupings/sub-group"
members_url = base_url + "/members/user"