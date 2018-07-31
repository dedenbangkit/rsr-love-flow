import pandas as pd
import requests
import logging
from config import email, password, instanceURI, survey_id

logging.basicConfig(level=logging.WARN)

requestURI = 'https://api.akvo.org/flow/orgs/' + instanceURI
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
tokenURI = 'https://login.akvo.org/auth/realms/akvo/protocol/openid-connect/token'
rtData = {
    'client_id':'curl',
    'username': email,
    'password': password,
    'grant_type':'password',
    'scope':'openid offline_access'
}

def refreshData():
    tokens = requests.post(tokenURI, rtData).json();
    return tokens['refresh_token']

def getAccessToken():
    account = {
        'client_id':'curl',
        'refresh_token': refreshData(),
        'grant_type':'refresh_token'
    }
    try:
        account = requests.post(tokenURI, account).json();
    except:
        logging.error('FAILED: TOKEN ACCESS UNKNOWN')
        return False
    return account['access_token']

def getResponse(url):
    header = {
        'Authorization':'Bearer ' + getAccessToken(),
        'Accept': 'application/vnd.akvo.flow.v2+json',
        'User-Agent':'python-requests/2.14.2'
    }
    response = requests.get(url, headers=header).json()
    return response

def getFlow():
    data = []
    meta = getResponse(requestURI + '/surveys/' + survey_id)
    form_url = meta['forms'][0]['formInstancesUrl']
    meta = meta['forms'][0]['questionGroups']
    form_group = pd.DataFrame(meta)
    form_group = form_group[['id','name']].values.tolist()
    meta = pd.DataFrame(meta)
    meta = [pd.DataFrame(meta['questions'][0]),
            pd.DataFrame(meta['questions'][1])]
    sources = getResponse(form_url).get('formInstances')
    for isource, source in enumerate(sources):
        cols = []
        for f_ix, forms in enumerate(form_group):
            for isource in source['responses'][forms[0]]:
                meta_id = meta[f_ix]['id'].tolist()
                var_name = meta[f_ix]['variableName'].tolist()
                rn = {}
                for m_ix, mt_id in enumerate(meta_id):
                    try:
                        rn.update({var_name[m_ix]:isource[mt_id]})
                    except:
                        pass
                cols.append({forms[1]:rn})
        data.append(cols)
    return data
