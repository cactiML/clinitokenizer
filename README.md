# clinitokenizer

`clinitokenizer` is a sentence tokenizer for clinical text to split unstructured text from clinical text (such as Electronic Medical Records) into individual sentences. 

General English sentence tokenizers are often unable to correctly parse medical abbreviations, jargon, and other conventions often used in medical records (see "Motivating Examples" section below). clinitokenizer is specifically trained on medical record data and can perform better in these situations (conversely, for non-domain specific use, using more general sentence tokenizers may yield better results). 

The model has been trained on multiple datasets provided by [i2b2 (now n2c2)](https://n2c2.dbmi.hms.harvard.edu). Please visit the n2c2 site to request access to the dataset.

## Quickstart

```
from clinitokenizer.tokenize import clini_tokenize

text = "He was asked if he was taking any medications. Patient is currently taking 5 m.g. Tylenol."
sents = clini_tokenize(text)
# sents = ['He was asked if he was taking any medications.', 'Patient is currently taking 5 m.g. Tylenol.']
```

You can use clinitokenizer as a drop-in replacement for [nltk's](https://www.nltk.org/api/nltk.tokenize.html) `sent_tokenize` function:

```
# to swap in clinitokenizer, replace the nltk import...
from nltk.tokenize import sent_tokenize

# ... with the following clinitokenizer import:
from clinitokenizer.tokenize import clini_tokenize as sent_tokenize

# and tokenizing should work in the same manner!
nltk_sents = sent_tokenize(text)
```

## Technical Details

clinitokenizer uses a `bert-large` Transformer model fine-tuned on sentences from Electronic Medical Records provided from the [i2b2/n2c2 dataset](https://n2c2.dbmi.hms.harvard.edu). The model has been fine-tuned and is inferenced using the [Simple Transformers library](http://simpletransformers.ai), and the model is hosted on [HuggingFace ](https://huggingface.co).

The model can be run on GPU or CPU, and will automatically switch depending on availability of GPU.

## Tradeoffs and Considerations

`clinitokenizer` uses a large neural network (about 1.2 GB) which will be downloaded and cached on-device on first run. This initial setup may take a few minutes, but should only happen once.

Compared to other off-the-shelf sentence tokenizers (i.e. `nltk`), `clinitokenizer` will run slower (especially on machines without GPU) and consume more memory, so if near-instant tokenization is the goal, using a GPU-based machine or another tokenizer may be better.

`clinitokenizer` is optimized for natural-language text in the clinical domain. Therefore, when tokenizing more general English sentences or for tasks in a different domain, other generalized tokenizers may perform better.
