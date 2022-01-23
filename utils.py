import time

from requests import Session

from cache import DiskCache

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'


headers = {
    'User-Agent': USER_AGENT,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "embed-808462.secondstreetapp.com",
    "Referer": "https://embed-808462.secondstreetapp.com/embed/4b368605-14ad-4bc4-b1cf-6d02be89e49d/",
    "sec-ch-ua": '"Chromium";"v"="97", " Not;A Brand";"v"="99"',
    "sec-ch-ua-platform": "Linux",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": 'cors',
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "X-Api-Key": "65032887",
    "X-Fingerprint": "DNT",
    "X-Organization-Id": "2293",
    "X-Organization-Promotion-Id": "808462",
    "X-Promotion-Id": "677132",
    "X-Requested-With": "XMLHttpRequest"
}

session = Session()

cache = DiskCache()


def get_matchups(session):
    url = 'https://embed-808462.secondstreetapp.com/api/matchups?excludeSecondaryMatchups=true'

    result = []

    try:
        result = cache[url]
    except KeyError:
        if not result:
            time.sleep(1)
            resp = session.get(url, headers=headers)
            resp_obj = resp.json()
            data = resp_obj.get('matchups')
            if data:
                for item in data:
                    result.append({
                        'name': item.get('name'),
                        'matchup_group_id': item.get('matchup_group_id'),
                        'id': item.get('id')
                    })

            cache[url] = result

    except:
        result = []

    return result or []

def get_matchup_groups(session):
    url = 'https://embed-808462.secondstreetapp.com/api/matchup_groups'

    result = []
    try:
        result = cache[url]
    except KeyError:
        if not result:
            time.sleep(1)
            resp = session.get(url, headers=headers)
            resp_obj = resp.json()
            data = resp_obj.get('matchup_groups')
            if data:
                for item in data:
                    result.append({
                    "id": item.get('id'),
                    "name": item.get('name')
                })
            cache[url] = result

    except:
        result = []

    return result or []

def get_winners(session):
    url = 'https://embed-808462.secondstreetapp.com/api/winners'

    result = []
    try:
        result = cache[url]
    except KeyError:
        if not result:
            time.sleep(1)
            resp = session.get(url, headers=headers)
            resp_obj = resp.json()
            data = resp_obj.get('winners')
            if data:
                for item in data:
                    result.append({
                    'matchup_entry_id': item.get('matchup_entry_id'),
                    'matchup_id': item.get('matchup_id'),
                    'title': item.get('media_title'),
                    'rank': item.get('rank')

                })
            cache[url] = result
    except:
        result = []

    return result or []

def get_matchup_entries(session, group_id=None):
    url = f'https://embed-808462.secondstreetapp.com/api/matchup_entries?matchupGroupId={group_id}&pageIndex=1&pageSize=10000'

    print(f'Url:  {url}')

    result = []

    try:
        result = cache[url]
    except KeyError:
        if not result:
            time.sleep(1)
            resp = session.get(url, headers=headers)
            resp_obj = resp.json()
            data = resp_obj.get('matchup_entries')
            if data:
                for item in data:
                    result.append({
                    'id': item.get('id'),
                    'matchup_id': item.get('matchup_id'),
                    'name': item.get('entries').get('name'),
                    'address': item.get('entries').get('full_address')
                })
            cache[url] = result
    except:
        result = []

    return result or []
