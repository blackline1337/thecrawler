import aiohttp
import asyncio
import re
from urllib.parse import urljoin
import warnings
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

def run_crawler(target, use_as_module=False, file=None, output=None, filter_file=None, random_agent=False):
    warnings.simplefilter("ignore", category=DeprecationWarning)
    
    if target:
        base_url = target if 'http' in target else f'http://{target}'
    elif file:
        with open(file, 'r') as f:
            targets = [url.strip() for url in f.readlines()]
            base_url = targets[0] if len(targets) == 1 else None
            if not base_url:
                raise ValueError("Please provide a single target URL when using -f/--file option.")
    else:
        raise ValueError("Please provide a target using the -t/--target option or specify a file using -f/--file.")

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(crawl([base_url], use_random_agent=random_agent))

    filter_conditions = []
    if filter_file:
        filter_conditions = read_filters(filter_file)

    extracted_links = []
    for result in results:
        links = find_links(result)

        if filter_conditions:
            links = filter_links(links, filter_conditions)

        extracted_links.extend(links)

    if output:
        save_to_file(extracted_links, output)

    if use_as_module:
        return extracted_links
    else:
        for link in extracted_links:
            print(link)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='The Crawler - A simple and fast web crawler')
    parser.add_argument('-t', '--target', help='Target URL or domain name')
    parser.add_argument('-f', '--file', help='File containing multiple target URLs')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('-ff', '--filter-file', help='Read from a file containing filters')
    parser.add_argument('-ra', '--random-agent', action='store_true', help='Use a random user agent')
    parser.add_argument('-m', '--use-as-module', action='store_true', help='Use as a module (no output)')

    args = parser.parse_args()

    # Check if the script is being run directly and not imported as a module
    if __name__ == "__main__":
        run_crawler(target=args.target, file=args.file, output=args.output, filter_file=args.filter_file, random_agent=args.random_agent, use_as_module=args.use_as_module)
