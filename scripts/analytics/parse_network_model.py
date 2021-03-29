import json


def get_bw_changes_list(network_profile_path):
    """
        Returns: A list of link changes in Mbps
    """
    link_change_bucket = []
    with open(network_profile_path) as f:
        config = json.load(f)
        for entry in config['changes']:
            link_change_bucket.append(entry['bw'])

    return link_change_bucket

if __name__ == '__main__':
    get_bw_changes_list('/vagrant/network_models/dash_if/network_config_1.json')