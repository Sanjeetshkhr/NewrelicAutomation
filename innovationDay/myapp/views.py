from django.shortcuts import render
from django.shortcuts import redirect
import requests
import json
from django.contrib import messages
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
    if response.status_code == 200:
        for i in accounts:
            exists = False
            if i['name'] == accountName:
                id = i['id']
                exists = True
        return render(request, 'queryAccounts.html', {'accountName':accountName, 'exists': exists, 'accountId': id})
    else:
        messages.info(request, 'Request unsuccessful please try again')
        return redirect(index)


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
    if response.status_code == 200:
        accountId = response.json()['data']['accountManagementCreateAccount']['managedAccount']['id']
        accountName = response.json()['data']['accountManagementCreateAccount']['managedAccount']['name']
        accountRegion = response.json()['data']['accountManagementCreateAccount']['managedAccount']['regionCode']
        return render(request, 'createAccount.html', {'accountName':accountName, 'accountId': accountId, 'accountRegion': accountRegion })
    else:
        messages.info(request, 'Request unsuccessful please try again')
        return redirect(index)

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
        'API-Key': 'NRAK-',
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
    link_l2_grp = requests.post('https://api.newrelic.com/graphql', headers=headers, json=sre_group)
    if link_app_grp.status_code != 200:
        messages.info(request, 'linking app group unsuccessful please try again')
        return redirect(index)
    elif link_engg_grp.status_code != 200:
        messages.info(request, 'linking engg group unsuccessful please try again')
        return redirect(index)
    elif link_l2_grp.status_code != 200:
        messages.info(request, 'linking l2 group unsuccessful please try again')
        return redirect(index)
    elif link_l2_grp.status_code != 200:
        messages.info(request, 'linking sre group unsuccessful please try again')
        return redirect(index)
    else:    
        accountId = link_app_grp.json()['data']['authorizationManagementGrantAccess']['roles']['accountId']
        accountName = link_app_grp.json()['data']['authorizationManagementGrantAccess']['roles']['displayName']

        return render(request, 'linkAccount.html', {'accountName':accountName, 'accountId': accountId , 'app_group': app_groupID})