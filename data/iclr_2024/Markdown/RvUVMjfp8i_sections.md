## Abstract

Semi-supervised learning (SSL) is a powerful paradigm for leveraging unlabeled data and has been proven to be successful across various tasks. Conventional SSL studies typically assume close environment scenarios where labeled and unlabeled examples are independently sampled from the same distribution. However, real- world tasks often involve open environment scenarios where the data distribution, label space, and feature space could differ between labeled and unlabeled data. This inconsistency introduces robustness challenges for SSL algorithms. In this paper, we first propose several robustness metrics for SSL based on the Robustness Analysis Curve (RAC), secondly, we establish a theoretical framework for studying the generalization performance and robustness of SSL algorithms in open environ- ments, thirdly, we re-implement widely adopted SSL algorithms within a unified SSL toolkit and evaluate their performance on proposed open environment SSL benchmarks, including both image, text, and tabular datasets. By investigating the empirical and theoretical results, insightful discussions on enhancing the robustness of SSL algorithms in open environments are presented. The re-implementation and benchmark datasets are all publicly available. More details can be found at https://ygzwqzd.github.io/Robust-SSL-Benchmark. 1

## Introduction

Semi-supervised learning (SSL) aims to leverage unlabeled data to improve learning performance when labels are limited or expensive to obtain (Chapelle et al., 2006). SSL algorithms have been repeatedly reported to achieve highly competitive performance to purely supervised learning and save a lot of labeling costs, by exploring the structure of unlabeled data. All of the positive results, however, are based on the close environment assumption where labeled and unlabeled data are sampled from the same distribution independently. However, many practical applications involve open environments (Zhou, 2022) where the data distribution, feature space, and label space could be inconsistent between labeled and unlabeled data. SSL