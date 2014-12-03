from time import time
import subprocess
import re

# This module for Py3status (i3status wrapper) displays
# the current volume in percent using amixer.
# For more information read:
# i3wm homepage: http://i3wm.org
# py3status homepage: https://github.com/ultrabug/py3status
# ----------------------------------------------------------------- #
# Notes:
# 1. 'amixer' is used to get the volume in percent.
# 
# Written and contributed by
#        Andre Doser <dosera AT gmail.com>

class GetData:
    """
    Get the required volume data.

    :returns: The volume in percent.
    """
    def getVolume(self):
        # run amixer in shell to get the volume percentage
        ps = subprocess.Popen('amixer get Master', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        comm = ps.communicate()[0].decode()
        if re.findall(r'.*\[(.*)\]', comm)[0] == 'on':
            return int(re.findall(r'.*Mono:.*\[(\d*)\%\]', comm)[0])
        else:
            return 0


class Py3status:
    """
    Output the volume to the py3status bar.
    """
    def volume(self, i3status_output_json, i3status_config):
        CACHE_TIMEOUT = 6000
        curr_vol = GetData().getVolume()
        # set, cache and return the output
        response = {'full_text': '♪: ' +
                    str(curr_vol) + '%', 'name': 'curr_volume'}
        response['cached_until'] = time() + CACHE_TIMEOUT

        if curr_vol == 0:
            response['color'] = i3status_config['color_degraded']
        return (6, response)
