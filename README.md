# Audacity Multi-Take Helper

A small and simple helper utility to implement the one killer feature I'm missing in Audacity:
A hands free loop recorder to make multiple takes without needing to take my hands away from my
instrument.

NB: To get the best use of this you should set your [latency compensation](https://support.audacityteam.org/troubleshooting/solving-recording-problems/latency-compensation).

## Usage

Make sure [Python](https://www.python.org/downloads/) is installed and enable
[mod-script-pipe](https://manual.audacityteam.org/man/scripting.html#Enable_mod-script-pipe)
in Audacity.

After that it's pretty dang simple! While Audacity is already running,
launch the script from a terminal providing the start and end times for your loop region:

`python audacity-multitake.py 02:05 04:32 2.0 Guitar`

NB: `python` might be `py` on Windows or `python3` on some Linux distros.

The last two arguments are optional.
In the example, `2.0` is the new gain to apply and `Guitar` is the prefix name for the tracks.
If you don't want to apply a new gain but need a prefix pass `0` as the third argument.

Audacity will start recording new tracks (using the channel setting from `Recording Channels`),
and after each one is done, the track is named and muted before starting the next.

When you're done, hit `Ctrl-C` on the script and it will stop. You may need to cancel the current recording from Audacity.
