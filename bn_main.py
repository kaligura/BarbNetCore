import os
import time
from pyfiglet import figlet_format
from simple_term_menu import TerminalMenu
from termcolor import colored
from icmplib import ping
import configparser
import requests

logo = ((colored(figlet_format('BarbNet'), color='green')))

def core_connection():
    try:
        _ = requests.get('http://www.google.com/', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def config_reader():
    config = configparser.ConfigParser()
    config.read('config.ini')
    global sensors
    sensors = dict(config.items("SensorIPs"))
    return sensors

def con_check(ip):
    global con_stat
    host = ping(ip, count=2, timeout=1)
    if host.is_alive:
        con_stat = colored('Online', 'green')
    else:
        con_stat = colored('Offline', 'red')

    return con_stat

def sensor_net():
    os.system('clear')
    print('Initializing sensor network')
    time.sleep(5)
    return


def mqtt_net():
    os.system('clear')
    print('Initializing MQTT network')
    time.sleep(5)
    return


def status():
    os.system('clear')
    print(str(logo))
    status_logo = colored('Systems Status', 'yellow')
    print(status_logo)
    print()
    core_connection()
    core_on  = colored('Online', 'green')
    core_off = colored('Offline', 'red')
    if core_connection():
        print('| {0:<10s}  '.format('BarbNetCore'))
        print('| {0:<10s}  '.format(core_on))
    else:
        print('| {0:<10s}  '.format('BarbNetCore'))
        print('| {0:<10s}  '.format(core_off))

    config_reader()
    for name, ip in sensors.items():
        con_check(ip)
        pname = name.capitalize()
        print()
        print('| {0:<10s} '.format(pname))
        print('| {0:<10s} '.format(con_stat))
        print()

    input()
    os.system('clear')
    return


def main():
    os.system('clear')
    print(str(logo))

    main_menu_title = "  BarbNet Systems \n"
    main_menu_items = ["Initialize Sensor Net", "Initialize MQTT Net", "BarbNet Status", "Deactivate Sensor Net",
                       "Deactivate MQTT Net", "Quit"]
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(menu_entries=main_menu_items,
                             title=main_menu_title,
                             menu_cursor=main_menu_cursor,
                             menu_cursor_style=main_menu_cursor_style,
                             menu_highlight_style=main_menu_style,
                             cycle_cursor=True,
                             clear_screen=False)

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            os.system('clear')
            sensor_net()

        if main_sel == 1:
            os.system('clear')
            mqtt_net()

        if main_sel == 2:
            os.system('clear')
            status()

        if main_sel == 3:
            os.system('clear')
            sensor_net()

        if main_sel == 4:
            os.system('clear')
            mqtt_net()

        if main_sel == 5:
            os.system('clear')
            raise SystemExit


main()
