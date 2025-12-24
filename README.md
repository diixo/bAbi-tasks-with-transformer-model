# bAbi-tasks-with-transformer-model

Fine tune and evaluate transformer model on facebook's bAbi tasks.
> [Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks](https://arxiv.org/abs/1502.05698)


## Requirements:

```bash
pip install numpy==1.26.4
pip install torch==2.5.1
pip install pandas==2.3.1
pip install datasets==3.6.0
pip install transformers==4.56.1
pip install evaluate==0.4.6
```

|task_no|epochs|learning_rate|batch_size| corrects/all |
|-------|------|-------------|----------|--------------|
|  qa1  |  15  |    3e-04    |    8     |   862/1000   |
|  qa1  |  20  |    3e-04    |    8     |   988/1000   |
|  qa1  |  15  |    2e-04    |    8     |   998/1000   |
|  qa1  |  20  |    2e-04    |    8     |  1000/1000   |
|  qa1  |  20  |    1e-04    |    8     |   999/1000   |
|  qa1  |  30  |    1e-04    |    8     |   995/1000   |
|  qa1  |  50  |    5e-05    |    8     |  1000/1000   |

|task_no|epochs|learning_rate|batch_size| corrects/all |     qa1     |
|-------|------|-------------|----------|--------------|-------------|
|  qa2  |  30  |    2e-04    |    8     |   445/1000   |             |
|  qa2  |  30  |    1e-04    |    8     |   845/1000   |             |
|  qa2  |  50  |    1e-04    |    8     |   865/1000   |   779/1000  |
|  qa1 + qa2 | 50 | 1e-04    |    8     |   929/1000   |  1000/1000  |


|task_no |epochs|learning_rate|batch_size|  corrects/all  |
|--------|------|-------------|----------|----------------|
|  qa22  |  1   |    1e-4     |    8     |   ????/10000   |
|  qa22  |  1   |    5e-5     |    8     |   ????/10000   |
|  qa22  |  1   |    1e-4     |    10    |   ????/10000   |
|  qa22  |  1   |    5e-5     |    10    |   ????/10000   |


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


## Acknowledgements:

Based on original: https://github.com/p208p2002/bAbi-tasks-with-transformer-model
