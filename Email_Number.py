import argparse
import re
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style
import pyfiglet
from playwright.sync_api import sync_playwright

console = Console()

def extract_emails_and_phone_numbers(url):
    banner = pyfiglet.figlet_format("Extract Emails & Phones")
    print(f"{Fore.BLUE}{banner}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Developed by: Ben Mansour Ahmed{Style.RESET_ALL}\n")

    # Launch the browser using Playwright
    with sync_playwright() as pr:
        browser = pr.firefox.launch(headless=True)  # Run in headless mode
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0"})
        page.goto(url, timeout=60000)

        # Retrieve all text from the page
        full_text = page.inner_text("body")

        # Regex to capture emails
        regex_email = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(regex_email, full_text)

        # Regex to capture phone numbers
        regex_phone = r"\+?\d{1,4}[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,4}"
        numbers = re.findall(regex_phone, full_text)

        # Create a table for displaying the results
        table = Table(title="Extracted Information")
        table.add_column("Emails", style="cyan")
        table.add_column("Phone Numbers", style="magenta")

        for email, number in zip(emails, numbers):
            table.add_row(email, number)

        console.print(table)

        # Close the browser
        browser.close()

def search_in_browser(query, num_page):
    banner = pyfiglet.figlet_format("Browser Search")
    print(f"{Fore.BLUE}{banner}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Developed by: Ben Mansour Ahmed{Style.RESET_ALL}\n")

    with sync_playwright() as pr:
        browser = pr.chromium.launch(headless=True)
        page = browser.new_page()
        url_search = f'https://www.bing.com/search?q={query}'
        page.goto(url_search)

        for _ in range(num_page):
            page.wait_for_selector('li.b_algo a', timeout=5000)

            # Extract titles, links, and descriptions
            links = page.eval_on_selector_all("li.b_algo a", "nodes => nodes.map(n => n.href)")
            descriptions = page.eval_on_selector_all("li.b_algo p", "nodes => nodes.map(n => n.innerText)")

            # Create a table for the search results
            table = Table(title=f"Search Results for: {query}")
            table.add_column("Links", style="cyan")
            table.add_column("Descriptions", style="magenta")

            for link, desc in zip(links, descriptions):
                table.add_row(link, desc)

            console.print(table)

            # Click the next page button
            next_page = page.query_selector('a.sb_pagN')
            if next_page:
                next_page.click()
                page.wait_for_timeout(3000)
            else:
                break

        browser.close()

def main():
    parser = argparse.ArgumentParser(description="Web Scraping and Search Tool")
    parser.add_argument("-u", "--url", help="URL to extract emails and phone numbers from", default=None)
    parser.add_argument("-q", "--query", help="Search query to search in browser", default=None)
    parser.add_argument("-n", "--num_pages", type=int, default=5, help="Number of pages to scrape for search query (default: 5)")
    
    args = parser.parse_args()

    if args.url:
        extract_emails_and_phone_numbers(args.url)
    elif args.query:
        search_in_browser(args.query, args.num_pages)
    else:
        print(f"{Fore.RED}Please provide either a URL or a search query!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
