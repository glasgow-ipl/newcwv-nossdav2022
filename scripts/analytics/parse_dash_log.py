import json


def _get_timestamp(msg_line):
    '''Returns an int value of the first element enclosed in [] from msg_line (typically the timestamp)'''
    return int(msg_line.split(']')[0][1:])


#TODO: For future use it would be helpful to record the start time, now we will reverse engineer it
def get_start_time(dash_log_file):
    '''Returns dashjs' start time timestamp'''
    # Once the manifest is downloaded a timestamp of that is recorded. The log message contains an offset from the original start time.
    with open(dash_log_file) as f:
        dash_log = json.load(f)['eventLog']

    for msg in dash_log:
        if 'Manifest has been refreshed' in msg:
            # The first and last items in that log message are important to us. They are both enclosed in []
            items = msg.split('[')
            offset = float(items[1].strip()[:-1])
            timestamp = float(items[-1].strip()[:-1])

            return timestamp - offset / 1000


def get_client_estimations(dash_log_file):
    ''' Returns a list of tuples containing: a linux timestamp and the client's bandwidth estimation at that point in time'''
    time_estimate = []

    start_time = get_start_time(dash_log_file)
    with open(dash_log_file) as f:
        dash_log = json.load(f)['eventLog']

    for msg in dash_log:
        if 'Average throughput' in msg:
            throughput = float(msg.split('Average throughput ')[1].split()[0]) * 1000
            offset = _get_timestamp(msg)
            timestamp = start_time + offset / 1000
            time_estimate.append((timestamp, throughput))

    return time_estimate


def get_startup_delay(dash_log_file):
    ''' Returns startup delay in milliseconds '''
    with open(dash_log_file) as f:
        dash_log = json.load(f)['eventLog']

    for msg in dash_log:
        if 'Native video element event: playing' in msg:
            return _get_timestamp(msg)


def get_playback_stalls(dash_log_file):
    ''' Returns a list of tuples, containing timestamps of the begining and the end of each stall event'''
    playback_stalls = []

    start_time = get_start_time(dash_log_file)

    with open(dash_log_file) as f:
        dash_log = json.load(f)['eventLog']

    skip = True
    stall_start = None
    for msg in dash_log:
        if 'Native video element event: playing' in msg: 
            if skip:
                # In order to detect stalls, we should first be playing. 
                # Skipping until playing, ensures that we do not account for the start-up delay
                skip = False
                continue
        if skip:
            continue

        if 'Native video element event: waiting' in msg:
            offset = _get_timestamp(msg)
            stall_start = start_time + offset / 1000
        elif 'Native video element event: playing' in msg:
            offset = _get_timestamp(msg)
            stall_end = start_time + offset / 1000
            playback_stalls.append((stall_start, stall_end))

    return playback_stalls


def get_buffer_levels(dash_log_file):
    '''Returns a list of tuples containing: timestamp and the buffer level at that timestamp'''
    buffer_levels = []

    start_time = get_start_time(dash_log_file)

    with open(dash_log_file) as f:
        dash_log = json.load(f)['eventLog']

    for msg in dash_log:
        if 'Buffered range' in msg:
            offset = _get_timestamp(msg)
            tokens = msg.split('Buffered range:')[1].split(',')
            buffer_time_max = float(tokens[0].split('-')[1].strip())
            current_time = float(tokens[1].split('=')[1].strip())
            buffer_level = buffer_time_max - current_time
            timestamp = start_time + offset / 1000
            buffer_levels.append((timestamp, buffer_level))

    return buffer_levels

def get_total_stall_time(dash_log_file):
    ''' Returns a scalar of the total time spent in video stall events in seconds '''
    stalls = get_playback_stalls(dash_log_file)
    total_stall_time = sum([x1 - x0 for x0, x1 in stalls])
    return total_stall_time


if __name__ == '__main__':
    # get_client_estimations('/vagrant/logs/tmp/no_loss/sample/1/1_reno/dashjs_metrics.json')
    # get_startup_delay('/vagrant/logs/tmp/no_loss/sample/1/1_reno/dashjs_metrics.json')
    # get_playback_stalls('/vagrant/logs/tmp/no_loss/sample/1/1_reno/dashjs_metrics.json')
    # get_buffer_levels('/vagrant/logs/tmp/no_loss/sample/1/1_reno/dashjs_metrics.json')
    x = get_total_stall_time('/vagrant/logs/tmp/no_loss/sample/1/1_reno/dashjs_metrics.json')
    print(x)
    