import json
import os

if __name__ == '__main__':
    s = json.loads('''{
        "changes": [
            {"time": 0, "bw": 9, "rtt": 70}
        ]
    }''')

    for idx, bw in enumerate(range(14, 131)):
        path = os.path.join('/', 'vagrant', 'scripts', 'bws', f'network_config_{idx+1}.json')
        with open(path, 'w') as f:
            s['changes'][0]['bw'] = bw / 10
            json.dump(s, f)
