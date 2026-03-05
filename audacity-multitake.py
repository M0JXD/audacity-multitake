#!/usr/bin/env python3

# TODOS:

# - Can we grab the current looping and/or selection from audacity so we don't need the args?
# - Punch in/out times to avoid recording lead-in garbage that needs cut
# - Single track mode that exports on each take - once done allows you to switch
#   the file "in-place" of the track rather than having a gazillion take tracks

import time, sys
import pipeclient

client = pipeclient.PipeClient()


def minsecs_convert(minsecs):
    minsecs = minsecs.split(":", 1)
    return (int(minsecs[0]) * 60) + int(minsecs[1])


def get_existing_track_amount():
    client.write("GetInfo: Type=Tracks")
    json = ""
    while json == "":
        json = client.read()
    return json.count("name")


if __name__ == "__main__":
    print("===== Audacity MultiTake Helper =====")
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("Specify at least two arguments for the start and end time!")
        exit()

    try:
        if ":" in sys.argv[1]:
            start_time = minsecs_convert(sys.argv[1])
            print(f"Starting at {sys.argv[1]} ({start_time} seconds).")
        else:
            start_time = float(sys.argv[1])
            print(f"Starting at {start_time} seconds.")
        if ":" in sys.argv[2]:
            end_time = minsecs_convert(sys.argv[2])
            print(f"Ending at {sys.argv[2]} ({end_time} seconds).")
        else:
            end_time = float(sys.argv[2])
            print(f"Ending at {end_time} seconds.")

        if len(sys.argv) > 3:
            prefix = sys.argv[3] + " Take "
        else:
            prefix = "Take "
    except:
        print("Arguments could not be converted!")
        exit()

    existing = get_existing_track_amount()
    take_no = 1
    print(f"Detected {existing} existing track(s).")
    print(f"Using prefix name: {prefix}")

    # Select the region to playback
    # We don't actually want to reach the end time so just "set the cursor"
    client.write(f"Select: Start={start_time} End={start_time}")
    print()
    try:
        while True:
            print(f"Recording new track: {prefix + str(take_no)}")
            # Start recording on a new track
            client.write("Record2ndChoice")
            # Wait the time of the take
            # TODO: IDK why we need a different time for the first take?
            time.sleep((end_time - start_time) + (take_no == 1 and 0.7 or 1.1))
            # Stop and reset the cursor
            client.write("PlayStop")
            # Name and mute this track
            client.write(f"Select: Track={existing + take_no - 1}")
            client.write("SetTrackVisuals: Height=50")  # Shrink down previous takes
            client.write("MuteTracks")
            client.write(f'SetTrackStatus: Name="{prefix + str(take_no)}"')
            take_no = take_no + 1

    except KeyboardInterrupt:
        print("\nStopping takes...")
        client.write("Pause")
        client.write("PlayStop")
        client.write("CursSelStart")
        client.write(f"Select: Track={existing + take_no - 1}")
        client.write(f'SetTrackStatus: Name="{prefix + str(take_no)}"')
        print(f"{take_no} takes recorded.")
