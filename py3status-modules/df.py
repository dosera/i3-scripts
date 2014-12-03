from subprocess import check_output
from collections import OrderedDict
from time import time
from os import system

# This module for Py3status (i3status wrapper) allows activation
# and deactivation of DPMS (Display Power Management Signaling)
# by clicking on 'DPMS' in the status bar.
# For more information read:
# i3wm homepage: http://i3wm.org
# py3status homepage: https://github.com/ultrabug/py3status
# ----------------------------------------------------------------- #
# Notes:
# 1. 'df' is used to receive the device usage.
#
# Written and contributed by
#        Andre Doser <dosera AT gmail.com>


class GetData():
    def __init__(self):
        # each element in the list with its displayed name
        # for example to display the size of / as sys just add
        #       '/' : 'sys'
        self.devices = {'/': 'sys', '/home': 'home'}

    def get_disk_info(self):
        """
        Collect the info of the discs.

        :returns: lexicographically ordered dict containing the usage.
        """
        df = check_output('df').decode('utf-8').split('\n')[:-1]
        result = {}
        for el in df:
            els = el.split()
            if els[5] in self.devices:
                result[self.devices[els[5]]] = round(float(els[2]) /
                                                     float(els[1]) * 100, 1)
        return OrderedDict(sorted(result.items()))


class Py3status:
    def space(self, i3status_output_json, i3status_config):
        result = {
            'name': 'df',
            'cached_until': time() + 60
        }
        disk_info = GetData().get_disk_info()
        s = ''
        for i, dev in enumerate(disk_info.keys()):
            s += dev + ': ' + str(disk_info[dev]) + '%'
            # spaces except last one
            if i < len(disk_info) - 1:
                s += ' '
            # critical if > 90%
            if disk_info[dev] > 90:
                result['color'] = i3status_config['color_bad']

        result['full_text'] = s
        return (0, result)

    def on_click(self, json, i3status_config, event):
        """
        Start Thunar on click.
        """
        if event['button'] == 1:
            system('spacefm')
