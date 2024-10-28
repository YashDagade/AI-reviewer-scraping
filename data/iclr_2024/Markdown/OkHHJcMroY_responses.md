## Reviewer Responses

### Decision 1
**Author:** Program Chairs

**Decision:**
Accept (spotlight)


### Meta Review 2
**Author:** Area Chair jkMV

**Metareview:**
The paper proposes a single\-timescale off\-policy evaluation algorithm which has both excellent theoretical properties (1/K convergence) as well as a more practical variant which performs well in practice. 


All reviewers agree on the paper being accepted, some enthusiastically so.

**Justification For Why Not Higher Score:**
It could be accepted as oral

**Justification For Why Not Lower Score:**
It could be accepted as poster


### Official Review 3
**Author:** Reviewer V3H9

**Summary:**
This work investigates policy evaluation with nonlinear function approximation. The work proposes path\-integrated primal\-dual stochastic gradient (PILOT), and PILOT\+. It shows that PILOT converges to stationary point with a convergence rate of $O(1/K). The theoretical results are based on the assumption of strong concavity and bounded variance. With adaptive batch size, PILOT\+ achieves some empirical results that demonstrates some sample efficiency. The algorithms demonstrate some efficiency on simple simulation tasks like Mountain Car and Cartpole.

**Soundness:**
3 good

**Presentation:**
3 good

**Contribution:**
2 fair

**Strengths:**
The work proposes a pair of algorithms, PILOT and PILOT\+, which are good in theory and in practice, respectively. It is nice to have variants of the algorithm to excel in both perspectives. The results on stationary point convergence and a convergence rate of O(1/K) seem relevant.

**Weaknesses:**
The work is based on very strong assumptions, which do not hold in RL tasks in general. It is of course valid to argue that some previous works are also based on such assumptions, but with the assumptions the work offers less relevance and less technical contribution to the community.

**Questions:**
N/A

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
6: marginally above the acceptance threshold

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 4
**Author:** Authors

**Comment:**
Thank you very much for your valuable feedback. Our point\-to\-point responses are as follows:



> **Your Comment 1:** The work is based on very strong assumptions, which do not hold in RL tasks in general. It is of course valid to argue that some previous works are also based on such assumptions, but with the assumptions the work offers less relevance and less technical contribution to the community.


**Our Response:** Thanks for your comments. We note that our assumptions are not strong and they have been widely adopted in the reinforcement learning (RL) literature due to their applicability for RL tasks in practice. For example, \[Wai et al. (2019\), Qiu et al. (2020\), Du et al. (2017\)] use similar assumptions as ours.


Further, we provide the following technical justifications here for each assumption we use to illustrate why they will hold in general:


**1\) Justification of Assumption 1:** To see why Assumption 1 holds, recall that D\=Es\[∇θVθ(s)∇θVθ(s)⊤]∈Rd×d, which implies that D is positive definite. Further, as the number of random samples M increases, D becomes more and more likely to be full\-rank, i.e., D becomes positive definite. That is, as M becomes sufficiently large, one can always find a μ\>0 such that μ≤λmin(D). Moreover, as soon as we find such a μ\>0, this μ is independent of M as M continues to increase. This μ\-value further implies the strong concavity relation stated in Assumption 1\. This justifies Assumption 1 holding in general. 


**2\) Justification of Assumption 2:** Assumption 2 states that the gradients of the loss function with respect to both θ and ω areLf\-smooth. This assumption holds in RL environments under the following conditions:


1. *Smooth Reward Functions:* If the reward function and transition dynamics of the environment are smooth (quite common in many RL applications), the resulting value function (for which the policy evaluation is trying to approximate) will also be smooth. This smoothness often implies that the objective function with respect to θ and ω are also smooth, especially in cases where these parameters are part of a linear function approximation or a differentiable function approximator (e.g., neural networks).
2. *Boundedness of State and Action Spaces:* If the spaces of states and actions are bounded, which is often the case in practical RL scenarios, the function mapping states and actions to values or rewards will be smooth.


**3\) Justifications of Assumption 3:** In the context of mean\-squared projected Bellman error (MSPBE) framework for RL policy evaluation (PE), if the MSPBE\-based min\-max problem is well\-posed (often true for most RL applications in practice), then this optimization problem is naturally bounded from below (i.e., the optimal value of the outer optimization problem will not go to negative infinity).


**4\) Justifications of Assumption 4:** The bounded variance in Assumption 4 is guaranteed to hold under the compact set condition and common for stochastic approximation algorithms for min\-max optimization (see, e.g.,\[Qiu et al., 2020; Lin et al., 2020a]). Also, this assumption holds in RL under following common conditions: In many RL applications modeled as Markov Decision Processes (MDPs), the state and action spaces are finite. This inherently limits the range of possible rewards, leading to a bounded variance of the stochastic gradients of the MSPBE function.


**5\) A Concrete Example:** Finally, to further highlight the applicability and summarize the above justifications of our assumptions, we use an RL application as a concrete example, where **all four assumptions hold**. In the MountainCar RL problem, the environment dynamics are smooth because the physics governing the car's movement. Specifically, the car's position and velocity evolve continuously based on the laws of physics (e.g., acceleration, gravity). In MountainCar, the variance of rewards is bounded because the reward structure is simple and deterministic (i.e., it does not involve any complex stochastic elements): the agent gets a reward of \-1 for each time step until the agent reaches the goal, which is clearly a simple and bounded reward signal. Moreover, in practice, there are no sources of significant randomness in the MountainCar environment that would lead to high variance in rewards.


### Official Comment 5
**Author:** Reviewer V3H9

**Comment:**
I thank the authors for providing additional justifications for the assumptions.


### Official Comment 6
**Author:** Authors

**Comment:**
Thank you very much for your valuable feedback. Our point\-to\-point responses are as follows:



> **Your Comment 1:** The work is based on very strong assumptions, which do not hold in RL tasks in general. It is of course valid to argue that some previous works are also based on such assumptions, but with the assumptions the work offers less relevance and less technical contribution to the community.


**Our Response:** Thanks for your comments. We note that our assumptions are not strong and they have been widely adopted in the reinforcement learning (RL) literature due to their applicability for RL tasks in practice. For example, \[Wai et al. (2019\), Qiu et al. (2020\), Du et al. (2017\)] use similar assumptions as ours.


Further, we provide the following technical justifications here for each assumption we use to illustrate why they will hold in general:


**1\) Justification of Assumption 1:** To see why Assumption 1 holds, recall that D\=Es\[∇θVθ(s)∇θVθ(s)⊤]∈Rd×d, which implies that D is positive definite. Further, as the number of random samples M increases, D becomes more and more likely to be full\-rank, i.e., D becomes positive definite. That is, as M becomes sufficiently large, one can always find a μ\>0 such that μ≤λmin(D). Moreover, as soon as we find such a μ\>0, this μ is independent of M as M continues to increase. This μ\-value further implies the strong concavity relation stated in Assumption 1\. This justifies Assumption 1 holding in general. 


**2\) Justification of Assumption 2:** Assumption 2 states that the gradients of the loss function with respect to both θ and ω areLf\-smooth. This assumption holds in RL environments under the following conditions:


1. *Smooth Reward Functions:* If the reward function and transition dynamics of the environment are smooth (quite common in many RL applications), the resulting value function (for which the policy evaluation is trying to approximate) will also be smooth. This smoothness often implies that the objective function with respect to θ and ω are also smooth, especially in cases where these parameters are part of a linear function approximation or a differentiable function approximator (e.g., neural networks).
2. *Boundedness of State and Action Spaces:* If the spaces of states and actions are bounded, which is often the case in practical RL scenarios, the function mapping states and actions to values or rewards will be smooth.


**3\) Justifications of Assumption 3:** In the context of mean\-squared projected Bellman error (MSPBE) framework for RL policy evaluation (PE), if the MSPBE\-based min\-max problem is well\-posed (often true for most RL applications in practice), then this optimization problem is naturally bounded from below (i.e., the optimal value of the outer optimization problem will not go to negative infinity).


**4\) Justifications of Assumption 4:** The bounded variance in Assumption 4 is guaranteed to hold under the compact set condition and common for stochastic approximation algorithms for min\-max optimization (see, e.g.,\[Qiu et al., 2020; Lin et al., 2020a]). Also, this assumption holds in RL under following common conditions: In many RL applications modeled as Markov Decision Processes (MDPs), the state and action spaces are finite. This inherently limits the range of possible rewards, leading to a bounded variance of the stochastic gradients of the MSPBE function.


**5\) A Concrete Example:** Finally, to further highlight the applicability and summarize the above justifications of our assumptions, we use an RL application as a concrete example, where **all four assumptions hold**. In the MountainCar RL problem, the environment dynamics are smooth because the physics governing the car's movement. Specifically, the car's position and velocity evolve continuously based on the laws of physics (e.g., acceleration, gravity). In MountainCar, the variance of rewards is bounded because the reward structure is simple and deterministic (i.e., it does not involve any complex stochastic elements): the agent gets a reward of \-1 for each time step until the agent reaches the goal, which is clearly a simple and bounded reward signal. Moreover, in practice, there are no sources of significant randomness in the MountainCar environment that would lead to high variance in rewards.


### Official Comment 7
**Author:** Reviewer V3H9

**Comment:**
I thank the authors for providing additional justifications for the assumptions.


### Official Review 8
**Author:** Reviewer XRvu

**Summary:**
The authors develop a single\-timescale version of the non\-linear policy evaluation algorithm (PILOT). The algorithm allows for instance\-independent stepsize choice and relies on the primal\-dual optimization with additional variance reduction for gradient computations. The authors also provide a modification of their approach with adaptive batch size selection in order to avoid the preiodic full gradient computations.

**Soundness:**
4 excellent

**Presentation:**
3 good

**Contribution:**
3 good

**Strengths:**
The introduced algorithm, PILOT, provides an explicit convergence rate under the choice of small and constant step sizes. Moreover, the obtained convergence rate matches the previous minimax bound. Convergence rates are studied under the assumptions, which are classical in the optimization literature. The authors present a comprehensive framework for their theoretical analysis, and the exposition of the paper is accessible.

**Weaknesses:**
The only weakness is the experimental section, which contains rather simple scenarios. At the same time, for the paper which is primarily theoretical, the proposed illustration is sufficient.

**Questions:**
a)If time permits, I would suggest the authors to complement the experimental section. 


b) The authors could also complement the bibliography on linear policy evaluation methods (TD(0\) with modifications) by the following papers:


1. Li, Tianjiao, Guanghui Lan, and Ashwin Pananjady. "Accelerated and instance\-optimal policy evaluation with linear function approximation." arXiv preprint arXiv:2112\.13109 (2021\) \- [https://arxiv.org/abs/2112\.13109](https://arxiv.org/abs/2112.13109)
2. Patil, Gandharv, et al. "Finite time analysis of temporal difference learning with linear function approximation: Tail averaging and regularisation." International Conference on Artificial Intelligence and Statistics. PMLR, 2023\. \- [https://arxiv.org/abs/2210\.05918](https://arxiv.org/abs/2210.05918)
The first one concerns instance\-optimal guarantees for Polyak\-Ruppert averaged iterates of TD(0\). The authors also use SPIDER\-type variance reduction. The second paper concerns TD(0\) with realizable step size.


c) I am also a bit surprised by the fact that the mixing time of the original chain (s1,a1,s2,…) does not pop up explicitly in the bounds. This would be a typical behavior for the optimization problems with dependent data. What is the explanation?

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
8: accept, good paper

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 9
**Author:** Authors

**Comment:**
Thank you for your constructive feedback and comments. Our point\-to\-point responses are as follows:



> **Your Comment 1:** The only weakness is the experimental section, which contains rather simple scenarios. At the same time, for the paper which is primarily theoretical, the proposed illustration is sufficient. If time permits, I would suggest the authors to complement the experimental section.


**Our Response:** Thank you for your constructive feedback on the experimental section of our paper. We appreciate your recognition of the primarily theoretical focus of our work and your understanding of the scope of our current experimental validation. **In the appendix of this paper, we have included further experiments on the Navigation tasks, where the state space has 30 dimensions.** We hope that these additional larger\-scale experiments could strengthen the empirical evidence supporting our theoretical findings and provide deeper insights into the practical applicability of our proposed algorithms.



> **Your Comment 2:** The authors could also complement the bibliography on linear policy evaluation methods (TD(0\) with modifications) by the following papers:
> 
> 
> \[R3] Li, Tianjiao, Guanghui Lan, and Ashwin Pananjady. "Accelerated and instance\-optimal policy evaluation with linear function approximation." arXiv preprint arXiv:2112\.13109 (2021\) \- [https://arxiv.org/abs/2112\.13109](https://arxiv.org/abs/2112.13109)
> 
> 
> \[R4] Patil, Gandharv, et al. "Finite time analysis of temporal difference learning with linear function approximation: Tail averaging and regularisation." International Conference on Artificial Intelligence and Statistics. PMLR, 2023\. \- [https://arxiv.org/abs/2210\.05918](https://arxiv.org/abs/2210.05918) 
> 
> 
> The first one concerns instance\-optimal guarantees for Polyak\-Ruppert averaged iterates of TD(0\). The authors also use SPIDER\-type variance reduction. The second paper concerns TD(0\) with realizable step size.


**Our Response:** Thank you for suggesting additional references to complement the bibliography of our paper. In this rebuttal period, we have carefully read these two papers. The relationships and differences between these two papers and our work are summarized as follows:


\[R4] investigates the finite\-time behavior of the widely\-used temporal difference (TD) learning algorithm when combined with the tail\-averaging technique and \[R4] achieves O(1/K) convergence rate. Tail averaging is a technique that averages the model parameters over the last few iterations (the "tail" of the optimization process). This method can lead to a more stable and generalizable model because it effectively smooths out the noise and variance in the parameter updates toward the end of the training. Similarly, \[R3] provided instance\-optimal guarantees for Polyak\-Ruppert averaged iterates of TD(0\). However, it's worth noting that these two works only focused on the **linear function approximation** setting, as a special case of the **nonlinear function approximation** setting considered in our paper. Moreover, as RL applications become increasingly sophisticated, most recent RL algorithms utilize **nonlinear function approximation** (e.g., deep neural network (DNN)) to model the value function. This motivates us to develop a new PILOT method, which is able to achieve a fast convergence speed for RL policy evaluation with nonlinear function approximation.


We will incorporate the references suggested by the reviewer into the related work section and add the above discussions in our paper. These additions will undoubtedly enhance the breadth and depth of our paper, providing a more comprehensive overview of the state\-of\-the\-art in policy evaluation methods.


### Official Comment 10
**Author:** Authors

**Comment:**
> **Your Comment 3:** I am also a bit surprised by the fact that the mixing time of the original chain (s1,a1,..) does not pop up explicitly in the bounds. This would be a typical behavior for optimization problems with dependent data. What is the explanation?


**Our Response:** Thanks for your comments. We agree with the reviwer that the samples of the M\-step trajectory (s1,s1,…,sM,aM,sM\+1) is Markovian. However, due to the challenge of handling dependent data, in the literature, many policy evaluation methods with linear/nonlinear function approximations and temporal differences (e.g., \[Wai et al. (2019\), Qiu et al. (2020\), Du et al. (2017\)]) ignored the Markovian data dependence and still used the finite\-sum empirical loss is an approximation of the expected loss function for PE. As a result, mixing time does not appear in the convergence bounds in these works. Moreover, as discussed in the footnote on Page 5 in our paper, although the finite\-sum empirical loss is an approximation of the expected loss function, it has been shown in \[Chen et al. (2021\)] that, under the conditions of bounded instantaneous loss and bounded derivatives (satisfied for most applications in practice), the approximation error of using empirical loss for Markovian data is small with high probability (cf.Lemma\~2 \[Chen et al. (2021]). Thus, the empirical loss has been widely used as a proxy for the expected loss of Markovian data in the literature \[Liu et al. (2015\); Wai et al. (2019\); Du et al. (2017\)].


Meanwhile, we do agree with the reviewer that a more thorough analysis incorporating the effects of the mixing time of the Markovian data will provide a more complete and deeper understanding of PE algorithms' convergence behavior, especially in complex environments where the dependency structure of the data cannot be ignored. How to develop variance\-reduction\-based accelerated PE algorithms with nonlinear function approximation under Markovian data is an important open problem, which deserves an independent paper dedicated to this topic. This problem will be left as an important future research, and we thank the reviewer for bringing up this direction.


### Official Comment 11
**Author:** Reviewer XRvu

**Comment:**
Dear authors,


I am pleased with your constructive feedback. I remain positive about the submission, and continue to support its acceptance with the same score.


### Official Comment 12
**Author:** Authors

**Comment:**
Thank you for your constructive feedback and comments. Our point\-to\-point responses are as follows:



> **Your Comment 1:** The only weakness is the experimental section, which contains rather simple scenarios. At the same time, for the paper which is primarily theoretical, the proposed illustration is sufficient. If time permits, I would suggest the authors to complement the experimental section.


**Our Response:** Thank you for your constructive feedback on the experimental section of our paper. We appreciate your recognition of the primarily theoretical focus of our work and your understanding of the scope of our current experimental validation. **In the appendix of this paper, we have included further experiments on the Navigation tasks, where the state space has 30 dimensions.** We hope that these additional larger\-scale experiments could strengthen the empirical evidence supporting our theoretical findings and provide deeper insights into the practical applicability of our proposed algorithms.



> **Your Comment 2:** The authors could also complement the bibliography on linear policy evaluation methods (TD(0\) with modifications) by the following papers:
> 
> 
> \[R3] Li, Tianjiao, Guanghui Lan, and Ashwin Pananjady. "Accelerated and instance\-optimal policy evaluation with linear function approximation." arXiv preprint arXiv:2112\.13109 (2021\) \- [https://arxiv.org/abs/2112\.13109](https://arxiv.org/abs/2112.13109)
> 
> 
> \[R4] Patil, Gandharv, et al. "Finite time analysis of temporal difference learning with linear function approximation: Tail averaging and regularisation." International Conference on Artificial Intelligence and Statistics. PMLR, 2023\. \- [https://arxiv.org/abs/2210\.05918](https://arxiv.org/abs/2210.05918) 
> 
> 
> The first one concerns instance\-optimal guarantees for Polyak\-Ruppert averaged iterates of TD(0\). The authors also use SPIDER\-type variance reduction. The second paper concerns TD(0\) with realizable step size.


**Our Response:** Thank you for suggesting additional references to complement the bibliography of our paper. In this rebuttal period, we have carefully read these two papers. The relationships and differences between these two papers and our work are summarized as follows:


\[R4] investigates the finite\-time behavior of the widely\-used temporal difference (TD) learning algorithm when combined with the tail\-averaging technique and \[R4] achieves O(1/K) convergence rate. Tail averaging is a technique that averages the model parameters over the last few iterations (the "tail" of the optimization process). This method can lead to a more stable and generalizable model because it effectively smooths out the noise and variance in the parameter updates toward the end of the training. Similarly, \[R3] provided instance\-optimal guarantees for Polyak\-Ruppert averaged iterates of TD(0\). However, it's worth noting that these two works only focused on the **linear function approximation** setting, as a special case of the **nonlinear function approximation** setting considered in our paper. Moreover, as RL applications become increasingly sophisticated, most recent RL algorithms utilize **nonlinear function approximation** (e.g., deep neural network (DNN)) to model the value function. This motivates us to develop a new PILOT method, which is able to achieve a fast convergence speed for RL policy evaluation with nonlinear function approximation.


We will incorporate the references suggested by the reviewer into the related work section and add the above discussions in our paper. These additions will undoubtedly enhance the breadth and depth of our paper, providing a more comprehensive overview of the state\-of\-the\-art in policy evaluation methods.


### Official Comment 13
**Author:** Authors

**Comment:**
> **Your Comment 3:** I am also a bit surprised by the fact that the mixing time of the original chain (s1,a1,..) does not pop up explicitly in the bounds. This would be a typical behavior for optimization problems with dependent data. What is the explanation?


**Our Response:** Thanks for your comments. We agree with the reviwer that the samples of the M\-step trajectory (s1,s1,…,sM,aM,sM\+1) is Markovian. However, due to the challenge of handling dependent data, in the literature, many policy evaluation methods with linear/nonlinear function approximations and temporal differences (e.g., \[Wai et al. (2019\), Qiu et al. (2020\), Du et al. (2017\)]) ignored the Markovian data dependence and still used the finite\-sum empirical loss is an approximation of the expected loss function for PE. As a result, mixing time does not appear in the convergence bounds in these works. Moreover, as discussed in the footnote on Page 5 in our paper, although the finite\-sum empirical loss is an approximation of the expected loss function, it has been shown in \[Chen et al. (2021\)] that, under the conditions of bounded instantaneous loss and bounded derivatives (satisfied for most applications in practice), the approximation error of using empirical loss for Markovian data is small with high probability (cf.Lemma\~2 \[Chen et al. (2021]). Thus, the empirical loss has been widely used as a proxy for the expected loss of Markovian data in the literature \[Liu et al. (2015\); Wai et al. (2019\); Du et al. (2017\)].


Meanwhile, we do agree with the reviewer that a more thorough analysis incorporating the effects of the mixing time of the Markovian data will provide a more complete and deeper understanding of PE algorithms' convergence behavior, especially in complex environments where the dependency structure of the data cannot be ignored. How to develop variance\-reduction\-based accelerated PE algorithms with nonlinear function approximation under Markovian data is an important open problem, which deserves an independent paper dedicated to this topic. This problem will be left as an important future research, and we thank the reviewer for bringing up this direction.


### Official Comment 14
**Author:** Reviewer XRvu

**Comment:**
Dear authors,


I am pleased with your constructive feedback. I remain positive about the submission, and continue to support its acceptance with the same score.


### Official Review 15
**Author:** Reviewer sDVM

**Summary:**
The paper introduces two algorithms, PILOT and PILOT\+, designed for Policy Evaluation (PE) with non\-linear function approximation. Theoretical analysis shows that PILOT, a single\-timescale algorithm using VR techniques, achieves an O(1/K) convergence rate with constant step sizes. PILOT\+ enhances sample efficiency by adapting batch sizes based on historical stochastic gradient information. Experimental results validate the theoretical findings regarding convergence and sample complexity.

**Soundness:**
3 good

**Presentation:**
3 good

**Contribution:**
3 good

**Strengths:**
1. The paper is fairly well organized and the results provided are impressive.
2. The related work and comparison with other algorithms and techniques are comprehensive.
3. The theoretical guarantee is solid and the paper also demonstrates the effectiveness of the algorithm in practice.

**Weaknesses:**
1. Since the paper claims the algorithms they propose achieve the first O(1/K) convergence rate (K is the number of
iterations) with constant step\-sizes for PE with nonlinear function approximation, it is better to give some brief statistical intuition of achieving this result.
2. The paper proposes a new metric for convergence performance, and gives the abundant explanation for using this concept, but it is hard to be applied to other performance metric, for example, \|V^π(s)−Vπ(s)\|, where V^π is the estimate you get from a policy evaluation problem.

**Questions:**
1. From Corollary 1, the sample complexity of PILOT is O(Mκ3ϵ−1\+M), where M is the number of state\-action pairs sampled by the evaluated policy, and ϵ measures the error under the new metric of convergence performance in this paper. Intuitively, to get a accurate estimate of the Vπ, we need a sufficient number of samples (a big M). However, it seems that this ϵ has nothing to do with M. Additionally, I have noticed that the Assumption 1 needs M to be sufficiently large. Can authors give the detailed justification of this explanation? I would like to see how M will affect the accuracy of the policy evaluation.
2. For the sample complexity of the algorithm, the first term O(Mκ3ϵ−1) seems redundant, because the total number of samples is fixed, i.e., M, and in this paper the first term of sample complexity comes from sampling from this dataset, and this operation does not increase the sample complexity (it will not interact with the environment). Therefore, I think PILOT\+ accually saves the computational cost, not sample complexity of PILOT. Can authors explain this concept more carefully?

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
6: marginally above the acceptance threshold

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 16
**Author:** Authors

**Comment:**
Thank you for your valuable feedback and comments. Our point\-to\-point responses are as follows:



> **Your Comment 1:** Since the paper claims the algorithms they propose achieve the first convergence rate O(1/K) (K is the number of iterations) with constant step\-sizes for PE with nonlinear function approximation, it is better to give some brief statistical intuition of achieving this result.


**Our Response:** Thanks for your suggestions. The intuitions of our method achieving the O(1/K) convergence rate for reinforcement learning (RL) policy evaluation (PE) with nonlinear function approximation are summarized as follows:


**1\) Variance Reduction:** The key idea of our approach to achieve a fast convergence is to utilize the state\-of\-the\-art recursive path\-integrated variance reduction (VR) technique. Specifically, in RL environments, there is inherent randomness due to the stochastic nature of actions and rewards. Our recursive path\-integrated VR helps stabilize the learning process by reducing the impact of this randomness. It effectively mitigates the noise introduced by the stochasticity in RL by periodically evaluating full gradients and using fresh information by using previous iterates. Our proposed VR technique makes the optimization trajectory much smoother. 


We would also like to highlight that similar VR techniques have been adopted in traditional simple minimization optimization problems (e.g., \[Fang et al., 2018] and \[Wang et al., 2019]). These works showed that recursive path\-integrated VR techniques achieve an O(1/K) convergence rate for simple minimization. In this paper, we show that a similar recursive path\-integrated VR technique can be applied to the MSPBE\-based RL PE problem, which has a far more complex min\-max structure.


**2\) Constant Step\-Sizes and Convergence:** The use of constant step\-sizes also plays an essential in achieving an O(1/K) convergence rate because they allow for consistent and steady improvement of the objective function value. However, using constant step\-sizes in stochastic environments is challenging due to the fluctuating nature of stochastic gradients, which often necessitates diminishing step\-sizes to avoid oscillations or even divergence. Thanks to the smoothed trajectory resulting from our proposed recursive path\-integrated VR technique, we show that the use of constant step\-sizes becomes possible without compromising the rate of convergence.




---



> **Your Comment 2:** The paper proposes a new metric for convergence performance, and gives the abundant explanation for using this concept, but it is hard to be applied to other performance metric, for example, \|V^π(s)−Vπ(s)\|, where V^π is the estimate you get from a policy evaluation problem.


**Our Response:** Thank you for your valuable feedback regarding the convergence metric M(k) used in our paper. We appreciate your suggested performance metric, i.e., the absolute error between the estimated and actual value functions in policy evaluation, \|V^π(s)−Vπ(s)\|. However, evaluating \|V^π(s)−Vπ(s)\| is intractable in our RL PE problem, because the MSPBE\-based PE problem is a non\-convex min\-max problem, which implies that computing \|V^π(s)−Vπ(s)\| is NP\-hard. Therefore, just as most first\-order methods for non\-convex optimization in the literature, convergence to a stationary point is our algorithm design goal for MSPBE\-based RL PE, hence we use our proposed performance metric.


Specifically, our proposed metric M(k) is designed to provide a comprehensive measure of convergence in the complex context of non\-convex optimization with RL policy evaluation. It comprises two components: the first term \|J(θ)\|2 in Eq. (6\) measures the convergence of the primal variable θ to a first\-order stationary point, reflecting the accuracy of the policy parameterization. In the second term, we can directly assess the dual solution distance to the unique maximizer under any given primal solution, i.e., \|ω−ω∗(θ)\| thanks to the strong concavity.


In summary, although the suggested metric \|V^π(s)−Vπ(s)\| is a direct measure of the value function error, it is computationally intractable to use in our convergence and sample complexity analysis. On the other hand, our proposed new metric allows us to prove a O(1/K) convergence rate for our PILOT algorithms, which is the first such result in the literture. We hope this explanation clarifies the rationale behind our choice of convergence metric and its relation to other performance measures in the field.


### Official Comment 17
**Author:** Authors

**Comment:**
> **Your Comment 3:** From Corollary 1, the sample complexity of PILOT is O(Mκ3ϵ−1\+M), where M is the number of state\-action pairs sampled by the evaluated policy, and ϵ measures the error under the new metric of convergence performance in this paper. Intuitively, to get a accurate estimate of the Vπ, we need a sufficient number of samples (a big M ). However, it seems that this ϵ has nothing to do with M. Additionally, I have noticed that the Assumption 1 needs M to be sufficiently large. Can authors give the detailed justification of this explanation? I would like to see how M will affect the accuracy of the policy evaluation.


**Our Response:** Thanks for your comments. However, it appears that there are some misunderstandings regarding the notations ϵ and M, as well as the terminology "sample complexity." Here, we would like to further clarify as follows:


1. **The dataset size M:** The reviewer is correct that the larger the value of M, the more accurate policy evaluation one can obtain for the value function Vπ. However, in the RL PE literature (e.g., \[Wai et al. (2019\), Qiu et al. (2020\), Du et al. (2017\)] and also in our work), the goal is *not* to determine how large M should be. Rather, the RL PE problem setting assumes that the dataset of the M\-step trajectory is already sampled and provided, i.e., the M\-value is **fixed** and independent of the convergence error ϵ (more on ϵ later). In other words, M is *not* a variable to control in RL PE, and it is given as a fixed parameter.
2. **Justification of M needs to be sufficiently large in Assumption 1:** Although M is a fixed parameter in the RL PE problem, it needs to be sufficiently large so that designing RL PE algorithms with *fast convergence* is possible. That is, a large M is needed in RL PE to allow the development of fast\-convergent PE algorithms (e.g., the O(1/K) convergence rate in our work). Specifically, many convergence analyses for RL PE algorithms in the literature, including ours, require the strong concavity condition in Assumption 1 to hold. To see why a suffciently large M allows in Assumption 1 to hold, recall that D\=Es\[∇θVθ(s)∇θVθ(s)⊤]∈Rd×d, which implies that D is positive semidefnite. Further, as the number of random samples M increases, D becomes more and more likely to be full\-rank, i.e., D becomes positive definite. That is, as M becomes sufficiently large, one can always find a μ\>0 such that μ≤λmin(D). This μ further implies the strong concavity relation stated in Assumption 1\.
3. **The convergence error ϵ:** We want to clarify that, in the RL PE literature, ϵ does *not* represent the accuracy of PE, which is affected by M. Rather, ϵ is a tolerable convergence error under a given convergence metric. In our paper, ϵ is the tolerable error of our proposed convergence metric in Eq. (6\), which captures the stationarity gap of the primal solution θ and the optimality distance of the dual solution ω. Therefore, ϵ is a system parameter that is independent of the dataset size M. Also, it is important to recognize that **a fast convergence to a PE solution does not necessarily mean that this solution has a high PE accuracy**. However, due to the non\-convex nature of the MSPBE\-based min\-max PE with nonlinear function approximation, convergence to a stationary point is typically the algorithm design goal one would pursue.
4. **The notion of sample complexity:** In the RL PE literature, sample complexity does *not* mean the dataset size M we need. Rather, sample complexity is defined as follows (also see the formal definition in our response to your next comment): Given a *fixed* tolerable convergence error ϵ and a *fixed* M\-sized dataset, **how many times of sampling from the dataset** an algorithm needs for gradient estimations, so that the algorithm can converge to within the ϵ\-error. In this paper, we show that the number of sampling from the M\-sized dataset (i.e., sample complexity) is bounded by O(Mκ3ϵ−1\+M), which is the state\-of\-the\-art result in the literature.


We sincerely hope that the above\-detailed explanations can clarify the reviewers' doubts regarding M, ϵ, and the notion of sample complexity.


### Official Comment 18
**Author:** Authors

**Comment:**
> **Your Comment 4:** For the sample complexity of the algorithm, the first term O(Mκ3ϵ−1) seems redundant because the total number of samples is fixed, i.e., M, and in this paper the first term of sample complexity comes from sampling from this dataset, and this operation does not increase the sample complexity (it will not interact with the environment). Therefore, I think PILOT\+ actually saves the computational cost, not the sample complexity of PILOT. Can authors explain this concept more carefully?


**Our Response:** Thanks for your questions. Again, this question is also related to the notion of sample complexity. In our paper, we adopt the sample complexity metric that is widely used in the literature (e.g., \[Luo et al. (2020\); Zhang et al. (2021\); Xu et al. (2020\)]) to measure the efficiency of an algorithm. To avoid confusion, we have added the following definition of sample complexity in our revised paper:


**Definition 1** (Sample Complexity): The sample complexity is defined as the total number of required samplings from the dataset to evaluate incremental first\-order oracle (IFO) until an algorithm converges, where one IFO call evaluates a pair of (Li(θ,ω),∇Li(θ,ω)),i∈\[M].


The reviewer is correct that the term O(Mκ3ϵ−1) in the sample complexity expression reflects the computational effort required to achieve a convergence error of ϵ when the algorithm processes a dataset comprising M state\-action pairs. As mentioned earlier, M represents the total number of samples obtained from the environment, and it is indeed fixed as you correctly pointed out. The reviewer is also correct that there is no interaction with the environment to collect more samples in RL PE. We believe the confusion comes from the terminology "sample complexity," which indeed measures the computational effort. However, to be consistent with the existing RL PE literature, we still adopt this terminology for easy comparisons with earlier works.


Lastly, regarding the sample complexity of our PILOT\+ algorithm, the reduction of sample complexity (i.e., saving of computational effort) stems from the adaptive batch size approach), which eliminates the need for computing full gradients using the entire M\-sized dataset. This leads to a much smaller number of samples from the M\-sized dataset.


### Official Comment 19
**Author:** 


### Official Comment 20
**Author:** Authors

**Comment:**
Thank you for your valuable feedback and comments. Our point\-to\-point responses are as follows:



> **Your Comment 1:** Since the paper claims the algorithms they propose achieve the first convergence rate O(1/K) (K is the number of iterations) with constant step\-sizes for PE with nonlinear function approximation, it is better to give some brief statistical intuition of achieving this result.


**Our Response:** Thanks for your suggestions. The intuitions of our method achieving the O(1/K) convergence rate for reinforcement learning (RL) policy evaluation (PE) with nonlinear function approximation are summarized as follows:


**1\) Variance Reduction:** The key idea of our approach to achieve a fast convergence is to utilize the state\-of\-the\-art recursive path\-integrated variance reduction (VR) technique. Specifically, in RL environments, there is inherent randomness due to the stochastic nature of actions and rewards. Our recursive path\-integrated VR helps stabilize the learning process by reducing the impact of this randomness. It effectively mitigates the noise introduced by the stochasticity in RL by periodically evaluating full gradients and using fresh information by using previous iterates. Our proposed VR technique makes the optimization trajectory much smoother. 


We would also like to highlight that similar VR techniques have been adopted in traditional simple minimization optimization problems (e.g., \[Fang et al., 2018] and \[Wang et al., 2019]). These works showed that recursive path\-integrated VR techniques achieve an O(1/K) convergence rate for simple minimization. In this paper, we show that a similar recursive path\-integrated VR technique can be applied to the MSPBE\-based RL PE problem, which has a far more complex min\-max structure.


**2\) Constant Step\-Sizes and Convergence:** The use of constant step\-sizes also plays an essential in achieving an O(1/K) convergence rate because they allow for consistent and steady improvement of the objective function value. However, using constant step\-sizes in stochastic environments is challenging due to the fluctuating nature of stochastic gradients, which often necessitates diminishing step\-sizes to avoid oscillations or even divergence. Thanks to the smoothed trajectory resulting from our proposed recursive path\-integrated VR technique, we show that the use of constant step\-sizes becomes possible without compromising the rate of convergence.




---



> **Your Comment 2:** The paper proposes a new metric for convergence performance, and gives the abundant explanation for using this concept, but it is hard to be applied to other performance metric, for example, \|V^π(s)−Vπ(s)\|, where V^π is the estimate you get from a policy evaluation problem.


**Our Response:** Thank you for your valuable feedback regarding the convergence metric M(k) used in our paper. We appreciate your suggested performance metric, i.e., the absolute error between the estimated and actual value functions in policy evaluation, \|V^π(s)−Vπ(s)\|. However, evaluating \|V^π(s)−Vπ(s)\| is intractable in our RL PE problem, because the MSPBE\-based PE problem is a non\-convex min\-max problem, which implies that computing \|V^π(s)−Vπ(s)\| is NP\-hard. Therefore, just as most first\-order methods for non\-convex optimization in the literature, convergence to a stationary point is our algorithm design goal for MSPBE\-based RL PE, hence we use our proposed performance metric.


Specifically, our proposed metric M(k) is designed to provide a comprehensive measure of convergence in the complex context of non\-convex optimization with RL policy evaluation. It comprises two components: the first term \|J(θ)\|2 in Eq. (6\) measures the convergence of the primal variable θ to a first\-order stationary point, reflecting the accuracy of the policy parameterization. In the second term, we can directly assess the dual solution distance to the unique maximizer under any given primal solution, i.e., \|ω−ω∗(θ)\| thanks to the strong concavity.


In summary, although the suggested metric \|V^π(s)−Vπ(s)\| is a direct measure of the value function error, it is computationally intractable to use in our convergence and sample complexity analysis. On the other hand, our proposed new metric allows us to prove a O(1/K) convergence rate for our PILOT algorithms, which is the first such result in the literture. We hope this explanation clarifies the rationale behind our choice of convergence metric and its relation to other performance measures in the field.


### Official Comment 21
**Author:** Authors

**Comment:**
> **Your Comment 3:** From Corollary 1, the sample complexity of PILOT is O(Mκ3ϵ−1\+M), where M is the number of state\-action pairs sampled by the evaluated policy, and ϵ measures the error under the new metric of convergence performance in this paper. Intuitively, to get a accurate estimate of the Vπ, we need a sufficient number of samples (a big M ). However, it seems that this ϵ has nothing to do with M. Additionally, I have noticed that the Assumption 1 needs M to be sufficiently large. Can authors give the detailed justification of this explanation? I would like to see how M will affect the accuracy of the policy evaluation.


**Our Response:** Thanks for your comments. However, it appears that there are some misunderstandings regarding the notations ϵ and M, as well as the terminology "sample complexity." Here, we would like to further clarify as follows:


1. **The dataset size M:** The reviewer is correct that the larger the value of M, the more accurate policy evaluation one can obtain for the value function Vπ. However, in the RL PE literature (e.g., \[Wai et al. (2019\), Qiu et al. (2020\), Du et al. (2017\)] and also in our work), the goal is *not* to determine how large M should be. Rather, the RL PE problem setting assumes that the dataset of the M\-step trajectory is already sampled and provided, i.e., the M\-value is **fixed** and independent of the convergence error ϵ (more on ϵ later). In other words, M is *not* a variable to control in RL PE, and it is given as a fixed parameter.
2. **Justification of M needs to be sufficiently large in Assumption 1:** Although M is a fixed parameter in the RL PE problem, it needs to be sufficiently large so that designing RL PE algorithms with *fast convergence* is possible. That is, a large M is needed in RL PE to allow the development of fast\-convergent PE algorithms (e.g., the O(1/K) convergence rate in our work). Specifically, many convergence analyses for RL PE algorithms in the literature, including ours, require the strong concavity condition in Assumption 1 to hold. To see why a suffciently large M allows in Assumption 1 to hold, recall that D\=Es\[∇θVθ(s)∇θVθ(s)⊤]∈Rd×d, which implies that D is positive semidefnite. Further, as the number of random samples M increases, D becomes more and more likely to be full\-rank, i.e., D becomes positive definite. That is, as M becomes sufficiently large, one can always find a μ\>0 such that μ≤λmin(D). This μ further implies the strong concavity relation stated in Assumption 1\.
3. **The convergence error ϵ:** We want to clarify that, in the RL PE literature, ϵ does *not* represent the accuracy of PE, which is affected by M. Rather, ϵ is a tolerable convergence error under a given convergence metric. In our paper, ϵ is the tolerable error of our proposed convergence metric in Eq. (6\), which captures the stationarity gap of the primal solution θ and the optimality distance of the dual solution ω. Therefore, ϵ is a system parameter that is independent of the dataset size M. Also, it is important to recognize that **a fast convergence to a PE solution does not necessarily mean that this solution has a high PE accuracy**. However, due to the non\-convex nature of the MSPBE\-based min\-max PE with nonlinear function approximation, convergence to a stationary point is typically the algorithm design goal one would pursue.
4. **The notion of sample complexity:** In the RL PE literature, sample complexity does *not* mean the dataset size M we need. Rather, sample complexity is defined as follows (also see the formal definition in our response to your next comment): Given a *fixed* tolerable convergence error ϵ and a *fixed* M\-sized dataset, **how many times of sampling from the dataset** an algorithm needs for gradient estimations, so that the algorithm can converge to within the ϵ\-error. In this paper, we show that the number of sampling from the M\-sized dataset (i.e., sample complexity) is bounded by O(Mκ3ϵ−1\+M), which is the state\-of\-the\-art result in the literature.


We sincerely hope that the above\-detailed explanations can clarify the reviewers' doubts regarding M, ϵ, and the notion of sample complexity.


### Official Comment 22
**Author:** Authors

**Comment:**
> **Your Comment 4:** For the sample complexity of the algorithm, the first term O(Mκ3ϵ−1) seems redundant because the total number of samples is fixed, i.e., M, and in this paper the first term of sample complexity comes from sampling from this dataset, and this operation does not increase the sample complexity (it will not interact with the environment). Therefore, I think PILOT\+ actually saves the computational cost, not the sample complexity of PILOT. Can authors explain this concept more carefully?


**Our Response:** Thanks for your questions. Again, this question is also related to the notion of sample complexity. In our paper, we adopt the sample complexity metric that is widely used in the literature (e.g., \[Luo et al. (2020\); Zhang et al. (2021\); Xu et al. (2020\)]) to measure the efficiency of an algorithm. To avoid confusion, we have added the following definition of sample complexity in our revised paper:


**Definition 1** (Sample Complexity): The sample complexity is defined as the total number of required samplings from the dataset to evaluate incremental first\-order oracle (IFO) until an algorithm converges, where one IFO call evaluates a pair of (Li(θ,ω),∇Li(θ,ω)),i∈\[M].


The reviewer is correct that the term O(Mκ3ϵ−1) in the sample complexity expression reflects the computational effort required to achieve a convergence error of ϵ when the algorithm processes a dataset comprising M state\-action pairs. As mentioned earlier, M represents the total number of samples obtained from the environment, and it is indeed fixed as you correctly pointed out. The reviewer is also correct that there is no interaction with the environment to collect more samples in RL PE. We believe the confusion comes from the terminology "sample complexity," which indeed measures the computational effort. However, to be consistent with the existing RL PE literature, we still adopt this terminology for easy comparisons with earlier works.


Lastly, regarding the sample complexity of our PILOT\+ algorithm, the reduction of sample complexity (i.e., saving of computational effort) stems from the adaptive batch size approach), which eliminates the need for computing full gradients using the entire M\-sized dataset. This leads to a much smaller number of samples from the M\-sized dataset.


### Official Comment 23
**Author:** 


### Official Review 24
**Author:** Reviewer b5y9

**Summary:**
This paper introduces a new algorithm (PILOT) to estimate value function with non\-linear function approximation. Under appropriate choices of step sizes, the algorithm achieves O(1/K) error after K iterations.

**Soundness:**
3 good

**Presentation:**
3 good

**Contribution:**
3 good

**Strengths:**
* The paper is well\-written and easy to follow. The literature review is quite complete.
* The results are interesting and the author adequately motivate the problem.
* The numerical experiments are convincing (although they could be polished, see below).

**Weaknesses:**
* No significant weakness. See my questions below.

**Questions:**
* What is K in the paragraph before the questions “ can we develop … ” on page 2? Suppose this the K defined after the question. In that case, the phrasing “ more than O(K) number of iterations to achieve the convergence ” seem to suggests that the algorithm terminates with the exact value function after O(K) iterations, which is probably not the case. Please clarify.
* Point (ii), paragraph (2\) of the literature reivew: “our algorithms only require the stepsizes to be sufficiently small, which is easier to tune in practice” —this is not very clear, what does sufficiently small ? In the previous paragraph a method with O(1/M) step size is criticized so the authors need to be more accurate here.
* Paragraph 1, Section 3: The notation π:S→A is only for deterministic policies. Please introduce randomized policies properly.
* Algorithm 1 refers to Eq. (4\) and Eq. (5\) who appear a page later.
* Why do the authors use arrows\+name for Figures 1\-4 and not just a legend?

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
8: accept, good paper

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 25
**Author:** Authors

**Comment:**
Thank you for your valuable feedback. Our point\-to\-point responses are as follows:



> **Your Comment 1:** What is K in the paragraph before the questions " can we develop ... " on page 2 ? Suppose this the K defined after the question. In that case, the phrasing " more than O(K) number of iterations to achieve the convergence " seem to suggests that the algorithm terminates with the exact value function after O(K) iterations, which is probably not the case. Please clarify.


**Our Response:** Thanks for your comments and questions. Here, we clarify that K is the number of iterations an algorithm runs. We will revise the paper and define K earlier, ensuring that it is clearly and unambiguously explained before its first significant use in the text. 


Additionally, in the revision, we will rewrite and refine the sentence to avoid similar future confusion. In the revision, the sentence "...more than O(K) number of iterations to achieve convergence" will be changed to "...achieving convergence rate slower than O(1/K)."




---



> **Your Comment 2:** Point (ii), paragraph (2\) of the literature reivew: "our algorithms only require the stepsizes to be sufficiently small, which is easier to tune in practice" \-this is not very clear, what does sufficiently small ? In the previous paragraph a method with O(1/M) step size is criticized so the authors need to be more accurate here.


 **Our Response:** Thanks for your comments. Note that many existing works in the reinforcement learning (RL) policy evaluation (PE) literature require sophisticated problem instance information for setting step sizes. For example, setting the step\-size in the SREDA algorithm in \[Luo et al. 2020] requires the knowledge of the condition number κ, which is hard to estimate in practice. In comparison, our PILOT and PILOT\+ algorithms only require the step size to be a sufficiently small constant and do not need the exact values of the parameters Lf and μ. 


Specifically, our Theorems 1 and 2 demonstrate that, as long as the step\-sizes α and β are smaller than the upper bounds stated in these theorems, the O(1/K) convergence rate of our algorithms is achieved. The phrase "sufficiently small" just means smaller than the upper bounds we provided in the theorems. Our approach does *not* need the exact knowledge of problem instance information, making the step\-size setting more convenient in practice.


Lastly, regarding the algorithm in \[Wai, et al, 2019], their best convergence results only hold for a small step\-size that is O(1/M), where M denotes the size of the dataset. That is, the step\-size setting is *dependent* on the dataset size M. This is problematic for RL problems with a large state\-action transition dataset size M. In contrast, the choices of step sizes in our paper are **independent** of the size of the dataset. 


In this revision, to address your concerns and to avoid similar confusion in the future, we revise this sentence and clearly define what constitutes "sufficiently small" in our paper. 




---



> **Your Comment 3:** Paragraph 1, Section 3: The notation π:S→A is only for deterministic policies. Please introduce randomized policies properly.


**Our Response:** Thank you for pointing out this confusion. In the revised paper, we will change our notation to precisely define policies that could be either deterministic or randomized. The revised notation is as follows: π(a\|s):S×A→\[0,1], where π(a\|s) is the probability distribution of taking an action a from the action space A given a state s in the state space S. The deterministic policy corresponds to the special case where the probability values can only be 0 or 1\.




---



> **Your Comment 4:** Algorithm 1 refers to Eq. (4\) and Eq. (5\) who appear a page later.


**Our Response:** Thank you for pointing out this issue. This is caused by the floating of the algorithm environment in LaTeX, which was overlooked in our initial submission. In the revised paper, we have fixed this problem and placed Eq. (4\), Eq. (5\), and the algorithm on the same page. 




---



> **Your Comment 5:** Why do the authors use arrows\+name for Figures 1−4 and not just a legend?


**Our Response:** Thanks for your question. The reason of using arrows\+name is to create an immediate visual association between the algorithm and the specific experimental result in the figure.


### Official Comment 26
**Author:** Authors

**Comment:**
Thank you for your valuable feedback. Our point\-to\-point responses are as follows:



> **Your Comment 1:** What is K in the paragraph before the questions " can we develop ... " on page 2 ? Suppose this the K defined after the question. In that case, the phrasing " more than O(K) number of iterations to achieve the convergence " seem to suggests that the algorithm terminates with the exact value function after O(K) iterations, which is probably not the case. Please clarify.


**Our Response:** Thanks for your comments and questions. Here, we clarify that K is the number of iterations an algorithm runs. We will revise the paper and define K earlier, ensuring that it is clearly and unambiguously explained before its first significant use in the text. 


Additionally, in the revision, we will rewrite and refine the sentence to avoid similar future confusion. In the revision, the sentence "...more than O(K) number of iterations to achieve convergence" will be changed to "...achieving convergence rate slower than O(1/K)."




---



> **Your Comment 2:** Point (ii), paragraph (2\) of the literature reivew: "our algorithms only require the stepsizes to be sufficiently small, which is easier to tune in practice" \-this is not very clear, what does sufficiently small ? In the previous paragraph a method with O(1/M) step size is criticized so the authors need to be more accurate here.


 **Our Response:** Thanks for your comments. Note that many existing works in the reinforcement learning (RL) policy evaluation (PE) literature require sophisticated problem instance information for setting step sizes. For example, setting the step\-size in the SREDA algorithm in \[Luo et al. 2020] requires the knowledge of the condition number κ, which is hard to estimate in practice. In comparison, our PILOT and PILOT\+ algorithms only require the step size to be a sufficiently small constant and do not need the exact values of the parameters Lf and μ. 


Specifically, our Theorems 1 and 2 demonstrate that, as long as the step\-sizes α and β are smaller than the upper bounds stated in these theorems, the O(1/K) convergence rate of our algorithms is achieved. The phrase "sufficiently small" just means smaller than the upper bounds we provided in the theorems. Our approach does *not* need the exact knowledge of problem instance information, making the step\-size setting more convenient in practice.


Lastly, regarding the algorithm in \[Wai, et al, 2019], their best convergence results only hold for a small step\-size that is O(1/M), where M denotes the size of the dataset. That is, the step\-size setting is *dependent* on the dataset size M. This is problematic for RL problems with a large state\-action transition dataset size M. In contrast, the choices of step sizes in our paper are **independent** of the size of the dataset. 


In this revision, to address your concerns and to avoid similar confusion in the future, we revise this sentence and clearly define what constitutes "sufficiently small" in our paper. 




---



> **Your Comment 3:** Paragraph 1, Section 3: The notation π:S→A is only for deterministic policies. Please introduce randomized policies properly.


**Our Response:** Thank you for pointing out this confusion. In the revised paper, we will change our notation to precisely define policies that could be either deterministic or randomized. The revised notation is as follows: π(a\|s):S×A→\[0,1], where π(a\|s) is the probability distribution of taking an action a from the action space A given a state s in the state space S. The deterministic policy corresponds to the special case where the probability values can only be 0 or 1\.




---



> **Your Comment 4:** Algorithm 1 refers to Eq. (4\) and Eq. (5\) who appear a page later.


**Our Response:** Thank you for pointing out this issue. This is caused by the floating of the algorithm environment in LaTeX, which was overlooked in our initial submission. In the revised paper, we have fixed this problem and placed Eq. (4\), Eq. (5\), and the algorithm on the same page. 




---



> **Your Comment 5:** Why do the authors use arrows\+name for Figures 1−4 and not just a legend?


**Our Response:** Thanks for your question. The reason of using arrows\+name is to create an immediate visual association between the algorithm and the specific experimental result in the figure.


