from os.path import dirname
import parse_access_log
import os
import parse_dash_log

resolutions_newcwv = ['480x200', '480x250', '480x300', '480x400','480x500','480x600','480x700']
bitrates_newcwv=[0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7]

q_kbps = {200: 0.2, 250:0.25, 300: 0.3, 400: 0.4, 500: 0.5, 600: 0.6, 700: 0.7}

if __name__ == '__main__':
    for alg in ['newcwvh', 'renoh']:
        for run in ['', '2', '3', '4']:
            dir_name = f'newcwv_{alg}{run}_05_17'
            print(f"Processing {dir_name}")

            log_path = os.path.join('/', 'vagrant', 'logs', 'tmp', 'newcwv', 'static', dir_name)

            access_log_path = os.path.join(log_path, 'nginx_access.log')
            time_quality = parse_access_log.get_qualities(access_log_path)
            time, qualities = zip(*time_quality)
            print("\tAverage bitrate: %s " %parse_access_log.calculate_avg_bitrate(qualities, q_kbps))

            print("\tAverage bitrate osc: %s " % parse_access_log.calculate_avg_oscillation(qualities, q_kbps))

            from . import parse_dash_log
            dash_log_path = os.path.join(log_path, 'dashjs_metrics.json')
            print("\tStartup delay: %s " % parse_dash_log.get_startup_delay(dash_log_path))
            print("\tStall time: %s " % parse_dash_log.get_total_stall_time(dash_log_path))
            # print(parse_dash_log.get_client_estimations(dash_log_path))
