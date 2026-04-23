import minescript as m
from minescript import EventQueue, EventType
import time
import threading
import random
import sys

toggle = False
do_click = True
fish_caught = 0

FISH_NAME = "!!!"
FISH_SLOT = 0
CLICK_SLOT = 2

def human_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def nearest_fish():
    ents = m.entities(sort="nearest", limit=None, min_distance=0.5, max_distance=15)
    for e in ents:
        if e.name == FISH_NAME:
            return e
    return None

def fish_once():
    global fish_caught

    m.player_inventory_select_slot(FISH_SLOT)
    human_delay(0.03, 0.08)

    m.player_press_use(True)
    human_delay(0.03, 0.08)
    m.player_press_use(False)
    human_delay(0.12, 0.18)
    m.echo("§aCasting rod...")

    while True:
        fish = nearest_fish()
        if fish:
            human_delay(0.15, 0.3)
            m.player_press_use(True)
            human_delay(0.03, 0.08)
            m.player_press_use(False)

            fish_caught += 1
            m.echo(f"§bFish caught! Total: {fish_caught}")

            if do_click:
                m.player_inventory_select_slot(CLICK_SLOT)
                human_delay(0.1, 0.25)
                m.player_press_use(True)
                human_delay(0.03, 0.06)
                m.player_press_use(False)
                m.echo(f"§eRight-clicked slot {CLICK_SLOT} after reel.")

            break

        human_delay(0.03, 0.06)

def key_listener():
    global toggle, do_click
    with EventQueue() as eq:
        eq.register_key_listener()
        while True:
            event = eq.get()
            if event.type == EventType.KEY:
                if event.action == 1 and event.key == 295:
                    toggle = not toggle
                    m.echo(f"§7§oFishing toggle: {toggle}")
                    if not toggle:
                        m.echo(f"§b§nFish caught: §6{fish_caught}")

                elif event.action == 1 and event.key == 296:
                    do_click = not do_click
                    m.echo(f"§7§oSlot 2 click: {do_click}")

def main():
    m.echo("§d§l- Fishing Script by 莫阿兹/fobiscool and 去你的/allthemighty_-§r")
    time.sleep(0.5)

    threading.Thread(target=key_listener, daemon=True).start()
    m.echo("§d§l-Fishin' time- §7§o~(F6 toggle, F7 to turn off attacking!)")

    while True:
        if toggle:
            fish_once()
            human_delay(0.1, 0.2)
        else:
            time.sleep(0.05)

main()
