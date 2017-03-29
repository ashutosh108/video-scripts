import urllib.request

ACCOUNT_URL = 'https://livestream.com/accounts/2645002/'


def get_next_event_url(account_url):
    f = urllib.request.urlopen(account_url)
    print(f.read())

def start_downloader_for_next_event(account_url):
    event_url = get_next_event_url(account_url)
    pass


def main():
    start_downloader_for_next_event(ACCOUNT_URL)

if __name__ == '__main__':
    main()
