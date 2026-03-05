# Audacity Multi-Take Helper

A small and simple helper utility to implement the one killer feature I'm missing in Audacity.
A hands free loop recorder to make multiple takes without needing to take my hands away from my
instrument.

## Usage

Pretty dang simple! While Audacity is already running, launch the script telling it the start and
end times for your loop region:

`python audacity-multitake.py start_time end_time prefix`

Prefix is optional. Audacity will start recording new tracks (with the amount of channels you've set
under `Recording Channels`), and when each one is done, the script names and mutes the track
before making the next one to record.

When you're done, hit `Ctrl-C` on the script and it will stop recording.
