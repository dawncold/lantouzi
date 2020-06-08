import os
import os.path
import re
import datetime
import csv
import json
import requests
from pyquery import PyQuery as pq
from lxml import etree

if not os.path.exists('posts'):
    os.mkdir('posts')

def load_existing_links():
    if not os.path.exists('posts/page-links'):
        return []
    with open('posts/page-links') as f:
        existing_links = [line.strip() for line in f.readlines()]
    return existing_links

def build_index():
    print('building post links...')
    existing_links = load_existing_links()
    news_list_url = 'https://ios.lantouzi.com/post'
    page_num = 1
    while 1:
        resp = requests.get(f'{news_list_url}', params={'page': page_num})
        d = pq(etree.HTML(resp.content))
        links = d('.news-list a').map(lambda i, e: pq(e).attr('href'))
        if not links:
            break
        new_links = set(links) - set(existing_links)
        if not new_links:
            print('all links could existed')
            break
        with open(f'posts/page-links', 'a+') as f:
            f.writelines('\n'.join(links))
            f.write('\n')
        page_num += 1

def crawl_post_content(post_url):
    print(f'crawl: {post_url}')
    resp = requests.get(post_url)
    d = pq(etree.HTML(resp.content))
    content = d('p.MsoNormal').text()
    post_id = int(post_url.split('/')[-1])
    with open(f'posts/post-{post_id}', 'w') as f:
        f.write(content)

def extract_structure_data(content):
    print('extracting structure data...')
    total_search = re.search('(\d+(,\d+)*\.?\d+)元', content)
    if not total_search:
        return
    total = total_search.group(1)
    time_search = re.findall('(\d\d\d\d年\d\d月\d\d日\d\d点\d\d分)', content)
    if not time_search:
        return
    start_time, end_time = time_search

    with open('posts/structure-data', 'a+') as f:
        f.write(f'{start_time} {end_time} {total}\n')

def sort_structure_data():
    with open('posts/structure-data') as f:
        lines = f.readlines()
    lines.sort()
    with open('posts/structure-data', 'w+') as f:
        f.writelines(lines)

def extract_year(year):
    print(f'extracting year: {year}')
    with open('posts/structure-data') as f:
        lines = f.readlines()
    date2total = {}
    for line in lines:
        if not line.strip():
            continue
        line = line.strip()
        if f'{year}年' not in line:
            continue
        start_time_str, end_time_str, total_str = line.split()
        start_date = datetime.datetime.strptime(start_time_str, '%Y年%m月%d日%H点%M分').date()
        end_date = datetime.datetime.strptime(end_time_str, '%Y年%m月%d日%H点%M分').date()
        date2total[end_date.strftime('%Y-%m-%d')] = total_str.replace(',', '')
    
    stat_date = datetime.date(year, 1, 1)
    stats = []
    while 1:
        date_str = stat_date.strftime('%Y-%m-%d')
        stats.append((date_str, date2total.get(date_str, '')))
        stat_date += datetime.timedelta(days=1)
        if stat_date.year > year or stat_date > datetime.date.today():
            break
    with open(f'posts/stats-year-{year}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['date', 'total'])
        writer.writerows(stats)
    with open(f'posts/stats-year-{year}.json', 'w') as f:
        f.write(json.dumps({'stats': stats}))

if __name__ == '__main__':
    build_index()
    
    for link in load_existing_links():
        post_id = int(link.split('/')[-1])
        if os.path.exists(f'posts/post-{post_id}'):
            continue
        crawl_post_content(link)
    
    if os.path.exists('posts/structure-data'):
        os.remove('posts/structure-data')

    for post_content_name in os.listdir('posts'):
        if not os.path.isfile(f'posts/{post_content_name}') or not post_content_name.startswith('post-'):
            continue
        with open(f'posts/{post_content_name}') as f:
            content = f.read()
        extract_structure_data(content)
    
    sort_structure_data()

    extract_year(2019)
    extract_year(2020)