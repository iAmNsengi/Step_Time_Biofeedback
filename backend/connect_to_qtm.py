"""
Connect to QTM to allow stream of data to come in
"""

import time
from pylsl import StreamInlet, resolve_stream

def stream_data (stream_type= 'Force', sleep_time= 0.1):
    """ 
    Connect to the specified data stream and print data. 
    :param stream_type: Type of the stream to connect to.
    :param sleep_time: Time in seconds to wait between pulling samples. 
    """
    streams = resolve_stream('type', 'Force')

    if not streams:
        print(f"No stream of type '{stream_type}' found.")
        return

    inlet= StreamInlet(streams[0])

    try:
        while True:
            sample, timestamp = inlet.pull_sample()
            print(f"Timestamp: {timestamp}, Sample: {sample}")
            time.sleep(sleep_time)
    except KeyboardInterrupt:
<<<<<<< HEAD
       print("Streaming stopped by user.")
    
    if __name__ == "__main__":
     stream_data()
=======
        print("Streaming stopped by user.")
>>>>>>> origin/main

if __name__ == "__main__":
    stream_data()
