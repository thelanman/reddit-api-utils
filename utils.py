#!/usr/bin/env python

import json
import urllib2
import datetime
import time

import requests
import requests.auth
    
requests.packages.urllib3.disable_warnings()    


def obj_to_csv(obj, keys, getter=lambda o,k: o[k], fn=None):
    '''
    getter : func : must accept (obj, key) as parameters e.g. lambda o, k: o[k]
    '''
    def get_line(o):
        try:
            return ','.join([str(getter(o, k)) for k in keys]) + '\n'
        except:
            return ''
    if type(obj) is not list:
        obj = [obj]
    out = ','.join(keys) + '\n'
    if fn is None:
        for o in obj:
            out += get_line(o)
    elif type(fn) is str:
        with open(fn, 'w') as f:
            f.write(out)
            for o in obj:
                f.write(get_line(o))
    elif type(f) is file:
        if 'a' not in file.mode:
            f.write(out)
        for o in obj:
            f.write(get_line(o))    
    if fn is None:
        return out


def get_token(client_id, secret_key, username, password):
    client_auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": "analysis-suite-client/0.1 by lanj88"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()


def get_saved(un, token, jdata=None):
    after = ''
    prev_keys = [c['data']['id'] for c in jdata['data']['children']] if jdata is not None else []
    while after is not None:
        headers = {"Authorization": "bearer %s" % token['access_token'], "User-Agent": "analysis-suite-client/0.1 by lanj88"}
        response = requests.get("https://oauth.reddit.com/user/%s/saved?limit=75&after=%s" % (un, after), headers=headers)
        j = response.json()
        after = j['data']['after']
        if jdata is None:
            jdata = j
        else:
            for c in j['data']['children']:
                if c['data']['id'] not in prev_keys:
                    jdata['data']['children'] += [c]
        time.sleep(1.1)
        if len(jdata['data']['children']) > 301:
            break
    return jdata


if __name__ == '__main__':
    import ConfigParser
    
    config = ConfigParser.ConfigParser()
    config.read('api.conf')
    jdata = None
    with open('saved_data.txt', 'r') as f:
        old_data = f.read()
        if old_data != '':
            jdata = json.loads(old_data)
    token = get_token(config.get('global', 'client_id'), config.get('global', 'secret_key'), config.get('global', 'username'), config.get('global', 'password'))
    data = get_saved(config.get('global', 'username'), token, jdata)
    with open('saved_data.txt', 'w') as f:
        json.dump(data, f)
    obj_to_csv(data['data']['children'], ['title', 'subreddit', 'permalink', 'num_comments', 'url', 'created_utc', 'created'], lambda o,k: o['data'][k], 'saved2.csv')
            
    