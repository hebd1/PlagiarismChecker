import sys
from googleapiclient.discovery import build

my_api_key = "AIzaSyBxH3r-1RTLw3S8f3VoyeouPwf3k-4spLs"
my_cse_id = "000369725811621077877:r5299wu6i08"


def google_search(searching_for, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=searching_for, cx=cse_id, **kwargs).execute()
    return res


def snippet_confidence(snippet, chunk):
    print(snippet)


def main():
    print("Welcome to plagiarism checker!")
    if len(sys.argv) <= 1:
        # filename = input("Please enter a filename to check: ")
        filename = "test1.txt"
    else:
        filename = sys.argv[1]
    with open(filename, 'r') as file:
        start = 0
        end = 33
        data = file.read().split()
    chunks = list()
    while end < len(data):
        chunk = ' '.join(data[start:end])
        chunks.append(chunk)
        end = end + 33
        start = start + 33
        if end > len(data):
            end = len(data)
            chunk = data[start:end]
            chunks.append(chunk)
    confidence = 0.0
    for chunk in chunks:
        result = google_search(str(chunk), my_api_key, my_cse_id)
        for item in result.get('items'):
            confidence = confidence * snippet_confidence(item['snippet'], chunk)

if __name__ == '__main__':
    main()
