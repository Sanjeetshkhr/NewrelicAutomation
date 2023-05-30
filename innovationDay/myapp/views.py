from django.shortcuts import render
import requests
import json
# Create your views here.
def index(request):
    return render(request, 'index.html')

def queryAccounts(request):
    accountName = request.GET['account-name']
    headers = {
        'Content-Type': 'application/json',
        'API-Key': 'NRAK-',
    }
    available_accounts = {
        'query': '{\n  actor {\n    accounts {\n      id\n      name\n    }\n  }\n}\n',
        'variables': '',
    }
    response = requests.post('https://api.newrelic.com/graphql', headers=headers, json=available_accounts)
    accounts = response.json()['data']['actor']['accounts']
    for i in accounts:
        exists = False
        if i['name'] == accountName:
            id = i['id']
            exists = True
    return render(request, 'queryAccounts.html', {'accountName':accountName, 'exists': exists, 'accountId': id})


def createAccount(request):
    accountName = request.GET['account-name']
    headers = {
        'Content-Type': 'application/json',
        'API-Key': 'NRAK-',
    }
    create_account = {
    'query': 'mutation {\n  accountManagementCreateAccount(managedAccount: {name: "test"}) {\n    managedAccount {\n      id\n      name\n      regionCode\n    }\n  }\n}\n',
    'variables': '',
    }

    response = requests.post('https://api.newrelic.com/graphql', headers=headers, json=create_account)
    accountId = response.json()['data']['accountManagementCreateAccount']['managedAccount']['id']
    accountName = response.json()['data']['accountManagementCreateAccount']['managedAccount']['name']
    accountRegion = response.json()['data']['accountManagementCreateAccount']['managedAccount']['regionCode']
    return render(request, 'createAccount.html', {'accountName':accountName, 'accountId': accountId, 'accountRegion': accountRegion })


def linkAccount(request):
    accountID = request.GET['account-id']
    app_groupID = request.GET['group-id']

    #Add group ids for respective groups
    engg_groupID = '<add engg group id>'
    l2_groupID = '<add l2 group id>'
    sre_groupID = '<add sre group id>'

    #Add role id for respective groups
    app_roleID = '<add engg role id>'
    engg_roleID = '<add engg role id>'
    l2_roleID = '<add l2 role id>'
    sre_roleID = '<add sre role id>'

    headers = {
        'Content-Type': 'application/json',
        'API-Key': 'NRAK-RY2I9OJ4V4OG1PI1PDX54IVCE8R',
    }

    app_group = {
        'query': 'mutation {\n  authorizationManagementGrantAccess(grantAccessOptions: {groupId: "'+app_groupID+'", accountAccessGrants: {accountId: '+accountID+', roleId: "'+app_roleID+'"}}) {\n    roles {\n      displayName\n      accountId\n    }\n  }\n}\n',
        'variables': '',
    }
    engg_group = {
        'query': 'mutation {\n  authorizationManagementGrantAccess(grantAccessOptions: {groupId: "'+engg_groupID+'", accountAccessGrants: {accountId: '+accountID+', roleId: "'+engg_roleID+'"}}) {\n    roles {\n      displayName\n      accountId\n    }\n  }\n}\n',
        'variables': '',
    }
    l2_group = {
        'query': 'mutation {\n  authorizationManagementGrantAccess(grantAccessOptions: {groupId: "'+l2_groupID+'", accountAccessGrants: {accountId: '+accountID+', roleId: "'+l2_roleID+'"}}) {\n    roles {\n      displayName\n      accountId\n    }\n  }\n}\n',
        'variables': '',
    }
    sre_group = {
        'query': 'mutation {\n  authorizationManagementGrantAccess(grantAccessOptions: {groupId: "'+sre_groupID+'", accountAccessGrants: {accountId: '+accountID+', roleId: "'+sre_roleID+'"}}) {\n    roles {\n      displayName\n      accountId\n    }\n  }\n}\n',
        'variables': '',
    }

    link_app_grp = requests.post('https://api.newrelic.com/graphql', headers=headers, json=app_group)
    link_engg_grp = requests.post('https://api.newrelic.com/graphql', headers=headers, json=engg_group)
    link_l2_grp = requests.post('https://api.newrelic.com/graphql', headers=headers, json=l2_group)
    link_sre_grp = requests.post('https://api.newrelic.com/graphql', headers=headers, json=sre_group)

    accountId = link_app_grp.json()['data']['accountManagementCreateAccount']['managedAccount']['id']
    accountName = link_app_grp.json()['data']['accountManagementCreateAccount']['managedAccount']['name']

    return render(request, 'linkAccount.html', {'accountName':accountName, 'accountId': accountId , 'app_group': app_groupID})