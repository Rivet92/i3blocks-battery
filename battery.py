#!/usr/bin/env python3
#
# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

from subprocess import check_output

status = check_output(['acpi'], universal_newlines=True)

if not status:
    # stands for no battery found
    fulltext = "<span color='red'><span font='FontAwesome'>\uf00d \uf240</span></span>"
    percentleft = 100
else:

    percentleft = 0    
    state = status.split("\n")
    del state[-1]
    timeleft = ""

    for i,line in enumerate(state):
        percentleft += int(float(line.split(", ")[1].rstrip("%")) / (len(state)*100) * 100)
        state[i] = line.split(": ")[1].split(",")[0]
        if len(line.split(", ")) > 2:
            timeleft = line.split(", ")[2].split()[0]
 
    # stands for charging
    FA_LIGHTNING = "<span color='yellow'><span font='FontAwesome'>\uf0e7</span></span>"

    # stands for plugged in
    FA_PLUG = "<span font='FontAwesome'>\uf1e6</span>"

    fulltext = ""
    timeleft_symbol = "-"
    
    if "Discharging" in state or "Charging" in state:
        if percentleft == 100:
            timeleft = " (FULL)"
        else:
            time = ":".join(timeleft.split(":")[0:2])
            timeleft = "{}".format(time)
    
    # At least one battery is full
    if "Full" in state:

        # Full & Charging
        if "Charging" in state or "Unknown" in state:
            fulltext = FA_LIGHTNING + FA_PLUG + " "
            timeleft_symbol = "+"

    # Battery missing/acpi error?
    elif "Unknown" in state:
        fulltext = "<span font='FontAwesome'>\uf128</span> "
    else:
        fulltext = FA_LIGHTNING + FA_PLUG + " "

    def color(percent):
        if percent < 10:
            # exit code 33 will turn background red
            return "#FFFFFF"
        if percent < 20:
            return "#FF0000"
        if percent < 30:
            return "#FF3300"
        if percent < 40:
            return "#FF6600"
        if percent < 50:
            return "#FF9900"
        if percent < 60:
            return "#FFCC00"
        if percent < 70:
            return "#FFFF00"
        if percent < 80:
            return "#CCFF00"
        return "#00FF00"

    form =  '<span color="{}">{}%</span>'
    fulltext += form.format(color(percentleft), percentleft)
    if ":" in timeleft:
        fulltext += " ({}{})".format(timeleft_symbol, timeleft)

print(fulltext)
print(fulltext)
if percentleft < 10:
    exit(33)
