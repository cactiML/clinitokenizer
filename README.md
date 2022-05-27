# clinitokenizer

`clinitokenizer` is a sentence tokenizer for clinical text to split unstructured text from clinical text (such as Electronic Medical Records) into individual sentences. 

General English sentence tokenizers are often unable to correctly parse medical abbreviations, jargon, and other conventions often used in medical records (see "Motivating Examples" section below). clinitokenizer is specifically trained on medical record data and can perform better in these situations (conversely, for non-domain specific use, using more general sentence tokenizers may yield better results). 

The model has been trained on multiple datasets provided by [i2b2 (now n2c2)](https://n2c2.dbmi.hms.harvard.edu). Please visit the n2c2 site to request access to the dataset.

## Installation
```bash
pip install clinitokenizer
```

## Quickstart

```python
from clinitokenizer.tokenize import clini_tokenize

text = "He was asked if he was taking any medications. Patient is currently taking 5 m.g. Tylenol."
sents = clini_tokenize(text)
# sents = ['He was asked if he was taking any medications.',
#         'Patient is currently taking 5 m.g. Tylenol.']
```

You can use clinitokenizer as a drop-in replacement for [nltk's](https://www.nltk.org/api/nltk.tokenize.html) `sent_tokenize` function:

```python
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


## Motivating Examples
Below are some examples of clinical text comparing `clinitokenizer` to `nltk.tokenize.sent_tokenize`:


### "He was asked if he was taking any medications. Patient is currently taking 5 m.g. Tylenol."
**notes:** Challenge here is not mistaking m.g. for end-of-sentence.

**nltk output:** 

```
He was asked if he was taking any medications.
Patient is currently taking 5 m.g.
Tylenol.
```


**clinitokenizer output:**

```
He was asked if he was taking any medications. 
Patient is currently taking 5 m.g. Tylenol.
```

---

### "Pt. has hx of alcohol use disorder He is recovering."
**notes:** Challenge here is there is a typo after 'disorder', missing a period. Can tokenizer semantically identify new sentence?

**nltk output:**

```
Pt.
has hx of alcohol use disorder He is recovering.
```

**clinitokenizer output:**
```
Pt. has hx of alcohol use disorder 
He is recovering.
```

---

### "Pt. has hx of alcohol use disorder but He is recovering."
**notes:** Opposite as previous example -- here, there is an accidental capitalization. Can tokenizer semantically identify it is NOT a new sentence?

**nltk output:**

```
Pt.
has hx of alcohol use disorder but He is recovering.
```

**clinitokenizer output:**

```
Pt. has hx of alcohol use disorder but He is recovering.
```

---

### "Past Medical History: Patient has PMH of COPD."
**notes:** "Past Medical History" is a sentence header. Even though it is technically a single sentence according to English grammar, when extracting section headers it may be important to identify them as distinct from all sentences under that header.

**nltk output:**

```
Past Medical History: Patient has PMH of COPD.
```

**clinitokenizer output:**

```
Past Medical History: 
Patient has PMH of COPD.
```
