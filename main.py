import requests
import random
import os
from user_agent import generate_user_agent
import pyfiglet
import sys
import time
from ssl import CERT_NONE
from gzip import decompress
from random import choice, choices
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from websocket import create_connection

def clear_screen():
    if os.name == 'nt': 
        os.system('cls')
    else:  
        os.system('clear')



def to(s):
    for char in s + "\n":
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(1)


failed = 0
success = 0
retry = 0
accounts = []


def work():
    global failed, success, retry
    username = choice('qwertyuiooasdfghjklzxcvpbnm') + ''.join(choices(list('qwertyuioasdfghjklzxcvbnpm1234567890'), k=16))
    password = "hmmm" 
    try:
        con = create_connection("wss://195.13.182.213/Auth",
                                header={"app": "com.safeum.android", "host": None, "remoteIp": "195.13.182.213",
                                        "remotePort": str(8080), "sessionId": "b6cbb22d-06ca-41ff-8fda-c0ddeb148195",
                                        "time": "2024-04-11 11:00:00", "url": "wss://51.79.208.190/Auth"},
                                sslopt={"cert_reqs": CERT_NONE})
        con.send(dumps(
            {"action":"Register","subaction":"Desktop","locale":"en_GB","gmt":"+05","password":{"m1x":"f8651d14949a88946be818a2fdf6bd9c2192c37394746a81a83d086237247185","m1y":"fa091fc28ef66e4857250c28363dcea0a93b35ae1bb4c0e7251ac6554c83b5f1","m2":"7e5003e3f7c51d334123544f6d65080f5c319b70c4519a3cbfa5b80fb94d4ebd","iv":"62624b7bd54fb5a0e81ca6f29704e255","message":"8a8a6f99a3710bad7b7a47c1d830c1d09fbd2ce01051644ddf2c1ea17704b5f489059e41d874fdd9cd36937059eab114acf0bff3a0b065f02a4038f57dd62e36bb25f20bc06955c8f6f669bdfaa8070f"},"magicword":{"m1x":"7d041f54ab8ce9cfc91a1d90599d7cc8fbe30954a89d7994a2d2b628427a7659","m1y":"b876e3b430cac21ae4aec9f1a0bbc78719154c9686e5dd99e652547880124a6f","m2":"435ac500a2a86e82f0e905988bbafc6b59838c5f8a7f5d6416e5deba2c7b7a01","iv":"c999901ed1360bbeb24e335c1a6c1ec4","message":"f13ec29621da646d1a0e9499494d9ad9"},"magicwordhint":"0000","login":str(username),"devicename":"Xiaomi 23106RN0DA","softwareversion":"1.1.0.2300","nickname":"u76sms","os":"AND","deviceuid":"7796efb323b2256e","devicepushuid":"*f6rehHZJStaTuXzjS1BZ3f:APA91bHt3rJ-fQT5U22jN0mGnVF4kx7M9efj2KsX9jx4VyqjG_rHaX_lbLs9xB5ayur0TCm_xTzgX30uBYkgpiz7cpR6ecDCtgFNPv7_hXtc9y9eyAYQUzPrEAoW3bfbJ0O04Q8ynbT7","osversion":"and_14.0.0","id":"1634706399"}))
        gzip = decompress(con.recv()).decode('utf-8')
        if '"status":"Success"' in gzip:
            success += 1
            b = accounts.append(username + ':' + password)
            print(b)
            with open('SafeUM.txt', 'a') as f:
                f.write(username + ":" + password + "\n")

        else:
            failed += 1
    except:
        retry += 1


start = ThreadPoolExecutor(max_workers=10000)


while True:
    start.submit(work)
    print('\n\n\n' + ' ' * 25 + 'Success : ' + str(success) + '\n\n\n' + ' ' * 25 + 'Failed : ' + str(
        failed) + '\n\n\n' + ' ' * 25 + 'ReTry : ' + str(retry))
    hh = str(failed) + str(success) + str(retry)
    if int(success) >= 2000:
        print("Created Acc successfully")
        
    
    if int(success) > int(0):
        z = "\n".join(accounts)
        
        print("CREATED ACCOUNTS>>\n", z)
        

    clear_screen()
