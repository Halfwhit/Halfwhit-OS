#!/usr/bin/python3

import keyboard
import os
import sys
from pyautogui import keyDown, keyUp
from time import sleep


def main():
    if os.getuid() != 0:
        os.execvp('sudo', ['sudo', sys.executable, *sys.argv])
    print("At any point press ctrl+alt+m to terminate this script")
    keyboard.add_hotkey('ctrl+alt+m', forceClose)
    cargo = input("Enter current cargo capacity (e.g. 1200): ")
    batch = input("Enter the batch size to sell: ")
    cargo_int = int(cargo)
    batch_int = int(batch)
    sale_loops = int(cargo_int / batch_int)
    if cargo_int % batch_int > 0:
        sale_loops = sale_loops + 1
    print("Number of batches to sell:", sale_loops)
    startTimer()
    sell(sale_loops, cargo_int, batch_int)

def forceClose():
    print("\nScript stopped by user\n\n")
    os.system("pkill -f ED-Script-Batch-Sell.py")

def startTimer():
    print("Focus the Elite Dangerous window, and have the item to be sold highlighted in the commodities market ready to go.\nYou have 10 seconds...")
    print("Starting..", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
        sleep(1)
    print(" Now!")
    sleep(1)

def sell(sale_loops, cargo_int, batch_int):
    for i in range(0, sale_loops):
        press('space')
        sleep(5)
        if i == 0:
            # Reset UI
            press('a')
            press('a')
            press('a')
            press('s')
            press('s')
            press('w')
        press('w')
        keyDown('a')
        sleep(3)
        keyUp('a')
        sleep(0.1)
        for j in range(0, batch_int):
            press('d')
        press('s')
        press('space')
        print("Batch sold. That's {} out of {} in total!".format(i+1, sale_loops))
        sleep(5)
    print("Finished selling {} units!".format(cargo_int))

def press(key):
    keyDown(key)
    sleep(0.05)
    keyUp(key)
    sleep(0.05)

if __name__ == "__main__":
    main()
