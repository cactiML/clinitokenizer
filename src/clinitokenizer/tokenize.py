import torch
from simpletransformers.ner import NERModel
from tqdm import tqdm
import logging

MAX_SEQ = 32
CUDA_AVAILABLE = torch.cuda.is_available()
TOKENIZER_MODEL = ("bert", "samrawal/medical-sentence-tokenizer")


class CliniTokenize:
    def __init__(
        self,
        tokenizer_model=TOKENIZER_MODEL,
        max_seq=MAX_SEQ,
        use_cuda=CUDA_AVAILABLE,
    ):

        self.MAX_SEQ = max_seq
        self.use_cuda = use_cuda

        self.model = NERModel(
            tokenizer_model[0],
            tokenizer_model[1],
            args={"silent": True, "labels_list": ["B-sent", "B-split", "I-sent"]},
            use_cuda=self.use_cuda,
        )

    def _inference(self, model, text, split_on_space=True):
        pred, raw_output = model.predict([text], split_on_space=split_on_space)
        pred = list(map(lambda x: [(k, v) for k, v in x.items()][0], pred[0]))
        return pred

    def _last_new_sent(self, x):
        try:
            return len(x) - x[::-1].index(1) - 1
        except:
            return -1

    def tokenize(self, text: str):
        BUFFER_SIZE = self.MAX_SEQ

        split = text.split()
        all_sents = []
        new_sent = []

        total_iterations = len(split) + BUFFER_SIZE
        with tqdm(
            total=total_iterations, desc="Tokenizing sentences", leave=False
        ) as pbar:
            while len(split) > 0:
                buffer = split[: min(BUFFER_SIZE, len(split))]
                pred = self._inference(self.model, buffer, split_on_space=False)
                while len(buffer) != len(pred):
                    if len(buffer) == 1:
                        logging.warning(
                            "Error tokenizing even when buffer size is 1, skipping."
                        )
                        continue
                    BUFFER_SIZE = int(BUFFER_SIZE / 2)
                    logging.warning(
                        "Buffer size reduced to {} for iteration.".format(BUFFER_SIZE)
                    )
                    buffer = split[: min(BUFFER_SIZE, len(split))]
                    pred = self._inference(self.model, buffer, split_on_space=False)
                assert len(buffer) == len(pred)

                new_sents = [1 if x[1] == "B-sent" else 0 for x in pred]
                last = self._last_new_sent(new_sents)

                if last == 0:
                    if len(new_sent) > 0:
                        all_sents.append(" ".join(new_sent))
                        new_sent = []
                    new_sent.extend([x[0] for x in pred])
                    split = split[BUFFER_SIZE:]
                    delta = BUFFER_SIZE

                elif last == -1:
                    new_sent.extend([x[0] for x in pred])
                    split = split[BUFFER_SIZE:]
                    delta = BUFFER_SIZE

                else:
                    for i in range(last):
                        if pred[i][-1] == "B-sent":
                            if len(new_sent) > 0:
                                all_sents.append(" ".join(new_sent))
                                new_sent = []
                        new_sent.append(pred[i][0])
                    split = split[last:]
                    delta = last

                BUFFER_SIZE = self.MAX_SEQ
                pbar.update(delta)
            all_sents.append(" ".join(new_sent))
            pbar.close()
        return all_sents


clinitokenize = None


def clini_tokenize(text):
    # lazy loading of model
    global clinitokenize
    if clinitokenize == None:
        clinitokenize = CliniTokenize()

    return clinitokenize.tokenize(text)
