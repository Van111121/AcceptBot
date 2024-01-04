from lcu_driver import Connector
import os
import keyboard
import time
from sys import exit
import datetime

vnnn = Connector()

#LCU API code
@vnnn.ready
async def connect(connection):
    timer = 0
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    os.system('cls')
    while True:
        second = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
        first = await second.json()
        if first == 'Lobby' or first == 'Matchmaking':
            await connection.request('post', '/lol-lobby/v2/lobby/matchmaking/search')
            while True:
                print('Waiting sa Queue')
                print(str(datetime.timedelta(seconds=timer)))
                timer += 1
                print('Click ESC to cancel or Click the X ')
                time.sleep(1)
                second = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
                first = await second.json()
            
                if keyboard.is_pressed('esc' or 'x'):
                    exit()
                os.system('cls')
                
                
                if first == 'ReadyCheck':
                    await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')
                    print("Match has been accepted!")
                    time.sleep(3)

#quit when apps closed or cilent 
@vnnn.close
async def disconnect(_):
    await vnnn.stop()

#start code
vnnn.start()
