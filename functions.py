import requests, random
from projectsecrets import keys

#list that stores all quotes to be used
total_quotes = []

#gets motivational quote data from FavQ
#param: page number, default 1
def find_quote(page_num = 1):
    url = "https://favqs.com/api/quotes/"
    headers = {"Authorization": "Token token=" + keys.favq_key}
    params = {"filter": "motivational", "type": "tag", "page": page_num}
    try:
        quotes = requests.get(url, headers=headers, params=params)
        return quotes.json()
    except requests.exceptions.RequestException:
        print("There was an error with the request: " + str(quotes.status_code))


#takes quote body and author from json, formatted in tuples (quote, author)
#excludes dialogue
#param: json data
def extract_quotes(quotes):
    for quote in range(0, len(quotes["quotes"])):
        if "lines" not in quotes["quotes"][quote]:
            author = quotes["quotes"][quote]["author"]
            quote = quotes["quotes"][quote]["body"]
            quote_author = (quote, author)
            total_quotes.append(quote_author)

#gets total number of quotes under the motivational tag
def get_num_quote():
    url = "https://favqs.com/api/typeahead/"
    headers = {"Authorization": "Token token=" + keys.favq_key}
    filters_json = requests.get(url, headers=headers)
    filters = filters_json.json()
    tags = filters["tags"]
    for tag in range(0, len(tags)):
        if tags[tag]["name"] == "motivational":
            return tags[tag]["count"]
    return 1

#goes through most pages and extracts their quote and adds to the list
def all_quotes():
    num_pages = get_num_quote() // 25
    for page in range(1, num_pages + 1):
        extract_quotes(find_quote(page))

#gets a random quote from the quote list
def get_random_quote():
    random_quote = random.choice(total_quotes)
    return random_quote

all_quotes()
print(total_quotes)
print(len(total_quotes))
print()
print(get_random_quote())

# print(get_num_quote())
# url = "https://favqs.com/api/typeahead/"
# headers = {"Authorization": "Token token=" + keys.favq_key}
#
# quotes = requests.get(url, headers=headers)
# print(quotes.json())