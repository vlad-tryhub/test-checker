import urllib.request
import urllib.error
import re
from multiprocessing import Process


def request(url):
    try:
        return print(f'{urllib.request.urlopen(url, timeout=5).getcode()}\t{url}')
    except urllib.error.URLError as e:
        return print(f'{e.reason}\t{url}')
    except BaseException as e:
        return print(f'{e.__class__}\t{url}')

def get_urls_text():
    with open('urls.txt', 'r', encoding="utf8") as file:
        return file.read()

def run_requests_in_parallel(urls):
    running_requests = []
    for url in urls:
        p = Process(target=request, args=(url,))
        p.start()
        running_requests.append(p)
    for p in running_requests:
        p.join()
    print('finish')

if __name__ == '__main__':
    file_content = get_urls_text()
    matches = re.findall("(https?://[^\s\(\)/]+)", file_content)
    filtered_matches = filter(lambda x: len(re.findall("(youtube)|(facebook)", x)) == 0, matches)
    filtered_matches = list([match.rstrip("/") for match in filtered_matches])
    distinct_matches = list(set(filtered_matches))
    distinct_matches.sort()
    #print('\n'.join(distinct_matches))
    run_requests_in_parallel(distinct_matches)
