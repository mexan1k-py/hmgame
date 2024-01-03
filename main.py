#🌲🌊❤️🔥🏣☁️🟩🚁🏢⚡️🛢️🏆

from map import Map
import time
import os
import json
from helicopter import Hellicopter as Hellico
from pynput import keyboard
from clouds import Clouds

TICK_SLEEP = 0.05
TREE_UPDATE = 50
FIRE_UPDETE = 50
MAP_W, MAP_H = 20, 10
CLOUDS_APDATE = 100

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
hellico = Hellico(MAP_W, MAP_H)
tick = 1

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0,-1)}
# f - save, g - startsave
def process_key(key):
    global hellico, tick, clouds, field
    c = key.char.lower()
    # обработка движения вертолета
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        hellico.move(dx, dy)
    # сохранение игры
    elif c == 'f':
        data = {'hellicopter': hellico.export_data(),
                'clouds': clouds.export_data(),
                'field': field.export_data(),
                'tick': tick}
        with open('level.json', 'w') as lvl:
            json.dump(data, lvl)
    elif c == 'g':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            tick = data['tick'] or 1
            hellico.import_data(data['hellicopter'])
            field.import_data(data['field'])
            clouds.import_data(data['clouds'])


listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()

while True:
    os.system('CLEAR')
    field.process_helicopter(hellico, clouds)
    hellico.print_stats()
    field.print_map(hellico, clouds)
    print('TICK', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDETE == 0):
        field.update_fires()
    if (tick % CLOUDS_APDATE == 0):
        clouds.update_clouds()