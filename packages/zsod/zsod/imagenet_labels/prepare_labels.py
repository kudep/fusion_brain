import json

import pandas as pd

groups_df = pd.read_csv('groups.csv')

with open('synsets.txt', 'r') as f:
    synsets_str = f.read()
    synsets = eval(synsets_str)

with open('simple.json', 'r') as f:
    simple = json.load(f)

with open('first.json', 'r') as f:
    only_first = json.load(f)
    only_first = [only_first[str(i)][1].replace('_', ' ') for i in
                  range(len(only_first))]

groups = {}

for row_id in range(len(groups_df)):
    category = groups_df.iloc[row_id, 0]
    labels = [word.replace('_', ' ') for word in groups_df.iloc[row_id, 1:] if
              isinstance(word, str)]
    groups[category] = labels

labels = [synset.split(', ') + [simple[int(i)]] for i, synset in synsets.items()]

for group, classes in groups.items():
    for category in classes:
        if category.startswith('crane'):
            category = 'crane'
        labels[only_first.index(category)].append(group)

with open('imagenet_labels.json', 'w') as f:
    json.dump(labels, f)
