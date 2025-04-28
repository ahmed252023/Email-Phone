https://github.com/ahmed252023/Email-Phone.git
Description
This is a powerful Python tool that can:

Extract emails and phone numbers from any webpage.

Perform automated Bing searches and scrape the results across multiple pages.

It uses Playwright for browser automation and Rich and Colorama for colorful, beautiful terminal output.

🚀 Features
📩 Extract all emails and phone numbers from a given URL.

🔎 Perform Bing search queries and scrape results.

📄 Scrape multiple search result pages automatically.

🎨 Colorful and structured terminal output with tables.

⚡ Fast, headless (no browser pop-up) browsing.


How to Use :

git clone https://github.com/ahmed252023/Email-Phone.git

cd email-phone
pip install -r requirements.txt
playwright install
python Email_Number.py -u https://example.com

Options :
-u : Provide a URL to extract emails/phones from.

-q : Provide a search query for Bing search.

-n : Number of pages to scrape (default: 5).
