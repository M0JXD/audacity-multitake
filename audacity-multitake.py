import time
import sys
import pipeclient

if __name__ == "__main__":
    print("Audacity MultiTake Helper")
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("Specify at least two arguments for the start and end time!")
        exit()

    try:
        start_time = float(sys.argv[1])
        end_time = float(sys.argv[2])
        if len(sys.argv) > 3:
            preexisting_tracks = int(sys.argv[3])
        else:
            preexisting_tracks = 1
    except:
        print("Arguments could not be converted!")
        exit()

    take_no = 1
    client = pipeclient.PipeClient()

    # Select the region to playback
    # NB: We don't actually wan't to reach the end time so just "set the cursor"
    client.write(f"Select: Start={start_time} End={start_time}")

    try:
        while True:
            # Start recording on a new track
            client.write("Record2ndChoice")
            # Wait the time of the take
            # TODO: IDK why we need a different time for the first take?
            time.sleep((end_time - start_time) + (take_no == 1 and 0.7 or 1.1))
            # Stop and reset the cursor
            client.write("PlayStop")
            client.write("CursSelStart")
            # Name and mute this track
            client.write(f"Select: Track={preexisting_tracks + take_no - 1}")
            client.write("SetTrackVisuals: Height=50")  # Shrink down previous takes
            client.write("MuteTracks")
            client.write(f'SetTrackStatus: Name="Take {take_no}"')
            take_no = take_no + 1

    except KeyboardInterrupt:
        client.write("PlayStop")
        client.write("CursSelStart")
        client.write(f"Select: Track={preexisting_tracks + take_no - 1}")
        client.write(f'SetTrackStatus: Name="Take {take_no}"')
