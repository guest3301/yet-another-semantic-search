"""
A script to chunk long texts into smaller ones. 
Because vector embeddings for models have specific limit, and they ignore the rest of texts 
that is not within their limit size. s
"""

import json

def chunk_by_char(text, chunk_size=300, chunk_overlap=20):
    chunks = []
    start_idx = 0
    
    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)
        
        start_idx = (
            end_idx - chunk_overlap if end_idx < len(text) else len(text)
        )
    
    return chunks

with open("response.json", "r") as f:
    data = json.loads(f.read())

new_data = list()
for part in data:
    text = part['text']
    if text is not None and len(text.split()) > 300:
        text_array = chunk_by_char(text)

        for i in text_array:
            new_dict = dict(url=part['url'], short_text=part['short_text'], text=i)
            new_data.append(new_dict)
        # part['text'] = text
        # We are changing our embed.json structure to make sure that we can embed more efficiently, and 
        # with less hassle. the idea is that we'll be creating additional dictionary if text exceeds
        # the specified limit (context limit of model, basically).
        # so it will be easier for final processing before embedding.
        # above commented line of code was our previous approach.
    else:
        new_dict = dict(url=part['url'], short_text=part['short_text'], text=text)
        new_data.append(new_dict)
        # part['text'] = [text]

with open("index.json", "w") as f:
    f.write(json.dumps(new_data))