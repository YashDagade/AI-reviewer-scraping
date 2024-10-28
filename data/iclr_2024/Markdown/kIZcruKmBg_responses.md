## Reviewer Responses

### Official Review 1
**Author:** Reviewer 2kyY

**Summary:**
The work proposes a method to enhance Physics\-informed Neural Networks (PINNs) by integrating geometric transformations, to address challenges posed by complex or non\-euclidean geometries. 
The method utilizes a diffeomorphism ϕ that maps a reference domain Ωref to the observation domain Ω, adapting the derivative computation in the physics\-informed loss function. The approach was demonstrated through various problems: Eikonal equation on Archimedean spiral, Poisson problem on surface manifold, Incompressible Stokes flow in deformed tube. Finally, they show that their method can be applied to perform shape optimization according to a Laplace PDE loss.

**Soundness:**
2 fair

**Presentation:**
2 fair

**Contribution:**
1 poor

**Strengths:**
The paper is easy to read and the geometric transformation seems reasonable to solve this kind of problem. The first three different examples each test a different geometric setting. The figures are pretty.

**Weaknesses:**
The method relies on the output transformation trick to enforce boundary conditions (BC), which is well suited for Dirichlet BC only. It would not be applicable as is for different kinds of BC, but the authors have a much more general claim.


Except for the last example, which we will discuss next, the diffeomorphism ϕ is known a priori. Therefore the method in such case simply looks like a change in variable with a known function. How can you apply this method on a domain which is not equipped with such a transformation ?


The last example is very mysterious to me. I actually do not understand what the method is supposed to achieve by learning simultaneously to impose the PDE constraint and the geometric transformation. Do we know what target geometry the network should converge to ? Besides, the network that learns the transformation is not a diffeomorphism, so there is no guarantee that the optimization problem finds a correct solution. 


The authors do not compare their method with any existing work. There is no literature review. As a result, we do not really understand why these problems cannot be tackled with existing methods. Why do they fail ?


The authors do not provide any numerical results for their methods, and even the qualitative results do not include the ground truth solutions. It is therefore impossible to judge the effectiveness of the method.

**Questions:**
What is the difference between L, Lx and Ly concretely for each example ?


 What does the following sentence mean ? "transformed PINN finds the exact length with an error of \= 0\.1 %" .

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
1: strong reject

**Confidence:**
4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.

**Code Of Conduct:**
Yes


### Official Comment 2
**Author:** Authors

**Comment:**
Thank you for your review! Allow us to respond to your comments as follows.


*The method relies on the output transformation trick to enforce boundary conditions (BC), which is well suited for Dirichlet BC only. It would not be applicable as is for different kinds of BC, but the authors have a much more general claim.*


We are not sure which claim you are referring to. Does this refer to “For simplicity, let us denote Dirichlet boundary conditions only”?   We are not claiming that our approach is applicable to different kinds of BC than Dirichlet ones, and we definitely didn’t intend to let it appear more general. Besides, regarding Neumann boundary conditions, one can use the domain transformation to compute the outer normal of the transformed geometry, but it’s unclear how to strongly impose Neumann boundary conditions, as it’s not clear for PINNs in general.


*Except for the last example, which we will discuss next, the diffeomorphism is known a priori. Therefore the method in such case simply looks like a change in variable with a known function. How can you apply this method on a domain which is not equipped with such a transformation?*


In our work, we assume that the diffeomorphism is given, and we assume that the domain geometry is defined by the mapping of the reference domain via the diffeomorphism. If, vice versa, a geometry is given, e.g., by a mesh, the diffeomorphism might be learned, but it’s definitely an open question how this would be achieved effectively.


*The last example is very mysterious to me. I actually do not understand what the method is supposed to achieve by learning simultaneously to impose the PDE constraint and the geometric transformation. Do we know what target geometry the network should converge to ? Besides, the network that learns the transformation is not a diffeomorphism, so there is no guarantee that the optimization problem finds a correct solution.*


In the last example, we tried to make the mapping more general by using an NN as transformation (targeting the concern of the limitation that the diffeomorphism has to be known a priori, as in your previous comment).
It was intended as an explorative example to show what could be done incorporating a parametrized transformation.
We believe that we were able to demonstrate that this idea results in a geometrically very flexible PDE solver, e.g., in contrast to classical FEM solvers that would require re\-meshing.


However, as you mentioned (and we stated clearly), the network has no guarantee to be diffeomorph and this stretches the framework we outlined beforehand beyond its assumptions.


We agree that our objective function \- not including an explicit target \- is somewhat arbitrary and that we are not able to state analytically what the network should converge to. Experience with PINNs suggests that a convex shape is easiest to optimize for w.r.t. weak boundary conditions, and this is what our example actually results in.


As this example opens too many concerns, we conclude in removing it completely upon further investigation.


*The authors do not compare their method with any existing work. There is no literature review. As a result, we do not really understand why these problems cannot be tackled with existing methods. Why do they fail ?*


We recognize that our examples need more comparisons with similar problems from literature.   Unfortunately, to the best of our knowledge, we are not aware of previous works that applied PINNs to manifolds, which severely limits the possibilities of a comparison as well as a literature review.


*The authors do not provide any numerical results for their methods, and even the qualitative results do not include the ground truth solutions. It is therefore impossible to judge the effectiveness of the method.* / 
*What does the following sentence mean? "transformed PINN finds the exact length with an error of \= 0\.1 %”*


The first example is constructed in a way that the numerical solution can be compared to an analytical solution. We were not providing a plot for both solutions, because they are trivial and closely aligned s.t. a plot didn’t make sense. Instead, we stated that the numerical solution fits the analytical solution “with an error of 0\.1%”. This is what the sentence meant, sorry for the incomprehensible expression.


We acknowledge that our work is lacking analytical results for example 2 and a comparative study for example 3\.


*What is the difference between L, L\_x and L\_y, and concretely for each example ?*


The subscript indicates the derivation variable of the differential operator. As other reviewers addressed the same issue, we have to make this more explicit along with equations (4\)\-(5\).   The examples are split into manifold and transformation cases, where manifold corresponds to L\_y and transformation to L\_x. We will provide more clarity here.


### Official Comment 3
**Author:** Reviewer 2kyY

**Comment:**
Thank you for your response, I will keep my score.


### Official Comment 4
**Author:** Authors

**Comment:**
Thank you for your review! Allow us to respond to your comments as follows.


*The method relies on the output transformation trick to enforce boundary conditions (BC), which is well suited for Dirichlet BC only. It would not be applicable as is for different kinds of BC, but the authors have a much more general claim.*


We are not sure which claim you are referring to. Does this refer to “For simplicity, let us denote Dirichlet boundary conditions only”?   We are not claiming that our approach is applicable to different kinds of BC than Dirichlet ones, and we definitely didn’t intend to let it appear more general. Besides, regarding Neumann boundary conditions, one can use the domain transformation to compute the outer normal of the transformed geometry, but it’s unclear how to strongly impose Neumann boundary conditions, as it’s not clear for PINNs in general.


*Except for the last example, which we will discuss next, the diffeomorphism is known a priori. Therefore the method in such case simply looks like a change in variable with a known function. How can you apply this method on a domain which is not equipped with such a transformation?*


In our work, we assume that the diffeomorphism is given, and we assume that the domain geometry is defined by the mapping of the reference domain via the diffeomorphism. If, vice versa, a geometry is given, e.g., by a mesh, the diffeomorphism might be learned, but it’s definitely an open question how this would be achieved effectively.


*The last example is very mysterious to me. I actually do not understand what the method is supposed to achieve by learning simultaneously to impose the PDE constraint and the geometric transformation. Do we know what target geometry the network should converge to ? Besides, the network that learns the transformation is not a diffeomorphism, so there is no guarantee that the optimization problem finds a correct solution.*


In the last example, we tried to make the mapping more general by using an NN as transformation (targeting the concern of the limitation that the diffeomorphism has to be known a priori, as in your previous comment).
It was intended as an explorative example to show what could be done incorporating a parametrized transformation.
We believe that we were able to demonstrate that this idea results in a geometrically very flexible PDE solver, e.g., in contrast to classical FEM solvers that would require re\-meshing.


However, as you mentioned (and we stated clearly), the network has no guarantee to be diffeomorph and this stretches the framework we outlined beforehand beyond its assumptions.


We agree that our objective function \- not including an explicit target \- is somewhat arbitrary and that we are not able to state analytically what the network should converge to. Experience with PINNs suggests that a convex shape is easiest to optimize for w.r.t. weak boundary conditions, and this is what our example actually results in.


As this example opens too many concerns, we conclude in removing it completely upon further investigation.


*The authors do not compare their method with any existing work. There is no literature review. As a result, we do not really understand why these problems cannot be tackled with existing methods. Why do they fail ?*


We recognize that our examples need more comparisons with similar problems from literature.   Unfortunately, to the best of our knowledge, we are not aware of previous works that applied PINNs to manifolds, which severely limits the possibilities of a comparison as well as a literature review.


*The authors do not provide any numerical results for their methods, and even the qualitative results do not include the ground truth solutions. It is therefore impossible to judge the effectiveness of the method.* / 
*What does the following sentence mean? "transformed PINN finds the exact length with an error of \= 0\.1 %”*


The first example is constructed in a way that the numerical solution can be compared to an analytical solution. We were not providing a plot for both solutions, because they are trivial and closely aligned s.t. a plot didn’t make sense. Instead, we stated that the numerical solution fits the analytical solution “with an error of 0\.1%”. This is what the sentence meant, sorry for the incomprehensible expression.


We acknowledge that our work is lacking analytical results for example 2 and a comparative study for example 3\.


*What is the difference between L, L\_x and L\_y, and concretely for each example ?*


The subscript indicates the derivation variable of the differential operator. As other reviewers addressed the same issue, we have to make this more explicit along with equations (4\)\-(5\).   The examples are split into manifold and transformation cases, where manifold corresponds to L\_y and transformation to L\_x. We will provide more clarity here.


### Official Comment 5
**Author:** Reviewer 2kyY

**Comment:**
Thank you for your response, I will keep my score.


### Official Review 6
**Author:** Reviewer VH6u

**Summary:**
This paper employs physics\-informed neural networks (PINNs) for addressing intricate or changing geometrical configurations. The primary technical innovation lies in the incorporation of a geometric transformation (diffeomorphism) of a reference domain to describe the computational domain.

**Soundness:**
2 fair

**Presentation:**
2 fair

**Contribution:**
2 fair

**Strengths:**
The problem is well defined and the author proposes a clear formulation in solving the problem.

**Weaknesses:**
Unfortunately, it appears that the problem tackled in the paper is somewhat incremental, and the proposed solution lacks a surprising or profound aspect. In the context of an ICLR paper, I'm seeking a novel problem that has not previously been successfully addressed, made attainable through this approach, or a novel method to solve a well\-established problem that has been extensively explored. Unfortunately, neither of these elements seems to be present in the paper.


Furthermore, the examples provided mainly consist of small\-scale 2D toy examples. To comprehensively assess the efficacy of this approach, it would be necessary for the authors to set up larger\-scale problems that are well\-documented in CFD/JCP/CMAME papers.

**Questions:**
How does this work compare with Bonev\+ ICML 2023? These authors propose a neural PDE approach using spherical coordinate. Your paper seems to be more general. Can you reproduce some of the examples in their paper so we can have an apple to apple comparison?

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
3: reject, not good enough

**Confidence:**
3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

**Code Of Conduct:**
Yes


### Official Comment 7
**Author:** Authors

**Comment:**
Thank you for your review! Let us address your comments as follows.


*Unfortunately, it appears that the problem tackled in the paper is somewhat incremental, and the proposed solution lacks a surprising or profound aspect. In the context of an ICLR paper, I'm seeking a novel problem that has not previously been successfully addressed yet, made attainable through this approach, or a novel method to solve a well\-established problem that has been extensively explored. Unfortunately, neither of these elements seems to be present in the paper.*


Thank you for your valuable feedback. We agree that one can consider the problem tackled somewhat incremental, and that our work does not propose a novel method to solve a well\-studied problem.


We tried to introduce the approach of including a diffeomorphism within PINNs as a (novel) general concept, and we believe it could benefit from a common introduction. Furthermore, we consider the application of PINNs to manifolds as a problem that has not been successfully addressed, which is made attainable through this approach.


A surprising aspect of our approach is that \- in the transformation case \- a latent representation of the PDE solution on the reference domain arises. This is likely to improve generalization capabilities for parametrized geometries, but we recognize that we were not able to demonstrate this effectively on a well\-studied problem.


*Furthermore, the examples provided mainly consist of small\-scale 2D toy examples. To comprehensively assess the efficacy of this approach, it would be necessary for the authors to set up larger\-scale problems that are well\-documented in CFD/JCP/CMAME papers.*


As mentioned above, we tried to introduce the approach as a general concept and, therefore, we set up easily understandable examples that demonstrate the efficacy of the approach. We tried to choose examples with a clear setup and analytical solutions, accompanied by a transparent and manageable implementation.


However, we accept that there is a request for applying our method to larger\-scale, well\-documented problems that would comprehensively assess the efficacy for non\-toy examples.


*How does this work compare with Bonev\+ ICML 2023? These authors propose a neural PDE approach using spherical coordinate. Your paper seems to be more general. Can you reproduce some of the examples in their paper so we can have an apple to apple comparison?*


Bonev\+2023 propose Spherical Fourier Neural Operators (Spherical FNOs) that put the concept of FNOs efficiently onto spheres. As they use spherical harmonics for the Fourier transform, their approach is limited to spheres by definition.  Our approach is more general in the sense that we can model arbitrary manifolds. We think an apple\-to\-apple comparison doesn’t make sense, because it would be restricted to the case of spheres where the SFNOs will clearly outperform all aspects of our method (accuracy and speed) as it is explicitly tailored to this case.


### Official Comment 8
**Author:** Authors

**Comment:**
Thank you for your review! Let us address your comments as follows.


*Unfortunately, it appears that the problem tackled in the paper is somewhat incremental, and the proposed solution lacks a surprising or profound aspect. In the context of an ICLR paper, I'm seeking a novel problem that has not previously been successfully addressed yet, made attainable through this approach, or a novel method to solve a well\-established problem that has been extensively explored. Unfortunately, neither of these elements seems to be present in the paper.*


Thank you for your valuable feedback. We agree that one can consider the problem tackled somewhat incremental, and that our work does not propose a novel method to solve a well\-studied problem.


We tried to introduce the approach of including a diffeomorphism within PINNs as a (novel) general concept, and we believe it could benefit from a common introduction. Furthermore, we consider the application of PINNs to manifolds as a problem that has not been successfully addressed, which is made attainable through this approach.


A surprising aspect of our approach is that \- in the transformation case \- a latent representation of the PDE solution on the reference domain arises. This is likely to improve generalization capabilities for parametrized geometries, but we recognize that we were not able to demonstrate this effectively on a well\-studied problem.


*Furthermore, the examples provided mainly consist of small\-scale 2D toy examples. To comprehensively assess the efficacy of this approach, it would be necessary for the authors to set up larger\-scale problems that are well\-documented in CFD/JCP/CMAME papers.*


As mentioned above, we tried to introduce the approach as a general concept and, therefore, we set up easily understandable examples that demonstrate the efficacy of the approach. We tried to choose examples with a clear setup and analytical solutions, accompanied by a transparent and manageable implementation.


However, we accept that there is a request for applying our method to larger\-scale, well\-documented problems that would comprehensively assess the efficacy for non\-toy examples.


*How does this work compare with Bonev\+ ICML 2023? These authors propose a neural PDE approach using spherical coordinate. Your paper seems to be more general. Can you reproduce some of the examples in their paper so we can have an apple to apple comparison?*


Bonev\+2023 propose Spherical Fourier Neural Operators (Spherical FNOs) that put the concept of FNOs efficiently onto spheres. As they use spherical harmonics for the Fourier transform, their approach is limited to spheres by definition.  Our approach is more general in the sense that we can model arbitrary manifolds. We think an apple\-to\-apple comparison doesn’t make sense, because it would be restricted to the case of spheres where the SFNOs will clearly outperform all aspects of our method (accuracy and speed) as it is explicitly tailored to this case.


### Official Review 9
**Author:** Reviewer UpPb

**Summary:**
In this paper, it is argued that the existing approaches to physics\-informed neural networks are not apt for complex and transforming geometries. To this end, the paper presents an approach to introduce geometric transformation within the physics\-informed neural network design. Concretely, it enforces the Dirichlet boundary condition using distance function to account for complex geometries. Experimental results on four different examples are shown to demonstrate the suitability of the method.

**Soundness:**
3 good

**Presentation:**
3 good

**Contribution:**
3 good

**Strengths:**
* It is a well\-written paper.
* The use of Dirichlet boundary conditions is promising.
* An initial approach to explore a new direction for more promising neural network design.

**Weaknesses:**
* Some of the technical notations are not fully exposed and detailed.
* Experiments are limited on toy\-example and missing on the manifolds which are widely used in science and engineering application.
* The paper misses to highlight the limitations of the proposed approach.


Kindly refer to the Questions section for more comments.

**Questions:**
Domain and Transformation
-------------------------


It’s better to include the dimension of the variables on the side of the Eq(1\). 


2\.2\.1 Manifold: m\<n
----------------------


Lx and Ly need more explanation. The subscripts have not been explained. Diagram conveys that one is in the reference domain and other is in the computational domain yet it's better to write near the equation (4\)\-(5\) and following equation.


3\.1 Exact boundary condition with output transform
---------------------------------------------------


Kindly help me understand the approximation of u^, given that the inverse must hold and the proposed approximation is not linear.


4\.4 Shape Optimization with Laplace Operator
---------------------------------------------


I am not entirely convinced with the imposed boundary condition. What could be considered a weak boundary condition is not fully exposed in the paper. Furthermore, I request the authors to perform some experiments and analysis of the proposed theory on negative curvature surfaces with the introduced local approach. Also, the use of Laplace\-Beltrami operator for shapes.


In addition to the above, experiment on Low\-Dimensional manifolds is simple and not convincing to me for real application. I request the authors to provide some analysis and results on popular manifolds such as low\-dimensional SPD, Grassmannian manifolds, etc.

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
6: marginally above the acceptance threshold

**Confidence:**
4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.

**Code Of Conduct:**
Yes


### Official Comment 10
**Author:** Authors

**Comment:**
Thank you for your review. We would like to answer your comments and questions as follows.


Lx *and* Ly *need more explanation. The subscripts have not been explained. Diagram conveys that one is in the reference domain and other is in the computational domain yet it's better to write near the equation (4\)\-(5\) and following equation.*


Thanks for your feedback, other reviewers addressed the same issue. We only stated “L\=Ly with respect to global coordinates” and assumed that it’s clear that the subscript indicates the derivation variable. Obviously, this it is not the case and the subscript needs more explanation.


*Exact boundary condition with output transform: Kindly help me understand the approximation of u^, given that the inverse must hold and the proposed approximation is not linear.*


As the smooth distance function b is zero at the boundary, N(y)u(y) is zero on the boundary, and, therefore, u^(y)\=g(y) satisfies the Dirichlet boundary values g(y) at the boundary.   Unfortunately, we do not understand what you are referring to with ‘inverse must hold’, and why the approximation should to be ‘linear’.


*I am not entirely convinced with the imposed boundary condition. What could be considered a weak boundary condition is not fully exposed in the paper.*


A weak boundary condition (in the context of PINNs) means imposing the boundary condition by adding a penalizing loss term, as outlined in (8\). You noted correctly that we missed introducing this wording in the context of (8\) and it should be added.


*Experiments are limited on toy\-example and missing on the manifolds which are widely used in science and engineering application.*


 We tried to demonstrate our method on minimal working examples to make the setup and implementation clearly understandable. It’s unfortunate if you consider them as too limited, and we will take this feedback into account.


*The paper misses to highlight the limitations of the proposed approach.*


Unfortunately, that is true, we will add a paragraph on this.


*Furthermore, I request the authors to perform some experiments and analysis of the proposed theory on negative curvature surfaces with the introduced local approach. Also, the use of Laplace\-Beltrami operator for shapes.*


We do not see why negative curvature should have any relevant impact on our method, the proposed method also works with negative curvature surfaces.  Also, our second example demonstrates a Poisson problem on a part of a sphere, which \- as we formulate the derivatives in local coordinates \- corresponds to a Laplace\-Beltrami on the manifold. Our apologies that we didn’t point this out explicitly.


*In addition to the above, experiment on Low\-Dimensional manifolds is simple and not convincing to me for real application. I request the authors to provide some analysis and results on popular manifolds such as low\-dimensional SPD, Grassmannian manifolds, etc.*


Which PDEs are commonly formulated on low\-dimensional SPD or Grassmannian manifolds?


### Official Comment 11
**Author:** Authors

**Comment:**
Thank you for your review. We would like to answer your comments and questions as follows.


Lx *and* Ly *need more explanation. The subscripts have not been explained. Diagram conveys that one is in the reference domain and other is in the computational domain yet it's better to write near the equation (4\)\-(5\) and following equation.*


Thanks for your feedback, other reviewers addressed the same issue. We only stated “L\=Ly with respect to global coordinates” and assumed that it’s clear that the subscript indicates the derivation variable. Obviously, this it is not the case and the subscript needs more explanation.


*Exact boundary condition with output transform: Kindly help me understand the approximation of u^, given that the inverse must hold and the proposed approximation is not linear.*


As the smooth distance function b is zero at the boundary, N(y)u(y) is zero on the boundary, and, therefore, u^(y)\=g(y) satisfies the Dirichlet boundary values g(y) at the boundary.   Unfortunately, we do not understand what you are referring to with ‘inverse must hold’, and why the approximation should to be ‘linear’.


*I am not entirely convinced with the imposed boundary condition. What could be considered a weak boundary condition is not fully exposed in the paper.*


A weak boundary condition (in the context of PINNs) means imposing the boundary condition by adding a penalizing loss term, as outlined in (8\). You noted correctly that we missed introducing this wording in the context of (8\) and it should be added.


*Experiments are limited on toy\-example and missing on the manifolds which are widely used in science and engineering application.*


 We tried to demonstrate our method on minimal working examples to make the setup and implementation clearly understandable. It’s unfortunate if you consider them as too limited, and we will take this feedback into account.


*The paper misses to highlight the limitations of the proposed approach.*


Unfortunately, that is true, we will add a paragraph on this.


*Furthermore, I request the authors to perform some experiments and analysis of the proposed theory on negative curvature surfaces with the introduced local approach. Also, the use of Laplace\-Beltrami operator for shapes.*


We do not see why negative curvature should have any relevant impact on our method, the proposed method also works with negative curvature surfaces.  Also, our second example demonstrates a Poisson problem on a part of a sphere, which \- as we formulate the derivatives in local coordinates \- corresponds to a Laplace\-Beltrami on the manifold. Our apologies that we didn’t point this out explicitly.


*In addition to the above, experiment on Low\-Dimensional manifolds is simple and not convincing to me for real application. I request the authors to provide some analysis and results on popular manifolds such as low\-dimensional SPD, Grassmannian manifolds, etc.*


Which PDEs are commonly formulated on low\-dimensional SPD or Grassmannian manifolds?


### Official Review 12
**Author:** Reviewer 2tfv

**Summary:**
The paper intends to improve the performance of PINN on domains of complex geometries. The method is to use smooth transformations to transform a complex geometry to less complex one which is a called reference domain. If the transformations are differentiable, the training of modified PINNs is the same as training vanilla PINNs.

**Soundness:**
2 fair

**Presentation:**
1 poor

**Contribution:**
2 fair

**Strengths:**
**Originality:** The paper implements diffeomorphisms to the problem of PINN on complex geometries.


**Quality:** The paper explores the proposed methods on some typical examples to demonstrate the effectiveness of the method.


**Clarity:** The idea is conveyed directly and straightforward.


**Significance:** Combining diffeomorphism with training of neural network is somewhat interesting and natural, due to the differentiability of transformations.

**Weaknesses:**
One of the major weakness is that the paper does not include experiments of comparison between modified PINN and vanilla PINN. In order to show the effectiveness of the proposed method, the author should also test the performance of PINN on all the problems in section 4\.

**Questions:**
If the original problems L(u)\=f in Ω is transformed to Lx(u∘ϕ)\=f on reference domain Ωref, then Lx should not equal L. The calculation of Lx should use chain rule. In your paper, this part is hardly touched. How did you actually implement your method in experiments?

**Flag For Ethics Review:**
No ethics review needed.

**Rating:**
3: reject, not good enough

**Confidence:**
4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.

**Code Of Conduct:**
Yes


### Official Comment 13
**Author:** Authors

**Comment:**
Thank you for your review. We would like to address the following comments.


*One of the major weakness is that the paper does not include experiments of comparison between modified PINN and vanilla PINN. In order to show the effectiveness of the proposed method, the author should also test the performance of PINN on all the problems in section 4\.*


Unfortunately, we do not understand how vanilla PINNs should be applied to the case of manifolds, as directional derivatives have to be computed.  It might be possible to elaborate the differential operators (e.g., Laplace\-Beltrami) explicitly and compute those in a “vanilla” way, but this is what our approach implicitly does, formulated in local coordinates, putting all the work into the automatic differentiation.
In the case of equi\-dimensional transformations, vanilla PINNs could actually be applied and would lead to a well\-studied reference solution. Thank you for this suggestion.


*If the original problems L(u)\=f in Ω is transformed to Lx(u∘ϕ)\=f on reference domain Ω ref, then Lx should not equal L. The calculation of Lx should use chain rule. In your paper, this part is hardly touched. How did you actually implement your method in experiments?*


In the manifold case, chain rule applies and is carried out by the automatic differentiation framework.
In the transformation case, we explicitly neglect the chain rule. It’s somewhat arbitrary (and we are sorry if we didn’t make this sufficiently clear), but this idea leads to general transformed domains.
Regarding the actual implementation: We provide our full source code as supplementary material and refer to it for all implementation details.


### Official Comment 14
**Author:** Reviewer 2tfv

**Comment:**
Thanks for clarifying. I agree that this paper has novelty in solving PDE problems on manifold. However, regarding geometry transformation, here's my follow\-up question:


I'm still confused with eq. (6\)\-(7\). Given L(uref)\=f, how can u\=uref∘ϕ−1 satisfy L(u)\=f, as you mentioned above eq. (6\)\-(7\) that L\=Ly? In my understanding, generally u satisfies Ly(u)\=f and L≠Ly. 


I did look at the code, but due to this fundamental question I didn't follow.


### Official Comment 15
**Author:** Authors

**Comment:**
In (6\)\-(7\) we only substitute u\=uref∘ϕ−1 into (2\)\-(3\), and take L\=Ly as it is in (2\)\-(3\) (global coordinate y∈Ω). The reformulation is essentially trivial, but it is quite interesting because ϕ now governs the shape of domain Ω.


### Official Comment 16
**Author:** Authors

**Comment:**
Thank you for your review. We would like to address the following comments.


*One of the major weakness is that the paper does not include experiments of comparison between modified PINN and vanilla PINN. In order to show the effectiveness of the proposed method, the author should also test the performance of PINN on all the problems in section 4\.*


Unfortunately, we do not understand how vanilla PINNs should be applied to the case of manifolds, as directional derivatives have to be computed.  It might be possible to elaborate the differential operators (e.g., Laplace\-Beltrami) explicitly and compute those in a “vanilla” way, but this is what our approach implicitly does, formulated in local coordinates, putting all the work into the automatic differentiation.
In the case of equi\-dimensional transformations, vanilla PINNs could actually be applied and would lead to a well\-studied reference solution. Thank you for this suggestion.


*If the original problems L(u)\=f in Ω is transformed to Lx(u∘ϕ)\=f on reference domain Ω ref, then Lx should not equal L. The calculation of Lx should use chain rule. In your paper, this part is hardly touched. How did you actually implement your method in experiments?*


In the manifold case, chain rule applies and is carried out by the automatic differentiation framework.
In the transformation case, we explicitly neglect the chain rule. It’s somewhat arbitrary (and we are sorry if we didn’t make this sufficiently clear), but this idea leads to general transformed domains.
Regarding the actual implementation: We provide our full source code as supplementary material and refer to it for all implementation details.


### Official Comment 17
**Author:** Reviewer 2tfv

**Comment:**
Thanks for clarifying. I agree that this paper has novelty in solving PDE problems on manifold. However, regarding geometry transformation, here's my follow\-up question:


I'm still confused with eq. (6\)\-(7\). Given L(uref)\=f, how can u\=uref∘ϕ−1 satisfy L(u)\=f, as you mentioned above eq. (6\)\-(7\) that L\=Ly? In my understanding, generally u satisfies Ly(u)\=f and L≠Ly. 


I did look at the code, but due to this fundamental question I didn't follow.


### Official Comment 18
**Author:** Authors

**Comment:**
In (6\)\-(7\) we only substitute u\=uref∘ϕ−1 into (2\)\-(3\), and take L\=Ly as it is in (2\)\-(3\) (global coordinate y∈Ω). The reformulation is essentially trivial, but it is quite interesting because ϕ now governs the shape of domain Ω.


