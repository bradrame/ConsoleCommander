import subprocess
import time
import pygetwindow as gw

def setup_browser(screen_width, screen_height):
    browser = gw.getWindowsWithTitle('edge')
    if browser:
        browser = browser[0]
        browser.restore()
        browser.resizeTo(
            int(screen_width * 0.5079),
            int(screen_height * 0.9624)
        )
        browser.moveTo(0 - 7, 0)
    else:
        try:
            subprocess.Popen(['start', 'msedge'], shell=True)
            time.sleep(1)
            setup_browser(screen_width, screen_height)
        except Exception as e:
            print(e)

def get_tab():
    active_tab = gw.getWindowsWithTitle('edge')[0].title.split(' - Personal')[0].split(' and')[0]
    return active_tab

def setup_ide(screen_width, screen_height):
    ide = gw.getWindowsWithTitle('.py')
    if ide:
        ide = ide[0]
        ide.restore()
        ide.resizeTo(
            int(screen_width * 0.5078),
            int(screen_height * 0.9624)
        )
        ide.moveTo(int(screen_width / 2) - 7, 0)