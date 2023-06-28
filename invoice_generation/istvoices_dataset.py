'''
Template:  https://huggingface.co/docs/datasets/v1.4.0/add_dataset.html
Reference: https://huggingface.co/datasets/nielsr/funsd-layoutlmv3/blob/main/funsd-layoutlmv3.py
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

def normalize_bbox(bbox, size):
    '''Normalizes a bounding box between (0-1000)'''
    return [
        int(1000 * bbox[0] / size[0]),
        int(1000 * bbox[1] / size[1]),
        int(1000 * bbox[2] / size[0]),
        int(1000 * bbox[3] / size[1]),
    ]

_CITATION = '''
            @unpublished{Habram2023,
                abstract = {},
                title = {An Investigation into the Impact of Multimodality on Named Entity Recognition},
                author = {Istvan Habram},
                year = {2023},
                month = {September},
                note = {IstVoices Dataset for Named Entity Recognition on Synthetic Invoices}
            }
            '''

_DESCRIPTION = '''
               Synthetic dataset for NER on invoices.
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

    BUILDER_CONFIG = IstVoicesConfig(name="IstVoices", version=datasets.Version("1.0.0"), description="IstVoices dataset")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "bboxes": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=['B-R_NAME',   'B-R_STREET', 'B-R_HOUSENUMBER', 'B-R_ZIP',    'B-R_CITY',     'B-R_COUNTRY', 'B-R_VAT',
                                   'I-R_NAME',   'I-R_STREET', 'I-R_HOUSENUMBER', 'I-R_ZIP',    'I-R_CITY',     'I-R_COUNTRY', 'I-R_VAT',
                                   'B-S_NAME',   'B-S_STREET', 'B-S_HOUSENUMBER', 'B-S_ZIP',    'B-S_CITY',     'B-S_COUNTRY', 'B-S_VAT',
                                   'I-S_NAME',   'I-S_STREET', 'I-S_HOUSENUMBER', 'I-S_ZIP',    'I-S_CITY',     'I-S_COUNTRY', 'I-S_VAT',
                                   'B-S_BANK',   'B-S_BIC',    'B-S_IBAN',        'B-S_TEL',    'B-S_EMAIL',
                                   'I-S_BANK',   'I-S_BIC',    'I-S_IBAN',        'I-S_TEL',    'I-S_EMAIL',
                                   'B-I_NUMBER', 'B-I_DATE',   'B-I_DUEDATE',     'B-I_AMOUNT', 'B-I_CURRENCY',
                                   'I-I_NUMBER', 'I-I_DATE',   'I-I_DUEDATE',     'I-I_AMOUNT', 'I-I_CURRENCY', 'OTHER']
                        )
                    ),
                    "image": datasets.features.Image(),
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
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": f"{downloaded_file}/training_data/"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": f"{downloaded_file}/testing_data/"}
            ),
        ]

    def _generate_examples(self, filepath):
        '''Turns the files into instances of the dataset (rows of the dataset)'''
        logger.info("⏳ Generating examples from = %s", filepath)
        ann_dir = os.path.join(filepath, "annotations")
        img_dir = os.path.join(filepath, "images")
        for guid, file in enumerate(sorted(os.listdir(ann_dir))):
            tokens = []
            bboxes = []
            ner_tags = []

            file_path = os.path.join(ann_dir, file)
            with open(file_path, "r", encoding="utf8") as f:
                data = json.load(f)
            image_path = os.path.join(img_dir, file)
            image_path = image_path.replace("json", "tif")
            image, size = load_image(image_path)

            for item in data:
                words, label = item["words"], item["label"]
                words = [w for w in words if w["text"].strip() != ""]
                if len(words) == 0:
                    continue
                if label == "Other":
                    for w in words:
                        tokens.append(w["text"])
                        ner_tags.append("OTHER")
                        bboxes.append(normalize_bbox(item["box"], size))
                else:
                    tokens.append(words[0]["text"])
                    ner_tags.append("B-" + label.upper())
                    bboxes.append(normalize_bbox(item["box"], size))
                    for w in words[1:]:
                        tokens.append(w["text"])
                        ner_tags.append("I-" + label.upper())
                        bboxes.append(normalize_bbox(item["box"], size))

            yield guid, {"id": str(guid), "tokens": tokens, "bboxes": bboxes, "ner_tags": ner_tags, "image": image}