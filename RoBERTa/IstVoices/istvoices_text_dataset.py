'''
This script turns the raw files into a dataset can be used universally.
'''

import os
import json
import datasets
from PIL import Image


def load_image(image_path):
    '''Loads and image, returns the image itself and the dimensions of it.'''
    image = Image.open(image_path).convert("RGB")
    w, h = image.size
    return image, (w, h)

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
                            names=['R_Name', 'R_Street', 'R_HouseNumber', 'R_ZIP', 'R_City', 'R_Country', 'R_VAT',
                                   'S_Name', 'S_Street', 'S_HouseNumber', 'S_ZIP', 'S_City', 'S_Country', 'S_VAT',
                                   'S_Bank', 'S_BIC', 'S_IBAN', 'S_Tel', 'S_Email', 
                                   'I_Number', 'I_Date', 'I_DueDate', 'I_Amount', 'I_Currency', 'Other']
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
        downloaded_file = r'C:\Users\Habram\Documents\Datasets\IstVoices_text'
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": f"{downloaded_file}/training_data/"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": f"{downloaded_file}/testing_data/"}
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

            tokens, ner_tags = data["tokens"], data["ner_tags"]

            yield guid, {"tokens": tokens, "ner_tags": ner_tags}