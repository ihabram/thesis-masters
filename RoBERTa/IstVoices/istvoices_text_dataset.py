'''
This script turns the raw files into a dataset can be used universally.
'''

import os
import json
import datasets

_CITATION = '''
            @unpublished{Habram2023,
                abstract = {},
                title = {An Investigation into the Impact of Multimodality on Named Entity Recognition},
                author = {Istvan Habram},
                year = {2023},
                month = {September},
                note = {Hochschule Bonn-Rhein-Sieg, Sankt Augustin, Germany}
            }
            '''

_DESCRIPTION = '''
               Synthetic dataset for NER on raw text.
               Created by Istvan Habram in 2023 for his Master's Thesis project.
               The dataset consists of 200 fully-annotated documents.
               25 NER tags were used to annotate the documents.
               '''

# Print the progress of the dataset generation to the terminal
logger = datasets.logging.get_logger(__name__)

class IstVoicesConfig(datasets.BuilderConfig):
    """BuilderConfig for IstVoices"""

    def __init__(self, **kwargs):
        super(IstVoicesConfig, self).__init__(**kwargs)


class IstVoices(datasets.GeneratorBasedBuilder):
    """DatasetBuilder for IstVoices"""

    BUILDER_CONFIG = IstVoicesConfig(name="IstVoices_text", version=datasets.Version("1.0.0"), description="IstVoices_text dataset")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=['O',
                                   'B-R_NAME', 'I-R_NAME', 'B-R_STREET', 'I-R_STREET', 'B-R_HOUSENUMBER', 'I-R_HOUSENUMBER',
                                   'B-R_ZIP',  'I-R_ZIP',  'B-R_CITY',   'I-R_CITY',   'B-R_COUNTRY', 'I-R_COUNTRY', 'B-R_VAT', 'I-R_VAT',
                                   'B-S_NAME', 'I-S_NAME', 'B-S_STREET', 'I-S_STREET', 'B-S_HOUSENUMBER', 'I-S_HOUSENUMBER',
                                   'B-S_ZIP',  'I-S_ZIP',  'B-S_CITY',   'I-S_CITY',   'B-S_COUNTRY', 'I-S_COUNTRY', 'B-S_VAT', 'I-S_VAT',          
                                   'B-S_BANK', 'I-S_BANK',  'B-S_BIC', 'I-S_BIC', 'B-S_IBAN', 'I-S_IBAN', 'B-S_TEL', 'I-S_TEL', 
                                   'B-S_EMAIL', 'I-S_EMAIL', 'B-I_NUMBER', 'I-I_NUMBER', 'B-I_DATE', 'I-I_DATE', 'B-I_DUEDATE',  'I-I_DUEDATE',
                                   'B-I_AMOUNT', 'I-I_AMOUNT', 'B-I_CURRENCY', 'I-I_CURRENCY'
                                ]
                        )
                    )
                }
            ),
            supervised_keys=None,
            homepage="No home page yet",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        ''' Splits the dataset into TRAIN and TEST subsets '''
        downloaded_file = r'C:\Users\Habram\Documents\Datasets\IstVoices'
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": f"{downloaded_file}/training_data/annotations/"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": f"{downloaded_file}/testing_data/annotations/"}
            ),
        ]

    def _generate_examples(self, filepath):
        '''Turns the files into instances of the dataset (rows of the dataset)'''
        logger.info("⏳ Generating examples from = %s", filepath)

        for guid, file in enumerate(sorted(os.listdir(filepath))):
            file_path = os.path.join(filepath, file)
            tokens = []
            ner_tags = []
            
            with open(file_path, "r", encoding="utf8") as f:
                data = json.load(f)

            for item in data:
              words, label = item["words"], item["label"]
              words = [w for w in words if w["text"].strip() != ""]
              if len(words) == 0:
                  continue
              if label == "Other":
                  for w in words:
                      tokens.append(w["text"])
                      ner_tags.append("O")
              else:
                  tokens.append(words[0]["text"])
                  ner_tags.append("B-" + label.upper())
                  for w in words[1:]:
                      tokens.append(w["text"])
                      ner_tags.append("I-" + label.upper())

            yield guid, {"tokens": tokens, "ner_tags": ner_tags}