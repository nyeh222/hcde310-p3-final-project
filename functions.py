import keys, datetime, requests

quote_page_num = 1

def find_quote(filter = None, type = None, quote_page_num = 1):
    url = "https://favqs.com/api/quotes/"
    headers = {"Authorization": "Token token=" + keys.favq_key}
    params = {"filter": filter, "type": type, "page": quote_page_num}
    try:
        quotes = requests.get(url, headers=headers, params=params)
        return quotes.json()
    except requests.exceptions.RequestException:
        print("There was an error with the request: " + str(quotes.status_code))

def next_page():
    return quote_page_num + 1




url = "https://favqs.com/api/typeahead/"
headers = {"Authorization": "Token token=" + keys.favq_key}

quotes = requests.get(url, headers=headers)
print(quotes.json())