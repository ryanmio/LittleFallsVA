[JOSIS] Editor Decision
2025-10-17 07:04 AM
Dear Ryan Mioduski,

We have reached a decision regarding your submission to Journal of Spatial Information Science, "Benchmarking Large Language Models for Geolocating Colonial Virginia Land Grants", based on the feedback of three reviewers.

Our decision is: Revisions Required

The three reviewers are positive about the novelty of your study, its comprehensiveness, and the sounsness of the experimental design. However, they also have some recommendations, which I'd like you to consider. The main three recommendations are about: 1) better embedding the work in the current literature and using references to the corpora and tools you list, 2) discussing the limitations regarding, among other things, that the study is limited to ChatGTP models and does not include other LLMs, and that the sample is relatively small, and 3) recondering if the sections 14-16 are crucial for the main message of the paper or rather make it too long and harder to read. Please find these and other comments in more detail below.

As an editor, I'd like to ask you if you could be a bit less pressing against us with your messages. We're a journal supported entirely through the efforts of volunteers without a publisher. That means that I am not monitoring your paper every minute of the day, but you can be assured that it is on my mind and on my to do list. In the current academic system, it is hard to find reviewers. Coming back with three constructive reviews in two months time even though your manuscript was submitted in the middle of our summer is a good service in my opinion. Please have a bit more trust in and respect for our work and the work of our reviewers, or otherwise feel free to pay a large publisher to be at your service every minute of the day. Thank you. 

If you are willing to revise your manuscript based on the main points above and the other points raised by the reviewers and editors, we can reconsider your manuscript for publication in our journal. Please submit two versions of the revised manuscript, one plain version and one in which the changes are highlighted. In addition, please submit a document with a detailed response to each point raised by the reviewers and editors as well as an indication of what has been changed in the manuscript to address that point. Thank you.

Best regards,

Judith Verstegen

editor-in-chief


------------------------------------------------------
Reviewer A:

The paper evaluates the suitability of LLM-based approaches to georeference historical text descriptions of locations based on a corpus of Virginia patent grants from the early 18th century. The paper provides a detailed quantitative analysis of mean errors, latency, involved costs, and the trade-offs between these, comparing multiple versions of ChatGPT, different implementation approaches (one-shot vs. chain-of-thought), and alternative (non-LLM-based) methods (including a human GIS analyst). One main conclusion is that LLM-based approaches outperform traditional methods at still very low costs, illustrating the potential that LLMs provide for automating the georeferencing of historical place descriptions.

 

Georeferencing historical place descriptions is a challenging task, even for humans, and I am not aware of many attempts to evaluate the suitability of LLM-based approaches to fully automate or at least support this task. It comes with the nature of this kind of study that with the fast development of LLMs, the results will most likely become outdated very quickly but the paper illustrates the benefits that LLM-based approaches already offer in this domain today, while at the same time providing a corpus and useful template for these kinds of evaluations in the future. Hence, I consider the described work a novel and significant contribution that fits very well to the themes of the journal.

 

The paper is clearly structured, written very well, and the material is overall well presented. Nevertheless, in particular the later parts still contain a significant number of smaller deficiencies that need to be resolved. I am including a list of the issues that I noticed at the end, together with some more minor suggestions for improvements. In addition, I'd like to point out that the additional material provided after the main text (Sections 14-16 in particular) is very, very extensive, basically doubling the length of the paper. I am certainly not against publishing this additional material and analyses but it could be an alternative to make this part of the apparently already existing complementary web repository to make the paper a bit less overwhelming. 

 

The conclusions the paper makes are justified within the limitations clearly stated in the text. The risk of training data contamination is clearly a crucial factor but the authors took reasonable efforts, so I feel it's unlikely to be the case here. However, the reasons for using a very small test data set (43 instances) did not get clear to me, and I would like to see some clarification on this. How was the number decided and wouldn't it have been possible to use a significantly larger number of instances, at least for comparing between the automatic approaches?  

 

A smaller downside to me is the fact that the study is limited to ChatGTP models and does not include other LLMs. I am willing to accept this given the large number of different variants and approaches that are already compared but I'd like to at least see this acknowledged somewhere in the paper.

 

Lastly, I felt that for a paper of this length, the bibliography is comparatively short. I can see that this is partially due to this work exploring new grounds but, on the other hand, the text refers to existing work like corpora or tools (GeoCorpora, WikToR, GeoLingit, GeoGlue, GeoText, ...) without providing references, so I would like to encourage the authors to add literature references for these wherever possible.

 

Detailed points:

 

- Reference Huang et al is missing (p.5)

 

- I would strongly suggest including an example of a grant description early on in the introduction (or at least a reference to one that appears much later in the paper). This would give the reader a good idea of what kind of texts the paper is about early on. 

 

- There are cases where the text refers to other sections using § which first made me think this was for some appendix or complementary material. I would suggest to instead use "Section ..." consistently.

 

- Section 4: I feel it would be more natural to switch the order of 4.3 and 4.4 (as 4.3 refers to the content of 4.4) or even put 4.4 before 4.2.

 

- Section 4.5: It would be good to briefly explain the meaning of the temperature parameter in the context of LLMs.

 

- Some table references appear with a ~ symbol (e.g. Section 4.8).

 

- In contrast to other subsections, 4.6 does not give an outlook on performance; this is a bit inconsistent, any reason?

 

- The beginning of section 5 is slightly redundant with the previous section; it would be better to decide for a single place for this information.

 

- Section 6.1: Figure 4 is only mentioned very briefly but it's not getting clear what can be learned from it.

 

- Section 6.2: No reference to table 6 in the text, and I don't see a good reason for listing both costs per individual grants and per 1000 requests.

 

- Figure 6 has no values for the H# ; if there is a good reason, it may still be better to remove them from the table altogether.

 

- Table reference in 6.4 should probably be "Table 7" and the table is lacking number + caption.

 

- The rounding of numbers in the text of Sect. 6.5 is a bit odd (compare to numbers in the table).

 

- Figure 8: Color of triangle in map does not match legend and the figure is not referenced in the text.

 

- There are several references to the "appendix" in the text but only 16.5.1 (still?) is labeled as appendix; this looks like a leftover from a previous version and needs to be carefully resolved.

Recommendation: Revisions Required

------------------------------------------------------



------------------------------------------------------
Reviewer B:

The study aimed to determine whether LLMs can improve the identification of geographic coordinates from narrative colonial land-grant abstracts. Their goals were explicitly stated to measure the accuracy, cost-effectiveness, and reproducibility of their approach, which combines LLMs for context interpretation and geocoding techniques for coordinate identification, against other geoparsing techniques and a human expert.

Results show that an LLM-enabled workflow outperforms state-of-the-art techniques and traditional baselines. They also document costs and latency. Finally, they provide reproducible and well-documented evidence.

They created a corpus of abstracts of Virginia land patents from Cavaliers & Pioneers. They used a small evaluation set of randomly sampled patents with authoritative GIS ground-truth coordinates, cross-validated by experts. They are also open-sourcing this dataset as a contribution.

I found their experimental methodology to be sound and comprehensive. They touched upon every combination of LLM, pre- and post-processing techniques, and geocoding techniques that I can think would be of value. They evaluated their ensemble approach against almost every existing geoparsing tool that could compete.

Perhaps the only workflow they missed in their comparison is an end-to-end Google geoparsing pipeline, which utilizes Google's spatial reasoning AI (only released recently) and Google geocoding capabilities. However, even if such a solution performed better, it would likely be more expensive and proprietary, which would limit its extensibility and scalability. If the researchers have the means, they can add such an experiment; however, I would leave this decision up to them, as the current version of the paper is sufficient. That could be a follow-up conference paper for them.

If I want to be picky, there are some minor deficiencies. One limitation is the small evaluation dataset, which restricts the conclusions that can be drawn from the results. However, I understand that their goal was more about a comprehensive evaluation compared to simply a high count. As other research has shown (e.g., GeoTxt and GeoCorpora), geoparsing is a complex and sometimes ambiguous process, and even humans examining individual texts may struggle to determine accurate answers. Second, they didn't attempt any polygon-level reconstruction (limited to point coordinates) of the plots. However, reconstructing historical boundaries is a topic of research in its own right.

The research article is an excellent contribution, both as a piece of historical GIS research and as a methodological benchmark for applying large language models (LLMs) to spatial problems. The study is well-planned and constructed with a clear description of data sources, experiments, evaluation metrics, and reproducibility procedures.  In addition, the authors effectively position their work within the related literature, summarize the results, and identify future research directions.

The sections discussing geospatial foundation models and cost trade-offs are a valuable addition, as they connect the technical performance evaluation to broader considerations of accessibility, scalability, and real-world adoption. In addition to advancing research, the manuscript serves as a practical guide to geoparsing with LLMs, providing valuable insights for both GIS practitioners and those in other domains seeking to apply geoparsing techniques.

Although the geoparsing task is somewhat niche (i.e., the geolocation of colonial Virginia land grants), the methodological insights are widely generalizable. Overall, the paper presents impressive research, compelling results, and clear implications. Their study methodology is well thought out and clearly explained, which lends substantial credibility to their results.

To quickly summarize my review requirements above, I have no desired requirements improvements or additions from their research. I provided some recommendations, but even these are not mandatory, and it is up to the authors to decide whether to incorporate any of them.

My only strong suggestion to improve their manuscript is that all of their table and figure captions need to be more descriptive. For example, "Figure 1: Coordinate accuracy by method" should provide some context about what the table means to the research article. Ie. "Figure 1: The coordinate accuracy shows … performing best with a mean error of … [such and such] is also interesting because…"

Recommendation: Accept Submission

------------------------------------------------------



------------------------------------------------------
Reviewer C:
This paper describes (in depth!) a careful trial of how existing large language models can be used in an extremely challenging geolocation task. The manuscript demonstrates impressive care to articulate how risks, biases &c. are considered, and how cost and accuracy must be balanced in actual large-scale projects. As it turns out, the large language work quite well, and based on the examples I can certainly understand that classical methods struggle. Coming at this paper as a reader with an interest in algorithms and methods, this result is quite unsatisfying to me – but that does not make it untrue. Indeed, it might be good to have this report in the literature as a thoroughly reported case study of what is possible with currently available LLM models. (The decision of whether JOSIS is the appropriate venue for this is of course up to the editors.)
I vote "revisions required," but these can be relatively minor, consisting of typesetting, some minor technical details, and a case where I would appreciate less credulous phrasing as to what an LLM "does".
page 5 "Huang et al. [?]" reference error page 6 section 2.4 line 4 "Li et al. [5]" large space: use ~ page 7, I don't love the phrasing of models' "cognitive processes" page 9, having one human is a source of variance... page 10, how often did H-2 fall back to virginia's geographic center? maybe it's better than having missing data, but it would also pull up the average enormously in a rather random way page 11, why this temperature? (this is discussed later, but might be nice to mention here) page 11, "geocode\_place" is the backslash a copy/paste error in typesetting? page 12, re: DBSCAN, so that's basically MinPts=3? middle of page 12: what is the "[H]" Maybe it was supposed to be a latex command? page 13, it would be nice to know what "script development time" entails and if further grants would now be quicker to georeference. page 14, The mean column is hard to read; it looks like enough width can be achieved by making some of the other columns less wide. Section 6.2's discussion of a cost/quality Pareto front is nice. page 21 ("WILLIAM WILLIAMS) has unbalanced quote characters page 21 I'm very skeptical of the phrasing "All cognition is 'in the head' of the network: it interprets archaic toponyms, performs mental triangulation against its latent world map, and produces a best-guess point estimate." Do we know any of this is true? I can be sold on the idea of a "latent world map", but what does it mean to say it performs mental triangulation against it? Section 6.6, ablation study is nice 7.2 "Error Analysis & Failure Modes" is a good section. Recommendation: Revisions Required

------------------------------------------------------




________________________________________________________________________
Journal of Spatial Information Science
Open Access International Journal for Spatial and Geographical Information Science
https://josis.org