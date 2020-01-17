from acquisition import acquire
from cleaning import clean
from scraping import scraping
from report import report

def main():
    data = acquire()
    print("data acquire")
    filtered = clean(data)
    print("data clean")
    enriched = scraping(filtered)
    print("data enriched")
    results = report(enriched)
    print("report created")

if __name__ == '__main__':
    main()