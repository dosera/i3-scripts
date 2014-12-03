from os import system

# This module for Py3status (i3status wrapper) allows activation
# and deactivation of DPMS (Display Power Management Signaling)
# by clicking on 'DPMS' in the status bar.
# For more information read:
# i3wm homepage: http://i3wm.org
# py3status homepage: https://github.com/ultrabug/py3status
# ----------------------------------------------------------------- #
# Notes:
# 1. 'xset' is used to change the DPMS status.
# 
# Written and contributed by
#        Andre Doser <dosera AT gmail.com>


class Py3status:
    # Check whether 'dpms' is currently enabled or not.
    def __init__(self):
        self.run = system('xset -q | grep -iq "DPMS is enabled"') == 0

    def dpms(self, i3status_output_json, i3status_config):
        """
        :returns: dpms-status in the bar in
            - color_good, if DPMS is active
            - color_bad, if DPMS is inactive
        """
        result = {
            'full_text': 'DPMS',
            'name': 'dpms'
        }
        if self.run:
            result['color'] = i3status_config['color_good']
        else:
            result['color'] = i3status_config['color_bad']
        return (1, result)

    def on_click(self, json, i3status_config, event):
        """
        Handles click events. When clicking,
        'DPMS' is toggled.
        """
        if event['button'] == 1:
            if self.run:
                self.run = False
                system("xset -dpms")
            else:
                self.run = True
                system("xset +dpms")
            system("killall -USR1 py3status")
