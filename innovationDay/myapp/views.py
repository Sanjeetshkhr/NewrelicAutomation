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
