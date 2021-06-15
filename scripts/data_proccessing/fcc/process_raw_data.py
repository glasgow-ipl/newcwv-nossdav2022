import pandas as pd
import json

headers = [ 'unit_id', 'dtime', 'target', 'downthrpt', 'downjitter',
 'latency', 'jitter', 'buffer_underruns', 'buffer_delay',
  'buffer_filltime', 'duration', 'bitrate', 'buffer_size', 'successes', 'failures', 'location_id']

df = pd.read_csv('/vagrant/network_models/fcc/curr_videostream_2014_05.csv', names=headers)


d2 = df.query('downthrpt < 1_500_000 and downthrpt != 0 ') # We need ~14Mbps to support 1080p HD video, filter reports over 15; and reports that show 0Mbps link speed

print(f'Filtered out {(len(df)-len(d2))/len(df):.3f} % of the data')

targets = set(d2['target'])

profile_template = {
    "changes": [
        {"time": 0, "bw": 1.5, "rtt": 200, "loss": 0.12},
        {"time": 30, "bw": 2, "rtt": 176, "loss": 0.09},
        {"time": 60, "bw": 3, "rtt": 150, "loss": 0.06},
        {"time": 90, "bw": 4, "rtt": 100, "loss": 0.08},
        {"time": 120, "bw": 5, "rtt": 76, "loss": 0.09},
        {"time": 150, "bw": 4, "rtt": 100, "loss": 0.08},
        {"time": 180, "bw": 3, "rtt": 150, "loss": 0.06},
        {"time": 210, "bw": 2, "rtt": 176, "loss": 0.09}
        ],
    "repeat": "True",
    "pause": 30,
    "duration": 640
}

for target_idx, t in enumerate(targets):
    temp = d2.query("target == @t")
    if len(temp) < 8: # We may not have enough data for some of the targets
        print(f'skipping {t}')
        continue

    profile_samples = temp.sample(n=8, random_state=42) # random_state will always select same 8 sample points
    changes = []
    for i, (_, sample) in enumerate(profile_samples.iterrows()):
        changes.append({'time': i*30,
         'bw': sample['downthrpt'] / 1_000_000 * 8, # need bw in Mbps 
          'rtt': sample['latency'] / 1000, # need rtt in milliseconds
          'loss': 0.00 # no channel loss data 
          })

    profile_template['changes'] = changes

    # with open(f'/vagrant/network_models/fcc/network_config_{target_idx+1}.json', 'w') as f:
    #     json.dump(profile_template, f)
