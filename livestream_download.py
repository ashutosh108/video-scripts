import urllib.request
import lxml.etree as ET
import re
import json
import datetime
import time
import dateutil.parser
import pytz
import subprocess

# 2645002 is TMS_TV
ACCOUNT_URL = 'https://livestream.com/accounts/2645002'
# ACCOUNT_URL = 'https://livestream.com/accounts/242049'


def get_next_event_url_and_time(account_url):
    f = urllib.request.urlopen(account_url)
    html_parser = ET.HTMLParser()
    tree = ET.parse(f, html_parser)
    for script in tree.getroot().xpath('//head//script'):
        if script.text is None:
            continue
        m = re.match(r'^\s*window\.config\s*=\s*(.*);\s*$', script.text)
        if m:
            json_str = m.group(1)
            json_obj = json.loads(json_str)
            json_account_obj = json.loads(json_obj['account'])
            json_upcoming_events = json_account_obj['upcoming_events']['data']
            return _get_next_event_url_and_start_time_from_upcoming_events(account_url, json_upcoming_events)
        else:
            print("No match")


def _get_next_event_url_and_start_time_from_upcoming_events(account_url, events):
    for event in events:
        start_time_str = event['start_time']
        start_time = dateutil.parser.parse(start_time_str)
        if event['short_name'] is not None:
            short_name = event['short_name']
            return [account_url + '/' + short_name, start_time]
        else:
            event_id = event['id']
            return [account_url + '/events/' + str(event_id), start_time]


def wait_and_start_downloader_for_next_event(account_url):
    event_url, start_time = get_next_event_url_and_time(account_url)
    print("Event url:", event_url)
    print("Start time:", start_time)
    start_time = dateutil.parser.parse('2017-03-30T12:45:00.000Z') + datetime.timedelta(minutes=-15)
    while True:
        t = datetime.datetime.now(pytz.utc)
        print(t)
        if t >= start_time:
            start_downloader(event_url)
            break
        time.sleep(15)
        pass


def start_downloader(event_url):
    print("Starting downloader for", event_url)
    while True:
        f = urllib.request.urlopen(event_url)
        html_parser = ET.HTMLParser()
        tree = ET.parse(f, html_parser)
        for script in tree.getroot().xpath('//head//script'):
            if script.text is None:
                continue
            m = re.match(r'^\s*window\.config\s*=\s*(.*);\s*$', script.text)
            if m:
                json_str = m.group(1)
                json_obj = json.loads(json_str)
                m3u_url = json_obj['event']['stream_info']['secure_m3u8_url']
                short_name = json_obj['event']['short_name']
                if short_name is None:
                    short_name = datetime.datetime.now().strftime('%Y-%m-%d %H-%i')
                print("m3u url:", m3u_url)
                start_download_m3u(m3u_url, short_name)
                return
            else:
                print("No match")
        t = datetime.datetime.now()
        print(t)
        time.sleep(15)


def start_download_m3u(m3u_url, short_name):
    cmd_line = 'cd /c/Users/ashutosh/Downloads; livestreamer "hlsvariant://{}" best -o "{}.ts"'.format(m3u_url, short_name)
    cmd = [r"C:\Program Files\Git\git-bash.exe", '--cd-to-home', '-c', cmd_line]
    subprocess.run(cmd)


def main():
    wait_and_start_downloader_for_next_event(ACCOUNT_URL)

if __name__ == '__main__':
    main()
