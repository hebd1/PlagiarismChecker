import sys
import config
from googleapiclient.discovery import build
from difflib import SequenceMatcher
import statistics


my_api_key = config.API_KEY
my_cse_id = config.CSE_ID


def google_search(searching_for, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=searching_for, cx=cse_id, **kwargs).execute()
    return res


def snippet_confidence(web_snippet, orig_chunk):
    web_snippet = web_snippet.replace('\n', '')
    orig_chunk = orig_chunk.replace('\n', '')
    match = SequenceMatcher(None, web_snippet, orig_chunk).find_longest_match(0, len(web_snippet), 0, len(orig_chunk))
    match = web_snippet[match.a: match.a + match.size]
    diff = round(len(match) / len(web_snippet), 2)
    return diff

def calculate_score(confidence):
    mean = round(statistics.mean(confidence), 2)
    print('Average Score: ', mean)
    if 1.0 in confidence:
        print('PLAGIARISM DETECTED!! \n An exact match was found in your document \n Better call your lawyer...')
    elif mean >= 0.50:
        print('PLAGIARISM DETECTED!! \n Average score exceeded the threshold \n Better call your lawyer..')
    else:
        print('Looks like your document is ok')

def main():
    print("Welcome to plagiarism checker!")
    if len(sys.argv) <= 1:
        # filename = input("Please enter a filename to check: ")
        filename = "test2.txt"
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
    confidence = []
    for chunk in chunks:
        response = google_search(str(chunk), my_api_key, my_cse_id)
        num_results = response.get('searchInformation').get('totalResults')
        if num_results != '0':
            for item in response.get('items'):
                web_snippet = ''.join(item['snippet'][0:203])
                confidence.append(snippet_confidence(web_snippet, str(chunk)))
    calculate_score(confidence)
    

if __name__ == '__main__':
    main()
