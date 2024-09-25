# Privacy-Preserving Data Deduplication for Enhancing Federated Learning of Language Models

This repository contains the source code to our paper <i>Privacy-Preserving Data Deduplication for
Enhancing Federated Learning of Language Models</i>.

The `EP_MPD` folder implements our core contribution, a privacy-preserving data duplication for protocol that removes all pairwse duplicates among datasets held by 2 or more clients.

The `FL` folder shows a working example of how to use `EP_MPD` as a pre-processing step to remove duplicates before running the `FedAvg` algorithm.

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
