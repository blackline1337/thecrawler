# The Crawler

## Description

The Crawler is an asynchronous web crawler using `aiohttp`. It extracts links from web pages, allowing users to specify target URLs, input/output files, filter conditions, and use a random user agent. The script is versatile, featuring functions for asynchronous HTTP requests, link extraction, filtering, and result saving. With a concise command-line interface, it provides flexibility for various web crawling tasks, including link filtering and random user agent rotation.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/blackline1337/thecrawler.git
    ```

2. Navigate to the project directory:

    ```bash
    cd thecrawler
    ```

3. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Run the `main.py` script:

    ```bash
    python main.py -h
        usage: main.py [-h] [-t TARGET] [-f FILE] [-o OUTPUT] [-ff FILTER_FILE] [-ra]

        The Crawler - A simple and fast web crawler

        options:
            -h, --help            show this help message and exit
            -t TARGET, --target TARGET
                                    Target URL or domain name
            -f FILE, --file FILE  File containing multiple target URLs
            -o OUTPUT, --output OUTPUT
                                    Output file to save results
            -ff FILTER_FILE, --filter-file FILTER_FILE
                                    Read from a file containing filters
            -ra, --random-agent   Use a random user agent
    ```

    Provide any additional command-line arguments or options that can be used with the script.

## Examples

Crawl with a random user agent
    ```bash
    admin@blacklinecyber:~$ python main.py -t blacklinecyber.org -ra 
    ```

Crawl and save the output to a file
    ```bash
    admin@blacklinecyber:~$ python main.py -t blacklinecyber.org -o output.txt
    ```

Crawl and show results with a filter for example '?', '.php'
    ```bash
    admin@blacklinecyber:~$ python main.py -t blacklinecyber.org -ff filter.txt
    ```

## Contributing

Contribute to this crawler by submitting a pull request.

## License

MIT License

Copyright (c) [2024] [BlackLineCyber]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

contact@blacklinecyber.org
