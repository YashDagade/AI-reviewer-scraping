## Abstract

The asymptotically precise estimation of the generalization of kernel

## Introduction

Quantitative description of various aspects of neural networks, most notably, generalization perfor- mance after training, is an important but challenging question of deep learning theory. One of the central approaches to this question is built on the connection between neural networks and its neural tangent kernel, first established for infinitely wide networks (Jacot et al., 2018; Lee et al., 2020; Chizat et al., 2019), and then further taken to the rich realm of finite practical networks (Fort et al., 2020; Maddox et al., 2021; Long, 2021; Kopitkov & Indelman, 2020; Vyas et al., 2023). Consider a task of learning target function f ∗(x) from training dataset DN = {xi}N i=1 and (possibly) noisy observation yi = f ∗(xi) + σεi, εi ∼ N (0, 1), using given kernel K(x, x′). Then, many authors (Bordelon et al., 2020; Jacot et al., 2020a; Wei et al., 2022) derive asymptotic N → ∞ generalization error for kernel ridge regression (KRR) algorithm with regularization η: LKRR(η) = 1 2 ∂ηeff ∂η (cid:88) l (ηeff cl)2 + λ2 l (ηeff + λl)2 σ2 N , 1 = η ηeff + 1 N (cid:88) l λl λl + ηeff , (1) where λl are population eigenvalues of K(x, x′) and cl are respective eigencoefficients of f ∗(x) (see definition in (4)). The main motivation of our work is what happens with (1) when, as required by association with neural networks, KRR is replaced with GD or an even more general learning algorithm. Importantly, a result of the type (1) may give precise insights for the family of power-law spectral distributions, closely related to capacity and source assumptions of non-parametric statistics: λl ∼ l−ν (with ν > 1), l ∼ l−κ−1 (with κ > 0). c2 (2) Power-law conditions (2) exhibit a rich picture of convergence rates. For the case of noisy observa- tions σ2 > 0, (Caponnetto & De Vito, 2007) gives minimax rate O(N − κ κ+1 ). For noiseless obser- vations σ2 = 0, the optimal estimation rate significantly improves (Bordelon et al., 2020; Cui et al., 2021) becoming O(N −κ). However, the optimal rates are not always achievable for some classical algorithms. For example, in the case when κ ν > 2 in the noisy case the rate of the KRR becomes 1 Published as a conference paper at ICLR 2024 Noisy observations σ2 > 0 Noiseless observations Exponent in L = O(N −#) Spectral localization scale s KRR (cid:12) (cid:12) (cid:12) (cid:8)0, κ κ+1 (cid:12) (cid:12) (cid:12) 2ν 2ν+1 ν 2ν+1 ν κ+1 Universality yes GF & Optimal KRR & GF & Optimal (cid:9) κ κ+1 ν κ+1 yes κ (cid:12) (cid:12) 2ν ν (cid:12) (cid:12) 0 no Table 1: Our results for power-law spectral distributions (2) and three algorithms: optimally regu- larized KRR, optimally stopped Gradient Flow (GF), and the optimal algorithm (see Section 3). For ν = 2, the vertical line ·(cid:12) quantities exhibiting saturation at κ (cid:12)· separates saturated and non-saturated values. The spectral localization at scale s means that the error is accumulated at eigenvalues λ of the order N −s (see Section 5.1). In the last line, by universality, we mean the asymptotic equality of the errors for different problems with the same population spectrum λl, cl. While we show the universality only for our two data models, we would expect it to hold for a broader class of data models. O(N − 2ν 2ν+1 ), i.e. KRR doesn’t attain the minimax lower bound (Li et al., 2023). Such an effect is usually called saturation and is well-known in various non-parametric problems (Math´e, 2004; Bauer et al., 2007). However, the saturation effect can be removed with algorithms other than KRR, for example spectral cut-off (Bauer et al., 2007) or gradient descent (Pillaud-Vivien et al., 2018). In noiseless case, (Bordelon et al., 2020; Cui et al., 2021) show saturation at the same point κ ν > 2, with the rate changing to O(N −2ν). Whether noiseless saturation can be removed by algorithms other than KRR, to the best of our knowledge, was not studied in the literature. Our contribution. In this work, we augment the above picture in several directions, as summarized in Table 1 and the following three blocks Loss functional. In Section 3, we introduce a new kernel learning framework by specifying the learning algorithm with a spectral profile h(λ) and expressing the generalization error as a quadratic functional of this profile. While specific choices of h(λ) can give KRR, Gradient Flow (GF), or any iterative first-order algorithm, we go beyond these classical examples and consider the optimal learning algorithm as the minimizer of the loss functional for a given problem. The models. As the loss functional is problem-specific, we consider two different models: a Wishart-type model with Gaussian features and a translational-invariant model on a circle. In Sec- tion 4, we derive loss functionals for these models. In addition, we introduce a simple Naive Model for Noisy Observations (NMNO). In the presence of observations noise, for reasonable learning al- gorithms, and at least for power-law spectrum, NMNO model gives asymptotically exact loss values for both Wishart and Circle models despite their differences. This suggests a possible universality property for a larger family of problems, including our Wishart and Circle models as special cases. Results for power-law spectrum. In Section 5, we reach specific