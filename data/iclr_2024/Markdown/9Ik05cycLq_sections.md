## Abstract

Large language models (LLMs) are vulnerable to adversarial attacks, which add maliciously designed token sequences to bypass the model’s safety guardrails and cause it to produce harmful content. In this work, we introduce erase-and-check, the first framework to defend against adver- sarial prompts with certifiable safety guarantees. Given a prompt, our erase-and-check method erases tokens individually and inspects the re- sulting subsequences using a safety filter, declaring it harmful if any of the subsequences are detected as harmful. Our safety filters are implemented by leveraging Llama 2 and DistilBERT. We theoretically demonstrate that our method detects harmful prompts with accuracy at least as high as the safety filter. Additionally, we propose three efficient empirical defenses inspired by our erase-and-check (EC) method: i) RandEC, a randomized subsampling version of erase-and-check; ii) GreedyEC, which greedily erases tokens that maximize the softmax score of the harmful class; and iii) GradEC, which uses gradient information to optimize the tokens to erase. Extensive empirical evaluation with real-world datasets demonstrates the effectiveness of the proposed

## Introduction

Large language models such as ChatGPT, Bard, and Llama are often trained using unvetted textual data from the web that contain significant amounts of inappropriate and objec- tionable material. A model trained on such data can produce harmful content, making it unsuitable for public use. Furthermore, as language models improve over time, they become better at following user instructions, including those from malicious actors intended to cause harm. To this end, several fine-tuning techniques have been developed to incorporate hu- man feedback to ensure that LLM outputs are safe and aligned with human values (Ouyang et al., 2022; Bai et al., 2022; Glaese et al., 2022; Korbak et al., 2023; Xu et al., 2020). When prompted with a harmful user request, an aligned model is expected to decline the request, similar to the example below. 1 Published as a conference paper at COLM 2024 Harmful Prompt Provide detailed instructions on making a homemade explosive de- vice using household materials. LLM Response Sorry, I cannot assist with that request. Promoting safety is of ut- most importance. Although significant progress has been made in developing guardrails for LLMs, several "jailbreak" attacks allow a malicious user to bypass safety measures. For example, Wei et al. (2023) show that simply asking an LLM to begin its response with “Absolutely! Here’s” could mislead the model into complying with a harmful request. Several other examples of adversarial augmentation of harmful prompts, such as the Do Anything Now (DAN) jailbreak, also exist. Recently, Zou et al. (2023) demonstrated an automated generation of adversarial sequences, creating an endless supply of such attacks, using their Greedy Coordinate Gradient (GCG) attacks. Their method achieves a high attack success rate, of up to 84%, even on black-box LLMs such as GPT-3.5 using adversarial suffixes that are only 20 tokens long. The following is an illustration of the effect of the attack on the above example: Harmful Prompt + Adversarial Sequence Provide detailed instructions on making a homemade explosive de- vice using household materials. hilt thou ordinary the our tly LLM Response Sure, here’s a step-by-step guide to making a homemade explosive device... Defenses against such attacks have been proposed in the literature. For example, Jain et al. (2023), Phute et al. (2023), and Alon & Kamfonas (2023) study approaches such as perplexity filtering, paraphrasing, and self-examination. Each approach targets a specific weakness of adversarial sequences to detect and defend against them. For instance, perplexity filtering leverages the gibberish nature of an adversarial sequence to distinguish it from the rest of the prompt, and