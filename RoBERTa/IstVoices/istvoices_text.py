'''
This script is responsible to convert the original IstVoices dataset's annotation files
into IstVoices_text files.
Difference between them:
- The original IstVoices dataset annotation files included the bounding boxes and
handled the associated words in one block.
- IstVoices_text dataset extracts every individual word and the corresponding label.
- The words which are related must be next to each other.
'''

import json
import os

input_dir = r'C:\Users\Habram\Documents\Datasets\IstVoices'
output_dir= r'C:\Users\Habram\Documents\Datasets\IstVoices_text'

input_splits = [r'\testing_data\annotations', r'\training_data\annotations']
output_splits = [r'\testing_data', r'\training_data']

# Iterate over the train and test splits
for split, _ in enumerate(input_splits):
    # Iterate over every file in the split  
    for file in os.listdir(input_dir + input_splits[split]):
        # Get example ID
        id = file[:-5]

        # Opening JSON file
        f = open(input_dir + input_splits[split] + '\\' + file)
        
        # returns JSON object as a dictionary
        data = json.load(f)

        # Store the textual data in a dictionary
        text_data = {
            'tokens': [],
            'ner_tags': []
        }

        # Extract the words and labels
        for elem in data:
            for word in elem['words']:
                text_data['tokens'].append(word['text'])
                text_data['ner_tags'].append(elem['label'])

        # Save the dictionary as a JSON file
        with open(output_dir + output_splits[split] + '\\' + id + '_text.json', 'w') as fp:
            json.dump(text_data, fp)