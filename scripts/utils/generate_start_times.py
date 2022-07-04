import random
import subprocess
import json

random.seed(42)

if __name__ == '__main__':
    out = subprocess.Popen('make echo_log', stdout=subprocess.PIPE, shell=True)
    runs = out.stdout.read().decode().strip()

    runs_list = runs.split(' ')

    start_times = []
    generating = True

    old_alg = None

    start_times_json = {}

    for entry in runs_list:
        tokens = entry.rsplit('/')
        alg = tokens[-2].split('_')[1]
        if old_alg and old_alg != alg:
            generating = False
            seed_list_index = 0
        
        old_alg = alg

        for i in range(len(tokens)):
            if tokens[i] == 'clients':
                clients_num = int(tokens[i+1])
        
        if generating:
            start_times_run = []
            for i in range(clients_num - 1):
                start_times_run.append(random.randint(0, 60*5)) 
            start_times.append(start_times_run)
        else:
            start_times_run = start_times[seed_list_index]
            seed_list_index += 1

        start_times_json[entry.rsplit('/', 1)[0]] = start_times_run


    with open('/vagrant/start_times.json', 'w') as f:
        json.dump(start_times_json, f)
    
    print("/vagrant/start_times.json updated")
