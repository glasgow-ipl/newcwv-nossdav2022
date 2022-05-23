import sys
import subprocess
import time

if __name__ == '__main__':
    print(sys.argv[1:])
    # Find the root directory
    log_dir = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg == '--log_dir':
            log_dir = sys.argv[1:][i+1]
            break
    print(log_dir)

    trys = 1
    while True:
        f = None
        try:
            f = subprocess.Popen(sys.argv[1:])
            f.wait(30*60) # If the program has not terminated in 30 minutes, possibly the dash.js connection failed to terminate.
        except subprocess.TimeoutExpired:
            f.terminate()

            subprocess.run("sudo mn -c", shell=True)
            applications_to_kill = ['firefox', 'nginx', 'Xvfb']
            for app in applications_to_kill:
                cmd_str = f"sudo killall {app}"
                subprocess.run(cmd_str, shell=True)
            
            f.terminate()

            subprocess.run(f"sudo rm -rf {log_dir}", shell=True)
            subprocess.run(f"touch /vagrant/{log_dir}_fail_{trys}", shell=True)
            trys += 1

            continue

        break
