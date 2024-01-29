import aiohttp
import asyncio
import argparse
import re
import warnings
from urllib.parse import urljoin
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

async def fetch(session, url, use_random_agent=False):
    try:
        headers = {'User-Agent': UserAgent(software_names=[SoftwareName.CHROME.value], operating_systems=[OperatingSystem.WINDOWS.value]).get_random_user_agent()} if use_random_agent else {'User-Agent': 'Mozilla/5.0'}
        async with session.get(url, headers=headers) as response:
            return await response.text()
    except Exception as e:
        warnings.warn(f"Failed to fetch {url}: {str(e)}")
        return None

def find_links(text):
    pattern = r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1'
    links = re.findall(pattern, text)
    return [link[1] for link in links]

def filter_links(links, filter_conditions):
    filtered_links = []
    for link in links:
        if any(filter_condition in link for filter_condition in filter_conditions):
            filtered_links.append(link)
    return filtered_links

async def crawl(urls, use_random_agent=False):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, use_random_agent) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses

def save_to_file(links, output_file):
    with open(output_file, 'w') as file:
        for link in links:
            file.write(link + '\n')

def read_filters(file_path):
    with open(file_path, 'r') as file:
        return [filter_condition.strip() for filter_condition in file.readlines()]

def construct_full_url(base_url, target):
    return urljoin(base_url, target)

if __name__ == "__main__":
    # Ignore DeprecationWarning - I added this because of the aiohttp library
    warnings.simplefilter("ignore", category=DeprecationWarning)

    parser = argparse.ArgumentParser(description='The Crawler - A simple and fast web crawler')
    parser.add_argument('-t', '--target', help='Target URL or domain name')
    parser.add_argument('-f', '--file', help='File containing multiple target URLs')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('-ff', '--filter-file', help='Read from a file containing filters')
    parser.add_argument('-ra', '--random-agent', action='store_true', help='Use a random user agent')

    args = parser.parse_args()

    if args.target:
        base_url = args.target if 'http' in args.target else f'http://{args.target}'
    elif args.file:
        with open(args.file, 'r') as file:
            targets = [url.strip() for url in file.readlines()]
            base_url = targets[0] if len(targets) == 1 else None
            if not base_url:
                parser.error("Please provide a single target URL when using -f/--file option.")
    else:
        parser.error("Please provide a target using the -t/--target option or specify a file using -f/--file.")

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(crawl([base_url], use_random_agent=args.random_agent))

    filter_conditions = []
    if args.filter_file:
        filter_conditions = read_filters(args.filter_file)

    for result in results:
        links = find_links(result)

        if filter_conditions:
            links = filter_links(links, filter_conditions)

        if args.output:
            save_to_file(links, args.output)

        for link in links:
            print(link)
