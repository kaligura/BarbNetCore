# !/usr/bin/python
# -*- coding:utf-8 -*-

"""BarbNetCore Menu"""
"""Simple configuration tool. Finished 17.08.2020"""

import configparser
import io
import logging
import os
import time
from pathlib import Path

import termcolor
from colorama import init
from getch import getch, pause
from pyfiglet import Figlet, print_figlet, figlet_format
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from simple_term_menu import TerminalMenu
from termcolor import cprint, colored

logo = ((colored(figlet_format('BarbNet'), color='green')))


def config_print():
    os.system('clear')
    print(str(logo))
    config = configparser.ConfigParser()
    config.read('config.ini')
    testmode = config.get('SensorVals', 'testmode')
    refresh = config.get('SensorVals', 'refresh')
    tm_enabled = colored('enabled', 'red')
    tm_disabled = colored('disabled', 'green')
    print()
    if testmode == '1':
        print('Testmode is ', str(tm_enabled))
    else:
        print('Testmode is ', str(tm_disabled))
    print('Refresh rate: ', str(refresh))
    print()
    pause('Press any key to return')
    main()


def configuration():
    os.system('clear')
    print(str(logo))
    config = configparser.ConfigParser()
    config.read('config.ini')
    testmode = config.get("SensorVals", "testmode")
    refresh = config.get("SensorVals", "refresh")

    config_menu_title = " BarbNet Configuration Menu\n"
    config_menu_items = ["Testmode  ", "Sensor refresh rate ", "Back"]
    config_menu_cursor = "> "
    config_menu_cursor_style = ("fg_red", "bold")
    config_menu_style = ("bg_red", "fg_yellow")
    config_menu_exit = False

    config_menu = TerminalMenu(menu_entries=config_menu_items,
                               title=config_menu_title,
                               menu_cursor=config_menu_cursor,
                               menu_cursor_style=config_menu_cursor_style,
                               menu_highlight_style=config_menu_style,
                               cycle_cursor=True,
                               clear_screen=-False)
    while not config_menu_exit:
        config_sel = config_menu.show()
        if config_sel == 0:
            while not config_menu_exit:

                if testmode == '1':
                    os.system('clear')
                    print("Testmode is currently enabled\n")
                    pause('Press any key to disable')
                    myfile = Path('config.ini')
                    config.read(myfile)
                    config.set('SensorVals', 'testmode', '0')
                    config.write(myfile.open("w"))
                    os.system('clear')
                    print("Testmode disabled")
                    pause()
                    configuration()

                if testmode == '0':
                    os.system('clear')
                    print("Testmode is currently disabled\n")
                    pause('Press any key to enable')
                    myfile = Path('config.ini')
                    config.read(myfile)
                    config.set('SensorVals', 'testmode', '1')
                    config.write(myfile.open("w"))
                    os.system('clear')
                    print("Testmode enabled")
                    pause()
                    configuration()

        if config_sel == 1:
            while not config_menu_exit:
                os.system('clear')
                print("Current sensor refresh rate is ")
                print(str(refresh))
                print()
                pause('Press any key to override refresh rate\n')
                os.system('clear')
                refresh = input('Enter new refresh rate: ')
                myfile = Path('config.ini')
                config.read(myfile)
                config.set('SensorVals', 'refresh', refresh)
                config.write(myfile.open("w"))
                pause()
                configuration()
        if config_sel == 2:
            os.system('clear')
            main()


def main():
    os.system('clear')
    print(str(logo))

    main_menu_title = "  BarbNet Systems \n"
    main_menu_items = ["Configuration", "Quit"]
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

    edit_menu_title = "  Configuration\n"
    edit_menu_items = ["Edit Config", "Show Current Config", "Back to Main Menu"]
    edit_menu_back = False
    edit_menu = TerminalMenu(edit_menu_items,
                             edit_menu_title,
                             main_menu_cursor,
                             main_menu_cursor_style,
                             main_menu_style,
                             cycle_cursor=True,
                             clear_screen=False)

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not edit_menu_back:
                os.system('clear')
                print(str(logo))
                edit_sel = edit_menu.show()
                if edit_sel == 0:
                    configuration()
                elif edit_sel == 1:
                    config_print()
                elif edit_sel == 2:
                    edit_menu_back = True

            edit_menu_back = False
        elif main_sel == 1:
            os.system('clear')
            raise SystemExit


if __name__ == "__main__":
    main()
