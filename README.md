# bAbi-tasks-with-transformer-model
Fine tune and evaluate transformer model on facebook's bAbi tasks.
> [Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks](https://arxiv.org/abs/1502.05698)


## Requirements:

```bash
pip install torch==2.5.1+cu118
pip install pandas==2.3.1
pip install datasets==3.6.0
pip install transformers==4.56.1
pip install scikit-learn==1.6.1
pip install evaluate==0.4.6
```


## Tasks
|task_no|task_name|
|----|------------|
|qa1 |single-supporting-fact|
|qa2 |two-supporting-facts|
|qa3 |three-supporting-facts|
|qa4 |two-arg-relations|
|qa5 |three-arg-relations|
|qa6 |yes-no-questions|
|qa7 |counting|
|qa8 |lists-sets|
|qa9 |simple-negation|
|qa10| indefinite-knowledge|
|qa11| basic-coreference|
|qa12| conjunction|
|qa13| compound-coreference|
|qa14| time-reasoning|
|qa15| basic-deduction|
|qa16| basic-induction|
|qa17| positional-reasoning|
|qa18| size-reasoning|
|qa19| path-finding|
|qa20| agents-motivations|

## Avaliable Models
- [gpt2-babi](https://huggingface.co/p208p2002/gpt2-babi)
- [gpt2-medium-babi](https://huggingface.co/p208p2002/gpt2-medium-babi)
- [gpt2-large-babi](https://huggingface.co/p208p2002/gpt2-large-babi)
