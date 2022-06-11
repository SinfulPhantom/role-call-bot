from os.path import exists
import configparser


def load_config():
    config = configparser.ConfigParser()
    config_file = "config.ini"
    if not exists(config_file):
        create_config(config)
    return config, config_file


def add_config_value(list_to_change, new_value, settings="settings"):
    new_value_str = str(new_value)
    config, config_file = load_config()
    try:
        config.read(config_file)
        fetched_list = config.get(settings, list_to_change)
        if fetched_list == '':
            config.set(settings, list_to_change, new_value_str)
            with open(config_file, 'w') as cf:
                config.write(cf)
            return f"Added {new_value} to {list_to_change}"

        converted_settings_list = fetched_list.split(',')
        if new_value_str in converted_settings_list:
            return f"That is already part of {list_to_change}"

        converted_settings_list.append(new_value_str)
        config.set(settings, list_to_change, ','.join(converted_settings_list))
        with open(config_file, 'w') as cf:
            config.write(cf)
        return f"Added {new_value} to {list_to_change}"
    except Exception as e:
        return f"Exception {type(e)}|{e} happened!"


def create_config(config):
    config['settings'] = {
        'command_channel': '',
        'attendance_channel': '',
        'allowed_roles': '',
    }
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
