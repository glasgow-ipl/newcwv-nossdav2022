

def get_initial_ts(event_log_path):

    with open(event_log_path) as f:
        for line in f:
            if line.startswith('changing BW'):
                time = line.strip().split(' ')[-1].split('-')[-1]
                return time

def get_bw_changes(event_log_path):
    changes = []
    with open(event_log_path) as f:
        for line in f:
            if line.startswith('changing BW'):
                tokens = line.strip().split(' ')
                time = tokens[-1].split('-')[-1]
                bandwidth = float(tokens[2])
                changes.append((time, bandwidth))

    return changes