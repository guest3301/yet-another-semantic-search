import json

with open("index.json", "r") as f:
    data = json.loads(f.read())

new_data = list()

# for i in data:
#     if i['text'] is not None:
#         for text in i['text']:
#             new_data.append(text)
#     elif i['text'][0] is None:
#         new_data.append(i['short_text'])
# it was pretty silly error. with type(...) i figured it out.
# there was inconsistency in type(dict['text']) as it was str and list mixed.

for item in data:
    # if not isinstance(item['text'], str):
    #     print(type(item['text']), item)
    if item['text'] is not None:
        new_data.append(item['text'])
    else:
        new_data.append(item['short_text'])

with open("to_embed.json", "w") as f:
    f.write(json.dumps(new_data))
