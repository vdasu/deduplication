# Privacy-Preserving Data Deduplication for Enhancing Federated Learning of Language Models

This repository contains the source code accompanying our paper <i>Privacy-Preserving Data Deduplication for
Enhancing Federated Learning of Language Models</i> which has been accepted at the Network and Distributed Security Symposium (NDSS) 2025.

The `EP_MPD` folder implements our core contribution, a privacy-preserving data duplication protocol that removes all pairwise duplicates among datasets held by 2 or more clients.

The `FL` folder shows a working example of how to use `EP_MPD` as a pre-processing step to remove duplicates before running the `FedAvg` algorithm. It also contains code to analyze the effects of duplicates on the perplexity and running time of fine-tuning `GPT-2` models.

Please refer to the two folders for detailed instructions on how to run.

## Citation

```
@misc{abadi2024privacypreservingdatadeduplicationenhancing,
      title={Privacy-Preserving Data Deduplication for Enhancing Federated Learning of Language Models}, 
      author={Aydin Abadi and Vishnu Asutosh Dasu and Sumanta Sarkar},
      year={2024},
      eprint={2407.08152},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2407.08152}, 
}
```
