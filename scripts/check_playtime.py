import xml.etree.ElementTree as ET
import json
import os
import sys

def check_playtime(mpd_location, dash_js_location):
    tree = ET.parse(mpd_location)
    mpd_duration = tree.getroot().get('mediaPresentationDuration')[2:]
    minutes, seconds = mpd_duration.split('M')
    seconds = seconds[:-1]

    play_time_expected = float(minutes) * 60 * 1000 + float(seconds) * 1000

    with open(dash_js_location) as f:
        dash_dic = json.load(f)

    play_time = dash_dic['play_time']
    delay = dash_dic['total_delay']
    delay += delay * .1 # In case of many rebuffering events allow, we are more linient and allow the OS more time to restart the video
    delay += dash_dic['startup_delay']
    play_time_expected += delay
    root = os.path.dirname(dash_js_location)

    outcome = 'passed'
    if play_time_expected + 3000 < play_time: # give it 3 seconds to account for startup delay and non significant stalls
        outcome = 'failed'
        print("Video playtime significantly deviates from expected playtime")

    with open(os.path.join(root, 'video_duration_%s' % outcome), 'w') as f:
        f.write("%s played video for: %s\nExpected: %s" % (dash_js_location, play_time, play_time_expected))
    
    if outcome == 'failed':
        print("Video played for longer than expected")
        sys.exit(1)


if __name__ == '__main__':
    check_playtime('/vagrant/data/ietf/bbb.mpd', '/vagrant/logs/single/newcwv/dashjs_metrics_client_10.0.0.2.json')
