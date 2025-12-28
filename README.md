# bAbi-tasks-with-transformer-model (SFT-mode for GPT2)

**Supervised fine tune** (**SFT**) and evaluate transformer model on facebook's bAbi tasks:
> [Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks](https://arxiv.org/abs/1502.05698)


* **Training**: [trainer.py](trainer.py)

* **Evaluation**: [eval.py](eval.py)


|task_no|epochs|learning_rate|batch_size| corrects/all |
|-------|------|-------------|----------|--------------|
|  qa1  |   2  |    1e-04    |    8     |   991/1000   |
|  qa1  |   3  |    1e-04    |    8     |  1000/1000   |


|  task_no  |epochs|learning_rate|batch_size|     qa1      |     qa2     |
|-----------|------|-------------|----------|--------------|-------------|
| qa1 + qa2 |   2  |    1e-04    |    8     |   977/1000   |   523/1000  |
| qa1 + qa2 |   3  |    1e-04    |    8     |   995/1000   |   683/1000  |
| qa1 + qa2 |   5  |    1e-04    |    8     |  1000/1000   |   890/1000  |
| qa1 + qa2 |  10  |    1e-04    |    8     |  1000/1000   |   904/1000  |


## Tasks

|task_no|task_name|
|------|-----------------------|
| qa1  | single-supporting-fact|
| qa2  | two-supporting-facts|
| qa3  | three-supporting-facts|
| qa4  | two-arg-relations|
| qa5  | three-arg-relations|
| qa6  | yes-no-questions|
| qa7  | counting|
| qa8  | lists-sets|
| qa9  | simple-negation|
| qa10 | indefinite-knowledge|
| qa11 | basic-coreference|
| qa12 | conjunction|
| qa13 | compound-coreference|
| qa14 | time-reasoning|
| qa15 | basic-deduction|
| qa16 | basic-induction|
| qa17 | positional-reasoning|
| qa18 | size-reasoning|
| qa19 | path-finding|
| qa20 | agents-motivations|


### Requirements:

```bash
pip install numpy==1.26.4
pip install torch==2.5.1
pip install pandas==2.3.1
pip install datasets==3.6.0
pip install transformers==4.56.1
pip install evaluate==0.4.6
```


## Acknowledgements:

Based on original: https://github.com/p208p2002/bAbi-tasks-with-transformer-model

* https://github.com/MostafaDehghani/bAbI-T2T

* https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/babi_qa.py
