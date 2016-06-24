from requests import get
url = 'https://raw.githubusercontent.com/wooorm/afinn-111/master/data/afinn-111.json'
w = get(url).json()

# Find affinity for a word
filter(lambda i: i[0]=='gross', w.items())

# Find all words above a given affinity, in alphabetical order
sorted(filter(lambda i: i[1]>3, w.items()))

# Find all words containing a string, in alphabetical order
sorted(filter(lambda i: 'bea' in i[0], w.items()))
