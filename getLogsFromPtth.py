import argparse
from   datetime        import datetime, timedelta
from   glob            import glob
import json
from   lxml            import html
from   multiprocessing import Pool
import os
import requests
from   shutil          import copyfileobj, move
from   time            import sleep

# Takes log URL and server data, and downloads the logs.
def downloadServerLogs(m, name, logsLen, n, serverName, namesLen, serverHeaders, args):
    logData = [None,None]
    while(not logData[1] or logData[1].status_code != 200):
        try:
            logData = (name, requests.get(''.join(name), stream = True, headers = serverHeaders))
        except (ConnectionError,TimeoutError,requests.exceptions.ConnectionError) as e:
            print(F"ERROR:  {e}\n  {type(e)} in:  {''.join(name)}")
            sleep(3)
    
    print(F"\n{n + 1:>{len(str(namesLen))}}/{namesLen} | {m + 1:>{len(str(logsLen))}}/{logsLen}")
    print(F"\tDownloading {serverName[0]}/{serverName[1]}/{serverName[1]}_{logData[0][1]} ...", end = '')
    
    try:
        logData[1].raw.decode_content = True
        with open(F"{args.dataFolder}/{serverName[0]}/{serverName[1]}/{serverName[1]}_{logData[0][1][2:]}", 'wb') as f:
            copyfileobj(logData[1].raw, f)
    except IOError as e:
        print(F"ERROR\nERROR:  {e}\n  Error saving:  {args.dataFolder}/{serverName[0]}/{serverName[1]}/{serverName[1]}_{logData[0][1]}")
    else:
        print("complete")
    
    return

# Gets URLs to logs in servers, formats the data, and calls a function to download the logs.
def getServerLogs(n, serverName, baseURL, namesLen, serverHeaders, dateBegin, args, url):
    try:
        response = requests.request('GET', url, headers = serverHeaders)
    except requests.exceptions.ConnectionError as e:
        print(F"ERROR:  {e}\n  ConnectionError in:  {n}/{namesLen}:  {serverName}, {baseURL}")
    except requests.exceptions.ChunkedEncodingError as e:
        print(F"ERROR:  {e}\n  ChunkedEncodingError in:  {n}/{namesLen}:  {serverName}, {baseURL}")
    else:
        tree           = html.fromstring(response.content)
        allLinks       = tree.xpath('//a[@class="entry"]/@href')
        
        existingLogs = [os.path.basename(x) for x in glob(F"{args.dataFolder}/**/*.txt", recursive=1)]
        
        logNames     =  [
                            (url, link) for link in allLinks if
                                link.endswith('.txt')                                 and
                                datetime.strptime(link[2:12], "%Y_%m_%d") >= dateBegin and
                                (F"{serverName[1]}_{link}" not in existingLogs or datetime.strptime(link[2:12], "%Y_%m_%d") >= datetime.today() - timedelta(days = 1))
                        ]
        
        logsLen = len(logNames)
        print(F"{n + 1:>{len(str(namesLen))}}/{namesLen} : {logsLen}")
        if(logsLen > 0):
            # download logs
            for m, name in enumerate(logNames):
                downloadServerLogs(m, name, logsLen, n, serverName, namesLen, serverHeaders, args)
    
    return

# Sends a request to retrieve server data.
# Returns a list of server names which contain the substring defined in the "server" variable.
def getServerNames(serversURL, serverHeaders, siteData, args):
    print("Getting server data...")
    
    payload     = {}
    response = None
    while(not response or response.status_code != 200):
        try:
            response = requests.request("GET", serversURL, headers = serverHeaders, data = payload)
        except ConnectionError as e:
            print(F"ERROR:  {e}\n  ConnectionError in servers.")
            sleep(3)
        except TimeoutError as e:
            print(F"ERROR:  {e}\n  TimeoutError in servers.")
            sleep(3)
        except requests.exceptions.ConnectionError as e:
            print(F"ERROR:  {e}\n  ConnectionError in servers.")
            sleep(3)
    
    serverNames = [x['name'] for x in json.loads(response.text)['servers'] if any([name in x['name'] for name in args.servers])]
    print(len(serverNames))
    with open(F"{args.dataFolder}/server_data.json", 'w') as f:
        f.write(response.text)

    for n,x in enumerate(serverNames):
        for y in siteData:
            if(x in y['sensors']):
                serverNames[n] = [y['name'].strip(), x.strip()]
                if(not os.path.exists(F"{args.dataFolder}/{y['name'].strip()}/{x.strip()}")):
                    os.makedirs(F"{args.dataFolder}/{y['name'].strip()}/{x.strip()}")
                
                break
        
        if(len(serverNames[n]) != 2 or x[1] == ''):
            serverNames[n] = ['NOSITE', x.strip()]
    
    return serverNames

def getSiteData(sitesURL, siteHeaders, args):
    print("Getting site data...")
    
    payload     = {}
    response    = requests.request("GET", sitesURL, headers = siteHeaders, data = payload)

    data        = json.loads(response.text)['sites']
    print(len(data))
    
    with open(F"{args.dataFolder}/site_data.json", 'w') as f:
        f.write(response.text)

    for site in data:
        for sensor in site['sensors']:
            if(not os.path.exists(F"{args.dataFolder}/{site['name'].strip()}/{sensor.strip()}")):
                os.makedirs(F"{args.dataFolder}/{site['name'].strip()}/{sensor.strip()}")

    return data

def makeParser():
    parser = argparse.ArgumentParser(description='Process ptth log download options')
    '''
    parser.add_argument('', '-', '--',
                        action='',
                        const=,
                        default=,
                        help='',
                        nargs=1,
                        required=False,
                        type=,)
    '''
    
    parser.add_argument('-f', '--folder',
                        default="./ptthLogs",
                        dest='dataFolder',
                        help='Folder location to store the logs.',
                        type=str,)
    
    parser.add_argument('-s', '--servers',
                        default=[''],
                        dest='servers',
                        help='List of substrings to check server names against.',
                        nargs='+',
                        type=str,)
    
    parser.add_argument('-d', '--date',
                        default="2000-01-01",
                        dest='dateStart',
                        help='Earliest log date to download.',
                        type=str,)
    
    return parser

def main():
    parser = makeParser()
    args   = parser.parse_args()
    print(args)
    
    servers = args.servers
    
    dateBegin           = datetime.fromisoformat(args.dateStart)
    
    baseURL             = F"https://vstalert-update.com/ptth/scraper/v1"
    serversURL          = F"{baseURL}/server_list"
    sitesURL            = r"https://data.vstalert.com/Sync/GetAllBranchesAndSensors"

    serverHeaders       = {
        'X-ApiKey': 'bony lend plaza used crave clink nap blush patio talon'
    }
    siteHeaders         = {
        'X-ApiKey': 'a832bf3d-26af-4397-a750-bf718369dee0'
    }
    
    try:
        os.makedirs(args.dataFolder)
    except IOError:
        pass
    
    siteData    = getSiteData(sitesURL, siteHeaders, args)
    serverNames = getServerNames(serversURL, serverHeaders, siteData, args)
        
    namesLen            = len(serverNames)
    getServerAlertLogsInputs =   [
                                (
                                    n,
                                    serverName,
                                    baseURL,
                                    namesLen,
                                    serverHeaders,
                                    dateBegin,
                                    args,
                                    F"{baseURL}/server/{serverName[1]}/files/VST_SD/curlLog/",
                                )
                                for n, serverName in enumerate(serverNames)
                            ]
    
    print(F"Downloading since date: {dateBegin.isoformat()}")
    '''
    for x in getServerLogsInputs:
        getServerLogs(*x)
    '''
    with Pool() as pool:
        pool.starmap(getServerLogs, getServerAlertLogsInputs)
        pool.close()
        pool.join()
    
    
        
    return

if(__name__ == '__main__'):
    #cProfile.run('main()')
    main()
