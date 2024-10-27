## Abstract

Recent advances in deep learning for physics have focused on discovering shared representations of target systems by incorporating physics priors or inductive biases into neural networks. While effective, these

## Introduction

Deep learning has succeeded in many application areas such as image classification, image generation, natural language processing, and so on (Reed et al., 2016; Tan & Le, 2019; Raffel et al., 2020; Gu et al., 2022). One of the major roles of such accomplishment was capable of parameterizing useful representations from data with neural networks (Chen et al., 2020; Van Den Oord et al., 2017; Hamilton et al., 2017). However, grafting deep learning to physics is yet another problem. They struggle to learn conservation laws or implicit physical geometries or symmetries. Although various studies make the model learn the conservative quantities or symmetries inside the system (Greydanus et al., 2019; Sanchez-Gonzalez et al., 2019; Liu & Tegmark, 2021), these approaches are system- specific, which means that if a model is trained for one system, it cannot easily adapt to another system with different physical laws. Since systems whose physics is unknown have more sparse data, these flaws make the standard supervised learning
