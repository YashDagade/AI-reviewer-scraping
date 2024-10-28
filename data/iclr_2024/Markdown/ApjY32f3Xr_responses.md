## Reviewer Responses

### Decision 1
**Author:** Program Chairs

**Decision:**
Reject


### Meta Review 2
**Author:** Area Chair f6oV

**Metareview:**
There was one very critical review, in which it was criticised that there is no clear methodological contribution in this paper. Other reviewers had a slightly more positive impression of this paper, putting more emphasis on the experimental and benchmark character of this work. After the rebuttal and discussion phase, however, I still think that the lacking novelty on the conceptual side is indeed a severe weakness of this paper, which could not be compensated by the experimental studies: In my opinion, the conclusions drawn from the benchmark experiments seem to be somewhat limited regarding truly novel insights into PINNs. Therefore I recommend rejection of this paper.

**Justification For Why Not Higher Score:**
This is mainly an experimental/benchmarking paper, but the experimental results did not lead to fundamentally new insights.

**Justification For Why Not Lower Score:**
N/A


### Official Review 3
**Author:** Reviewer Ytqc

**Summary:**
This paper provides both a collection of benchmark datasets as well as a standardized suite of PINN\-type neural network PDE solution approximators arranged as a python package.


It further shows benchmark numbers of the different PINN methods on the benchmark datasets.

**Soundness:**
3 good

**Presentation:**
3 good

**Contribution:**
3 good

**Strengths:**
Providing any meaningful benchmark to the community is a valuable service.
In addition to creating the benchmark data sets, the authors have made a big effort in collecting and unifying PINN methods into a unified framework.
The paper appendix contains detailed specifications about the particular setup for the data benchmark.

**Weaknesses:**
While providing a benchmark data set to the community is a valuable service, several aspects could be improved.


Minor: 
\-It would be great to have a table or list (in the appendix) detailing a comparison of the provided data sets to those in PDEarena (and PDEbench).


Major: 


* The relative error values in the results tables are for the most part shockingly bad and simply not useful for many numerical analysis contexts. Given that PINNs seem to be mostly providing different function spaces for PDE solutions, one original base PINN should be included in the benchmark, which is to give each hat function on a finite element mesh one parameter, and hence include finite element methods. Because some of the data sets were created using FEM, the original mesh would yield 0 error, but different meshes may not, and in particular coarser meshes would accumulate error. Analyzing a curve of remeshing from same resolution to coarse would provide a baseline for the performances of the other PINNs.
* In the above sense, it also becomes important to quantify flop counts. It appears that most PINNs need to be fitted for each PDE solution, incurring the typically high flop count of solving an optimization problem (compared to one forward pass), and only some of them can learn solutions conditional on hyperparameters given as input and require only forward passes to solve e.g. from different inital conditions.
For all cases, there should be 3 different flop counts provided: 1\) The number of flops required to create the training set 2\) The number of flops required for any general training of the method 3\) the number of flops required to evaluate/fit the method on a particular example. Many PINNs, and the FEM baseline would only have nonzero counts in point 3, and it would be good to compare them.
Having flop counts or even wall time counts would allow answering questions like "at equal error rate, does fitting a PINN or fitting FEM cost more computational power?" and "At equal computing power, can FEM beat the error rates of the listed PINNs?"
* continuing the discussion about flop counts, methods learning from multiple data sets/examples should be included in order to compare flop counts and provide additional reference error values. In particular for the time propagating PDEs, solutions using U\-nets or FNOs from e.g. PDE bench should be included as reference values, in terms of performance, flops required for training, flops required to generate the required training data, and flops required to run a forward pass to obtain a solution. Then one can assess how many PINNs or FEM solutions one can compute for the same budget as a certain number of forward passes of the propagator network. The should be a break\-even point at some number of forward passes justifying the training effort.


Without these points, the benchmark is unfortunately sitting just beyond actual widespread utility. I would highly encourage the authors to add these baselines to make the benchmark useful. Despite my positive bias towards benchmarking efforts I cannot recommend acceptance of this paper in its current state.

**Questions:**
Would it be possible to address the major issues listed above among weaknesses?

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
Dear Reviewer Ytqc,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions. 


**Q1\.** The relative error values in the results tables are for the most part shockingly bad and simply not useful for many numerical analysis contexts.


**A1\.** In the experiments presented in this paper, a variety of metrics such as L2RE, L1RE, MSE, and Fourier error at different frequencies were employed to demonstrate the discrepancies between the predicted solutions and the true solutions. Importantly, the poor performance of L2RE in certain tasks is attributed to the deliberate selection of PDEs with varying degrees of difficulty. For instance, NS2d\-LT and Heat2d\-LT highlight the current challenges in mitigating error accumulation over long durations in PINNs, thereby drawing attention to this issue. Moreover, most PINN\-related studies compare L2RE in their results; hence, our utilization of L2RE as a primary criterion facilitates a more effective comparison with other research findings.


**Q2\.** Analyzing a curve of remeshing from the same resolution to coarse.


**A2\.** Firstly, PINNs are not purely data\-driven machine learning methods; they do not require a training set. Thus, even using original FEM grid points does not reduce the error to zero at these points. Secondly, we present the trend of L2RE variation with increasing grid points (corresponding to batch size) in **Table 15** and **Figure 2**, accompanied by an analysis in the main text.


**Q3\.** On using PINNs to predict FEM's hat function.


**A3\.** We believe that combining the strengths of PINNs and FEM in this manner could be an interesting approach worthy of in\-depth investigation. However, as a benchmark, comparing this currently nascent method falls outside the scope of this paper. We anticipate considering its inclusion in our comparisons once more detailed related research is published in the future.


**Q4\.** Calculation of FLOPS.


**A4\.** We have listed the training and inference FLOPs of different methods across various PDEs in the **Table 13, Table 16, Appendix E.1**. As for the flops for data generation in main experiments, we only generate FEM solution for evaluating different approaches on a single instance per PDE. Thus the cost is negligible as we do not need parametric data like PDEBench. 


**Q5\.** Comparison with methods like U\-Net, FNO, etc.


**A5\.** In all our experimental settings for positive PDE problems, no data was provided; we sought to solve using PINNs solely based on the PDE itself. In contrast, neural operator methods such as FNO and U\-Net are data\-driven and, thus, are not applicable to our problem settings.


**Q6\.** Comparing datasets and PDEs with those used in PDEBench/PDEArena.


**A6\.** The PDEs we selected are not significantly related to those chosen in PDEBench or PDEArena. PDEBench and PDEArena primarily focus on time\-dependent PDEs like compressible Naiver\-Stokes equations, Diffusion Reaction equations, etc. Moreover, their complexity is such that PINNs often fail to solve them correctly or yield substantial errors. Our selection of PDEs, derived from various PINN publications, encompasses a diverse range of types and complexities. For common PDEs, we selected the incompressible Naiver\-Stokes equation and the Poisson equation (Darcy flow) due to their representativeness and widespread applicability in numerous fields.


### Official Comment 5
**Author:** Authors

**Comment:**
Dear reviewer Ytqc,


We are wondering if our response and revision have resolved your concerns. In the revised version and rebuttal responses, we have conducted experiments like flops computation and revised our manuscript. If our response has addressed your concerns, we would highly appreciate it if you could re\-evaluate our work and consider raising the score.


If you have any additional questions or suggestions, we would be happy to have further discussions.


Best regards,


authors


### Official Comment 6
**Author:** Reviewer Ytqc

**Comment:**
> A6\. The PDEs we selected are not significantly related to those chosen in PDEBench or PDEArena.


There is overlap (e.g. Burgers' equation), so this statement is False, unless Burgers' equation is not significant. My suggestion was to add a table in the appendix to highlight the differences between the data sets. This was in an effort to help the authors point out the gap that they are filling by introducing this data set ...



> Q2\. Analyzing a curve of remeshing from the same resolution to coarse.



> A2\. Firstly, PINNs are not purely data\-driven machine learning methods; they do not require a training set. Thus, even using original FEM grid points does not reduce the error to zero at these points.


I do not understand this response. The point here was to have a baseline that shows how FEM using coarser and coarser grids fares and can lead to a plot of compute power vs error that should be at minimum attained by PINN methods before they can be considered useful



> A3\. We believe that combining the strengths of PINNs and FEM in this manner could be an interesting approach worthy of in\-depth investigation.


As above, the idea was to include FEM as a baseline. By "base PINN" I mean one where each FEM hat function receives a parameter and the solution is obtained using a sparse matrix solve, i.e. the FEM method.


I feel uneasy about this contribution because it artificially creates boundaries to other existing methods thereby avoiding comparison. If you propose a data set, why restrict it to PINNs? I will increase my score, because having more data sets available is a good thing, but am generally unhappy with the way it is presented.


### Official Comment 7
**Author:** Authors

**Comment:**
Dear Reviewer Ytqc,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions. 


**Q1\.** The relative error values in the results tables are for the most part shockingly bad and simply not useful for many numerical analysis contexts.


**A1\.** In the experiments presented in this paper, a variety of metrics such as L2RE, L1RE, MSE, and Fourier error at different frequencies were employed to demonstrate the discrepancies between the predicted solutions and the true solutions. Importantly, the poor performance of L2RE in certain tasks is attributed to the deliberate selection of PDEs with varying degrees of difficulty. For instance, NS2d\-LT and Heat2d\-LT highlight the current challenges in mitigating error accumulation over long durations in PINNs, thereby drawing attention to this issue. Moreover, most PINN\-related studies compare L2RE in their results; hence, our utilization of L2RE as a primary criterion facilitates a more effective comparison with other research findings.


**Q2\.** Analyzing a curve of remeshing from the same resolution to coarse.


**A2\.** Firstly, PINNs are not purely data\-driven machine learning methods; they do not require a training set. Thus, even using original FEM grid points does not reduce the error to zero at these points. Secondly, we present the trend of L2RE variation with increasing grid points (corresponding to batch size) in **Table 15** and **Figure 2**, accompanied by an analysis in the main text.


**Q3\.** On using PINNs to predict FEM's hat function.


**A3\.** We believe that combining the strengths of PINNs and FEM in this manner could be an interesting approach worthy of in\-depth investigation. However, as a benchmark, comparing this currently nascent method falls outside the scope of this paper. We anticipate considering its inclusion in our comparisons once more detailed related research is published in the future.


**Q4\.** Calculation of FLOPS.


**A4\.** We have listed the training and inference FLOPs of different methods across various PDEs in the **Table 13, Table 16, Appendix E.1**. As for the flops for data generation in main experiments, we only generate FEM solution for evaluating different approaches on a single instance per PDE. Thus the cost is negligible as we do not need parametric data like PDEBench. 


**Q5\.** Comparison with methods like U\-Net, FNO, etc.


**A5\.** In all our experimental settings for positive PDE problems, no data was provided; we sought to solve using PINNs solely based on the PDE itself. In contrast, neural operator methods such as FNO and U\-Net are data\-driven and, thus, are not applicable to our problem settings.


**Q6\.** Comparing datasets and PDEs with those used in PDEBench/PDEArena.


**A6\.** The PDEs we selected are not significantly related to those chosen in PDEBench or PDEArena. PDEBench and PDEArena primarily focus on time\-dependent PDEs like compressible Naiver\-Stokes equations, Diffusion Reaction equations, etc. Moreover, their complexity is such that PINNs often fail to solve them correctly or yield substantial errors. Our selection of PDEs, derived from various PINN publications, encompasses a diverse range of types and complexities. For common PDEs, we selected the incompressible Naiver\-Stokes equation and the Poisson equation (Darcy flow) due to their representativeness and widespread applicability in numerous fields.


### Official Comment 8
**Author:** Authors

**Comment:**
Dear reviewer Ytqc,


We are wondering if our response and revision have resolved your concerns. In the revised version and rebuttal responses, we have conducted experiments like flops computation and revised our manuscript. If our response has addressed your concerns, we would highly appreciate it if you could re\-evaluate our work and consider raising the score.


If you have any additional questions or suggestions, we would be happy to have further discussions.


Best regards,


authors


### Official Comment 9
**Author:** Reviewer Ytqc

**Comment:**
> A6\. The PDEs we selected are not significantly related to those chosen in PDEBench or PDEArena.


There is overlap (e.g. Burgers' equation), so this statement is False, unless Burgers' equation is not significant. My suggestion was to add a table in the appendix to highlight the differences between the data sets. This was in an effort to help the authors point out the gap that they are filling by introducing this data set ...



> Q2\. Analyzing a curve of remeshing from the same resolution to coarse.



> A2\. Firstly, PINNs are not purely data\-driven machine learning methods; they do not require a training set. Thus, even using original FEM grid points does not reduce the error to zero at these points.


I do not understand this response. The point here was to have a baseline that shows how FEM using coarser and coarser grids fares and can lead to a plot of compute power vs error that should be at minimum attained by PINN methods before they can be considered useful



> A3\. We believe that combining the strengths of PINNs and FEM in this manner could be an interesting approach worthy of in\-depth investigation.


As above, the idea was to include FEM as a baseline. By "base PINN" I mean one where each FEM hat function receives a parameter and the solution is obtained using a sparse matrix solve, i.e. the FEM method.


I feel uneasy about this contribution because it artificially creates boundaries to other existing methods thereby avoiding comparison. If you propose a data set, why restrict it to PINNs? I will increase my score, because having more data sets available is a good thing, but am generally unhappy with the way it is presented.


### Official Review 10
**Author:** Reviewer RGvf

**Summary:**
This paper provides a comprehensive comparison of PINN training methods, problems, and data. The paper visits common problems with training PINNs, namely the complex geometry, the multi\-scale phenomena, nonlinearity of some PDE ofrs, and the high dimensional PDE problems. They also provide various training mechanisms such as domain decomposition and loss reweighting methods.

**Soundness:**
4 excellent

**Presentation:**
4 excellent

**Contribution:**
4 excellent

**Strengths:**
1. The paper is well\-written; it seems obvious this work has gone through a few rounds of polishing and review.
2. The literature review is detailed and comprehensive.
3. The challenging aspects of training PINNs are decomposed and categorized well.
4. The appendix section of the paper is thorough and contains quality information.
5. The suite of experiments is admittedly comprehensive; there are more than 20 PDE forms, 10 methods considered and compartmentalized well in this paper.
6. The scale of the experiments and the analyses of the hyper\-parameters is certainly admirable.

**Weaknesses:**
1. I'm saying out of respect to the author's work, but this paper may be more suited for a journal format. In particular, the page limit constraint is hitting the work hard in my opinion.


* By the time the authors present the data and experiments, there is less than half a page left to interpret the results and provide discussions and conclusions.
* Many key discussions, at different points in the main text, were deferred to the appendix. While they do exist in the appendix and carry out important information, they carry more scientific content than the existing paper's text.


To be clear, the paper's topic is certainly relevant to ICLR and could benefit the ICLR community. However, the conference format may not be the most suitable to present the work as best as it could have been.


2. The work utilizes 10 different methods for training PINNs, but a brief description of these methods in a single mathematical framework is missing. Adding such a description and correlating the numerical findings to the theoretical properties of each method is probably the most important, yet under\-performed, part of the work in my opinion.


 To be clear, I understand the paper's space constraints, but this is very important in my opinion. The least the authors could do is to add such a section, however briefly, to the appendix.

**Questions:**
See the weaknesses section.

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
6: marginally above the acceptance threshold

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 11
**Author:** Authors

**Comment:**
Dear Reviewer RGvf,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions.


**Q1\.** The conference format may not be the most suitable to present the work.


**A1\.** We acknowledge your concern regarding the format constraints. Due to space limitations, a considerable portion of our results and discussions had to be relegated to the appendix, which might inconvenience readers. However, it's worth noting that at the ICLR conference, many benchmark articles are accepted annually \[1, 2, 3, 4]. Furthermore, the main conclusions of our article are presented in the main text, with the appendix serving primarily to supplement and corroborate these findings.


**Q2\.** A brief description of these methods in a single mathematical framework is missing.


**A2\.** Thank you for your valuable suggestion. It is important to note that different methods contribute to the improvement of PINNs in varied ways, hence we categorized these methods and described each category within a unified framework. Due to constraints in the main text's length, we have included these descriptions in an additional section denoted as **Appendix B.4**.


**References**


1. EAGLE: Large\-scale Learning of Turbulent Fluid Dynamics with Mesh Transformers ([https://openreview.net/forum?id\=mfIX4QpsARJ](https://openreview.net/forum?id=mfIX4QpsARJ)), ICLR 2023,
2. Learned Coarse Models for Efficient Turbulence Simulation ([https://openreview.net/forum?id\=msRBojTz\-Nh](https://openreview.net/forum?id=msRBojTz-Nh)), ICLR 2022,
3. SoftZoo: A Soft Robot Co\-design Benchmark For Locomotion In Diverse Environments ([https://openreview.net/forum?id\=Xyme9p1rpZw](https://openreview.net/forum?id=Xyme9p1rpZw)), ICLR 2023,
4. GeneDisco: A Benchmark for Experimental Design in Drug Discovery ([https://openreview.net/forum?id\=\-w2oomO6qgc](https://openreview.net/forum?id=-w2oomO6qgc)), ICLR 2022\.


### Official Comment 12
**Author:** Authors

**Comment:**
Dear Reviewer RGvf,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions.


**Q1\.** The conference format may not be the most suitable to present the work.


**A1\.** We acknowledge your concern regarding the format constraints. Due to space limitations, a considerable portion of our results and discussions had to be relegated to the appendix, which might inconvenience readers. However, it's worth noting that at the ICLR conference, many benchmark articles are accepted annually \[1, 2, 3, 4]. Furthermore, the main conclusions of our article are presented in the main text, with the appendix serving primarily to supplement and corroborate these findings.


**Q2\.** A brief description of these methods in a single mathematical framework is missing.


**A2\.** Thank you for your valuable suggestion. It is important to note that different methods contribute to the improvement of PINNs in varied ways, hence we categorized these methods and described each category within a unified framework. Due to constraints in the main text's length, we have included these descriptions in an additional section denoted as **Appendix B.4**.


**References**


1. EAGLE: Large\-scale Learning of Turbulent Fluid Dynamics with Mesh Transformers ([https://openreview.net/forum?id\=mfIX4QpsARJ](https://openreview.net/forum?id=mfIX4QpsARJ)), ICLR 2023,
2. Learned Coarse Models for Efficient Turbulence Simulation ([https://openreview.net/forum?id\=msRBojTz\-Nh](https://openreview.net/forum?id=msRBojTz-Nh)), ICLR 2022,
3. SoftZoo: A Soft Robot Co\-design Benchmark For Locomotion In Diverse Environments ([https://openreview.net/forum?id\=Xyme9p1rpZw](https://openreview.net/forum?id=Xyme9p1rpZw)), ICLR 2023,
4. GeneDisco: A Benchmark for Experimental Design in Drug Discovery ([https://openreview.net/forum?id\=\-w2oomO6qgc](https://openreview.net/forum?id=-w2oomO6qgc)), ICLR 2022\.


### Official Review 13
**Author:** Reviewer oeuE

**Summary:**
The paper provides a benchmarking tool called PINNacle which was lacking in the domain of PINNs. The tool provides a diverse set of 20 different PDEs spanning over various application domains. The tool also provides implementations of 10 state\-of\-the\-art techniques in PINNs and shows extensive experiments to show the strengths and weaknesses of each method.

**Soundness:**
2 fair

**Presentation:**
4 excellent

**Contribution:**
1 poor

**Strengths:**
1. The paper is overall well written and easy to follow.
2. The paper provides an extensive comparison of the different SOTA methods for different PDEs.

**Weaknesses:**
1. The paper lacks technical novelty to be considered for the main track. In my opinion, the paper is more suitable for an application/dataset track, for e.g., NeurIPS Dataset/Benchmark Track.
2. The insights provided in the paper are not novel and are also well\-known in the PINN literature which the paper cites as well.

**Questions:**
1. Table 3 shows that all of the selected SOTA methods fail on the KS Equation. However, some PINN methods can solve KS Equations such as Causal PINNs \[1].
2. When comparing the effect of the parametric PDEs on different PINN variants (shown in Table 4\), using the Average L2RE is not a good choice. It would be more informative to show the mean and the standard deviations for the different parameter choices. The average L2RE can be skewed if one (or few) of the parameter settings fails (i.e., have L2RE of 100%) while others have very low errors (such as \~1e\-4\).


\[1] Wang, S., Sankaran, S., \& Perdikaris, P. (2022\). Respecting causality is all you need for training physics\-informed neural networks. arXiv preprint arXiv:2203\.07404\.

**Flag For Ethics Review:**
No ethics review needed.

**Details Of Ethics Concerns:**
None

**Rating:**
3: reject, not good enough

**Confidence:**
5: You are absolutely certain about your assessment. You are very familiar with the related work and checked the math/other details carefully.

**Code Of Conduct:**
Yes


### Official Comment 14
**Author:** Authors

**Comment:**
Dear Reviewer oeuE,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions.


**Q1\.** The paper is more suitable for an application/dataset track, for e.g., NeurIPS Dataset/Benchmark Track.


**A1\.** We appreciate your perspective, yet it's pertinent to note that at the ICLR Conference, numerous benchmark and dataset articles are accepted each year, as exemplified by references \[1,2,3,4]. While benchmark articles may not introduce new techniques, they play a crucial role in highlighting existing issues in the field and guiding future research directions. Therefore, we respectfully request that you reconsider the contribution of our paper in this context.


**Q2\.** All of the selected SOTA methods fail on the KS Equation but some PINNs methods could solve it.


**A2\.** CausualPINNs represent a combination of various methods and techniques, and the training parameters and iteration numbers in their original work significantly differ from those in our study. Although their results suggest the resolution of the KS equation, it does not entirely apply under our problem settings. Given the plethora of improvements in PINN methods, we promise to gradually include more widely recognized, published, and effective works in our future research.


**Q3\.** Using averaged L2RE in parametric PDEs experiments is not a good indicator.


**A3\.** Due to the limited space in the main text, we only presented averaged L2RE, but comprehensive statistics, including mean and standard deviation, are provided in the appendix's **Table 27** for reference.


**References**


1. EAGLE: Large\-scale Learning of Turbulent Fluid Dynamics with Mesh Transformers ([https://openreview.net/forum?id\=mfIX4QpsARJ](https://openreview.net/forum?id=mfIX4QpsARJ)), ICLR 2023,
2. Learned Coarse Models for Efficient Turbulence Simulation ([https://openreview.net/forum?id\=msRBojTz\-Nh](https://openreview.net/forum?id=msRBojTz-Nh)), ICLR 2022,
3. SoftZoo: A Soft Robot Co\-design Benchmark For Locomotion In Diverse Environments ([https://openreview.net/forum?id\=Xyme9p1rpZw](https://openreview.net/forum?id=Xyme9p1rpZw)), ICLR 2023,
4. GeneDisco: A Benchmark for Experimental Design in Drug Discovery ([https://openreview.net/forum?id\=\-w2oomO6qgc](https://openreview.net/forum?id=-w2oomO6qgc)), ICLR 2022\.


### Official Comment 15
**Author:** Reviewer oeuE

**Comment:**
I thank the authors for providing clarifications to my questions/comments. I have read the other reviews and the authors' comments and have updated my score accordingly. I have a few follow\-up comments regarding the paper:


1. I would like to thank the authors for pointing out that benchmark papers are accepted at ICLR, which I was not familiar with, and I completely understand the importance of benchmarking for the community. As a side note, two of the four example benchmark papers \[1, 2] mentioned by the authors are not purely benchmarks and they have algorithmic innovations. However, I do appreciate the efforts that the authors have put into this paper for creating a benchmark with diverse PDEs and PINN variants.
2. From reading the other reviews and discussions, I also share the same concern as other reviewers that a journal format might be more suitable for this work as most of the interesting discussion of the results are in the Appendix.
3. As a benchmark study, I feel it would further strengthen the paper if more detailed discussions about the results and the some deeper insights about them are included, as opposed to just reporting the results and suggesting suitable approaches. While I recognize the constraints of the ICLR format in terms of page limits, I believe that an expanded discussion could significantly enhance the paper's impact in the scientific ML community.
4. **Minor Comment:** Although the major focus of this work has been on using PINNs for forward problems, the practical applications on PINNs are mostly for inverse problems which has not been extensively explored in this paper. If the authors are planning to extend the benchmark, it would be great to look into a more diverse set of inverse problems.


### Official Comment 16
**Author:** Authors

**Comment:**
Dear Reviewer oeuE,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions.


**Q1\.** The paper is more suitable for an application/dataset track, for e.g., NeurIPS Dataset/Benchmark Track.


**A1\.** We appreciate your perspective, yet it's pertinent to note that at the ICLR Conference, numerous benchmark and dataset articles are accepted each year, as exemplified by references \[1,2,3,4]. While benchmark articles may not introduce new techniques, they play a crucial role in highlighting existing issues in the field and guiding future research directions. Therefore, we respectfully request that you reconsider the contribution of our paper in this context.


**Q2\.** All of the selected SOTA methods fail on the KS Equation but some PINNs methods could solve it.


**A2\.** CausualPINNs represent a combination of various methods and techniques, and the training parameters and iteration numbers in their original work significantly differ from those in our study. Although their results suggest the resolution of the KS equation, it does not entirely apply under our problem settings. Given the plethora of improvements in PINN methods, we promise to gradually include more widely recognized, published, and effective works in our future research.


**Q3\.** Using averaged L2RE in parametric PDEs experiments is not a good indicator.


**A3\.** Due to the limited space in the main text, we only presented averaged L2RE, but comprehensive statistics, including mean and standard deviation, are provided in the appendix's **Table 27** for reference.


**References**


1. EAGLE: Large\-scale Learning of Turbulent Fluid Dynamics with Mesh Transformers ([https://openreview.net/forum?id\=mfIX4QpsARJ](https://openreview.net/forum?id=mfIX4QpsARJ)), ICLR 2023,
2. Learned Coarse Models for Efficient Turbulence Simulation ([https://openreview.net/forum?id\=msRBojTz\-Nh](https://openreview.net/forum?id=msRBojTz-Nh)), ICLR 2022,
3. SoftZoo: A Soft Robot Co\-design Benchmark For Locomotion In Diverse Environments ([https://openreview.net/forum?id\=Xyme9p1rpZw](https://openreview.net/forum?id=Xyme9p1rpZw)), ICLR 2023,
4. GeneDisco: A Benchmark for Experimental Design in Drug Discovery ([https://openreview.net/forum?id\=\-w2oomO6qgc](https://openreview.net/forum?id=-w2oomO6qgc)), ICLR 2022\.


### Official Comment 17
**Author:** Reviewer oeuE

**Comment:**
I thank the authors for providing clarifications to my questions/comments. I have read the other reviews and the authors' comments and have updated my score accordingly. I have a few follow\-up comments regarding the paper:


1. I would like to thank the authors for pointing out that benchmark papers are accepted at ICLR, which I was not familiar with, and I completely understand the importance of benchmarking for the community. As a side note, two of the four example benchmark papers \[1, 2] mentioned by the authors are not purely benchmarks and they have algorithmic innovations. However, I do appreciate the efforts that the authors have put into this paper for creating a benchmark with diverse PDEs and PINN variants.
2. From reading the other reviews and discussions, I also share the same concern as other reviewers that a journal format might be more suitable for this work as most of the interesting discussion of the results are in the Appendix.
3. As a benchmark study, I feel it would further strengthen the paper if more detailed discussions about the results and the some deeper insights about them are included, as opposed to just reporting the results and suggesting suitable approaches. While I recognize the constraints of the ICLR format in terms of page limits, I believe that an expanded discussion could significantly enhance the paper's impact in the scientific ML community.
4. **Minor Comment:** Although the major focus of this work has been on using PINNs for forward problems, the practical applications on PINNs are mostly for inverse problems which has not been extensively explored in this paper. If the authors are planning to extend the benchmark, it would be great to look into a more diverse set of inverse problems.


### Official Review 18
**Author:** Reviewer xNZs

**Summary:**
The article introduces "PINNacle", a robust benchmark suite tailored for Physics\-Informed Neural Networks (PINNs). This suite boasts a rich assortment of over 20 intricate PDE challenges, complemented by a user\-centric toolbox that houses over 10 of the latest PINN techniques. These techniques are segmented by the authors into categories: loss reweighting, advanced optimizers, unique loss functions, and groundbreaking architectures. An exhaustive analysis is then executed with this benchmark dataset to scrutinize these variations.


Many of the challenges pinpointed in the dataset resonate with a multitude of real\-world scenarios. Thus, the efficacy of a method in tackling these challenges becomes a credible measure of its real\-world utility. To generate the data, the authors employ the FEM solver from COMSOL 6\.0 for intricately geometric problems and the spectral method from Chebfun for the more chaotic issues. This dataset encompasses challenges like the heat equation, Poisson equation, Burgers' equation, Navier\-Stokes equation, among others.


The paper outlines a uniform criteria to gauge the performance of varied PINN techniques across all challenges, promoting a methodical comparison of different tactics. Performance assessment is conducted using various metrics, such as accuracy, convergence rate, and computational prowess. Moreover, the authors shed light on the advantages and limitations of these methods, providing direction for subsequent studies, especially in fields like domain decomposition and loss reweighting.


In essence, the article's merits lie in its crafting of a dataset that mirrors significant challenges confronted by PINNs, establishing a uniform assessment criteria for different PINN approaches, and giving valuable insights on the strengths and pitfalls of these methods. This work undeniably propels the growth of PINNs, igniting further creativity and advancements in this burgeoning domain.

**Soundness:**
3 good

**Presentation:**
3 good

**Contribution:**
2 fair

**Strengths:**
This paper stands out with several merits, accentuating its importance in the realm of Physics\-Informed Neural Networks (PINNs).


To begin with, it offers an all\-encompassing benchmark suite for PINNs, showcasing a varied dataset containing over 20 intricate PDE challenges, supplemented by an accessible toolbox with more than 10 leading PINN techniques. This suite facilitates an organized comparison of multiple approaches and delivers a uniform metric to evaluate the efficacy of various PINN methodologies across tasks.


Next, the authors embark on an in\-depth evaluation using the benchmark dataset to appraise these variations. They measure the performance through multiple indicators such as accuracy, convergence speed, and computational prowess. Their findings elucidate the advantages and pitfalls of these methods, charting a course for prospective studies, especially in areas like domain decomposition and loss reweighting.


Moreover, the challenges pinpointed in the dataset find parallels in many real\-world scenarios. Hence, how a method navigates these challenges becomes a tangible testament to its applicability in practical contexts. This tangible applicability amplifies the relevance of both the benchmark suite and the research's findings to field professionals and researchers.


In conclusion, this work marks a significant leap in the trajectory of PINNs, fueling further innovation and exploration in this riveting domain. The paper's offerings, spanning from the benchmark suite to the critical insights, are poised to galvanize more in\-depth investigations and advancements in PINNs, ushering in enhanced solutions for real\-world quandaries.

**Weaknesses:**
The paper has some areas it could improve on.


First, the authors only discuss PINN methods. They didn't look at other common methods. It would be good to see how PINN methods compare to these.


Second, they didn't give much detail on what computer stuff is needed for PINN methods. They did say if the methods work fast or slow. But, it would be helpful to know what computer tools or power is needed. People who want to use these methods would find that information useful.


Last, the authors worked with a set of 20 PDE problems. But they might have missed some other important problems. In future studies, it would be good to add more problems to their list. This way, we can learn even more.

**Questions:**
How did you ensure that the PINN methods you evaluated were able to handle the diverse range of PDEs in your dataset, and what challenges did you encounter in this process?


Can you describe the process of training the neural networks for each PDE, and how you optimized the hyperparameters for each method?


How did you handle issues such as boundary conditions and initial conditions in your experiments, and what strategies did you use to ensure that these conditions were satisfied?


Can you discuss the limitations of your benchmarking tool, and how future research could address these limitations to further advance the field of PINNs?

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
6: marginally above the acceptance threshold

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 19
**Author:** Authors

**Comment:**
Dear Reviewer xNZs,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions.


**Q1\.** This work only compares PINN variants but did not look at other methods.


**A1\.** PINNs represent a highly significant and promising approach, with numerous studies dedicated to their improvement. Given the diverse range of enhancements applicable to PINNs, conducting a systematic comparison within this domain alone is a substantial undertaking that can guide the development of future methodologies.


**Q2\.** Details of the computer stuff needed for PINNs.


**A2\.** All our experiments were conducted using a Linux server with 20 Intel(R) Xeon(R) Silver 4210 CPUs @ 2\.20GHz and eight NVIDIA GeForce RTX 2080 Ti each with 12 GB GPU memory. We have included this information in **Appendix E.1**.


**Q3\.** How did you ensure that the PINN methods you evaluated were able to handle the diverse range of PDEs in your dataset, and what challenges did you encounter in this process?


**A3\.** The selection of PDEs for our benchmark was derived from a range of representative literature, encompassing typical equations categorized by their mathematical properties. Specifically, we chose 7 major categories of PDEs, relevant to various fields like fluid dynamics and electromagnetism. The primary challenge lay in the multitude of PDE types and the complexity of categorization. Our solution involved classifying PDEs by mathematical form, then grouping practical problems under these different types, and designing varying levels of difficulty.


**Q4\.** Can you describe the process of training the neural networks for each PDE, and how you optimized the hyperparameters for each method?


**A4\.** If I understand your question correctly, in our main experiments, we fixed certain hyperparameters like 1e\-3 for learning rate, 8192/32768 for batch size, 20000 for epochs, etc., and adopted an approach of running three repetitions to ensure reproducibility. For hyperparameter selection, we initially studied the impact of some shared hyperparameters in **Figure 2, Figure 3, Appendix E.2** and chose a balanced parameter in terms of effectiveness and computational cost. For method\-specific hyperparameters, detailed studies are provided in the appendix **Appendix E.2, Table 19\~Table 26**.


**Q5\.** How did you handle issues such as boundary conditions and initial conditions in your experiments, and what strategies did you use to ensure that these conditions were satisfied?


**A5\.** Different types of PINN variants have their own approaches to handling boundary conditions. For instance, vanilla PINNs directly incorporate boundary conditions into the loss function combined with PDE loss, so the results may not strictly satisfy boundary conditions. Some methods, like FBPINNs, employ strategies such as hard constraints to restrict the solution space to a certain type of boundary conditions.


**Q6\.** Can you discuss the limitations of your benchmarking tool, and how future research could address these limitations to further advance the field of PINNs?


**A6\.** As a benchmark, its main limitation is the difficulty in continuously following new work and fairly, comprehensively testing its strengths and weaknesses. For future work, if researchers correctly use our benchmark for comparison, we can establish a leaderboard. This approach will make researchers aware of the current issues in PINNs and continue to drive progress in the field.


### Official Comment 20
**Author:** Authors

**Comment:**
Dear Reviewer xNZs,


Thank you for your valuable feedback and suggestions on improving our paper. Here we address responses to your questions.


**Q1\.** This work only compares PINN variants but did not look at other methods.


**A1\.** PINNs represent a highly significant and promising approach, with numerous studies dedicated to their improvement. Given the diverse range of enhancements applicable to PINNs, conducting a systematic comparison within this domain alone is a substantial undertaking that can guide the development of future methodologies.


**Q2\.** Details of the computer stuff needed for PINNs.


**A2\.** All our experiments were conducted using a Linux server with 20 Intel(R) Xeon(R) Silver 4210 CPUs @ 2\.20GHz and eight NVIDIA GeForce RTX 2080 Ti each with 12 GB GPU memory. We have included this information in **Appendix E.1**.


**Q3\.** How did you ensure that the PINN methods you evaluated were able to handle the diverse range of PDEs in your dataset, and what challenges did you encounter in this process?


**A3\.** The selection of PDEs for our benchmark was derived from a range of representative literature, encompassing typical equations categorized by their mathematical properties. Specifically, we chose 7 major categories of PDEs, relevant to various fields like fluid dynamics and electromagnetism. The primary challenge lay in the multitude of PDE types and the complexity of categorization. Our solution involved classifying PDEs by mathematical form, then grouping practical problems under these different types, and designing varying levels of difficulty.


**Q4\.** Can you describe the process of training the neural networks for each PDE, and how you optimized the hyperparameters for each method?


**A4\.** If I understand your question correctly, in our main experiments, we fixed certain hyperparameters like 1e\-3 for learning rate, 8192/32768 for batch size, 20000 for epochs, etc., and adopted an approach of running three repetitions to ensure reproducibility. For hyperparameter selection, we initially studied the impact of some shared hyperparameters in **Figure 2, Figure 3, Appendix E.2** and chose a balanced parameter in terms of effectiveness and computational cost. For method\-specific hyperparameters, detailed studies are provided in the appendix **Appendix E.2, Table 19\~Table 26**.


**Q5\.** How did you handle issues such as boundary conditions and initial conditions in your experiments, and what strategies did you use to ensure that these conditions were satisfied?


**A5\.** Different types of PINN variants have their own approaches to handling boundary conditions. For instance, vanilla PINNs directly incorporate boundary conditions into the loss function combined with PDE loss, so the results may not strictly satisfy boundary conditions. Some methods, like FBPINNs, employ strategies such as hard constraints to restrict the solution space to a certain type of boundary conditions.


**Q6\.** Can you discuss the limitations of your benchmarking tool, and how future research could address these limitations to further advance the field of PINNs?


**A6\.** As a benchmark, its main limitation is the difficulty in continuously following new work and fairly, comprehensively testing its strengths and weaknesses. For future work, if researchers correctly use our benchmark for comparison, we can establish a leaderboard. This approach will make researchers aware of the current issues in PINNs and continue to drive progress in the field.


