Dear @essepuntato, 
Thank you for your comments, they allowed us to refine our research and analyse our data in new ways.
Here are the answers to you comments:

## General comments from the presentation

It is important that both the groups are aligned and use the same dumps, in particular the DOAJ one, which is the one in common. Please check that this is so. If this is not true, please use the most updated dump among those ones taken by the groups.

*We proceeded to use the dump the Don'tLockUp group used*

In Crossref data, in case a DOI is already specified by the publisher in one of the items of the reference list, is it changed by Crossref if they identify an error? Is this behaviour specified in some documentation?

*This is unclear; from [this](https://www.crossref.org/documentation/cited-by/cited-by-participation/) it appears Crossref takes the DOI as correct.*

Since you used a multithread approach to download data from Crossref, did you check that the Crossref API returned always good answers (i.e. HTTP status code 200)? How did you handle possible problems (e.g. when the request to Crossref returned a different HTTP status code)?

*We added a time.sleep function to avoid overloading the API*

During the presentation, someone said that the license of a journal affected, somehow, the license of all its data. How is it so? In particular, considering that bibliographic metadata and citations, in Crossref, are separate, it is entirely possible that the article has a different license from that specified to its metadata in Crossref. Thus, what did you mean by the initial claim?

*We were referring to the license of the metadata on the [DOAJ dump](https://doaj.org/docs/public-data-dump/); the fact is that the metadata from the journal is distributed in CC-BY-SA, making us distribute the data that combined from the journal with this license rather than CC0.*

During the presentation, you mentioned a concept, i.e. non-standard DOI. What does it mean? This is not a correct definition, so please provide an explanation about it.

*We meant badly formed DOIs, or DOIs in a format different from 10.prefic/suffix. We now added a piece of software that deals with the problem of normalising said DOIs. A more detailed answer about this is provided in the Article section*

In some of the diagrams presented in the discussion, it was not clear what the bars mean. Please, accompany always the diagrams with descriptions of what the various axis refer to.

*We provided better descriptions*

Similarly, the diagram with the circles is not clear. What does the dimension of the circles mean? The possible overlap between the circles has some specific meaning? If not, maybe it is not the correct kind of diagram to use to convey such information, since it may create ambiguities.

*We decided to use an alternative graph to be clearer in our exposition*

Among the articles not specifying any reference list, there is the possibility that its condition of not having a reference list is correct? For instance, often editorials of journal issues may not include reference lists at all, as well as letters. Were you able to identify, somehow, when the absence of reference lists is justified?

*We added this level of analysis in this version. This does not change substantially the state of data, but it was interesting to add.*

During the presentation, it seems that before 2000, according to the data published in Crossref, no DOIs are specified in the reference list. Is it really so? I would suggest checking it carefully, or to justify the claim.

*Data suggests that most references before 2000 do not have a DOI; this might be connected to the problem of retroactively give a DOI to articles, an effort that might not be easy for some publishers.*

Introduce approaches (to be even developed in future works) for correcting data that include Persian dates.

*We provided a possible description that could help preserve the use of calendars different from the one of Western Traditions; rather than using a single date, it could be possible to use a dictionary containing both a date and the type of calendar. As an example: date: date: [{year: 2022 type: 'gregorian'}]*

Clarify what measure you used to identify "smaller journals" - what is a "small journal"? What is the threshold used to differentiate it from a "big journal"? What is a "medium journal"?

*We mean those journals having a mean ad median number of articles lower than the median of the total sample. By saying this we do not refer to any previous classification made by other researchers.*

Including, in the analysis, also the publication type of the citing entity could be beneficial for the discussion of the results, I believe, since you can show if there are different behaviours depending on the kind of the citing entities.

*We tried this kind of analysis and we found that... .*
*In the new version of the project we added some visualizations – and the following analysis – showing the behaviour of journals belonging to different fuields. By doing this we followed [Library of Congress Classification of subjects & categorical](https://www.loc.gov/catdir/cpso/lcco/), grouping the journals into two macro-categories: Science Technology and Medical (STM) field or Social Sciences and Humanities field (SSH). We found out that (to be continued...)*

Did you use some approach to check about possible dumps in the original data, in particular those from Crossref? It is important to do this check, since it may happen that in a Crossref dump the same entity (i.e. the same citing DOI) is introduced twice or more times. It is, of course, a mistake from Crossref, but it happens and must be handled since it may affect the results of your analysis. How did you approach it?

*We used a dictionary for keeping track of the DOIs; since no duplicates are possible in this datatype, this problem is not possible.*

In answering one of the comments during the presentation, you said that Crossref modifies the metadata that is deposited to some extent. It is necessary to clarify if and how Crossref does it, in particular clarifying which metadata it modifies and providing specific source documentation that supports this claim.

*Crossref modifies the metadata of references by adding a DOI if it is not given. [This](https://www.crossref.org/documentation/cited-by/cited-by-participation/) should contain all the information about it*

Since Crossref may behave and return an unexpected result if queried simultaneously multiple times in the same time window, it would be necessary to develop some mechanism to even wait a few moments before querying the API.

*As anticipated above, we added sleep times for avoiding this kind of problem.*

## DMP
General points:

there are a few typos, please correct them.

*We reviewed the DMP to remove typos*

if you mention something in the description, please add links to it (e.g., when you mention Dublin Core, add the link to the vocabulary used)

*We have added links to the entities.*

### DOAJ and Crossref populated DATASET

1.1.1: it is not clear in this context what it means that "building the final dataframe". The dataframe is something you have in your mind, but it has not been clarified in the DMP at all. Please, be more generic or provide a clear description of what you refer to.

*We rephrased this point hoping to make it clearer*

1.1.2: add links to the Crossref API and DOAJ dump.

*We added the links*

1.1.3: it refers to the format used (CSV, JSON), not the content.

*We modified this element*

3.1.1.8: if it is possible, please add a brief description of the naming convention (how it works)

*We provided some examples*

3.1.1.13: how are you going to provide the metadata in Linked Open Data? It is not clear at all.

*We modified this part, as we are not providing it*

3.1.1.15: I doubt you have 8-bit ASCII honestly, considering that they do not allow you to represent all the characters. Are you sure about it?

*We removed this part as we had misunderstood it*

4.1.2: you say there are two people here, but you listed three in the following point.

*We clarified this point*

## La Chouffe SOFTWARE

3.1.1.3: but FRBR is a standardised vocabulary, isn't it? In addition, I could not see where you have such FRBR-based metadata about the software available. Did you create them? Where are they?

*This was mistakenly kept there, we removed it*

3.1.1.8: it is not clear how you have applied the naming convention to the software, that BTW should be explained a bit.

*We hope to have clarified this point*

3.1.1.13: how are you going to provide the metadata in Linked Open Data? It is not clear at all.

*We modified this part, as we are not providing it*

3.1.1.15: I doubt you have 8-bit ASCII honestly, considering that they do not allow you to represent all the characters. Are you sure about it?

*We removed this part as we had misunderstood it*

3.1.2.1: not clear how the reuse concerns ethics, here.

*We removed this part as we had misunderstood it*

3.1.2.9: "at the end of the project" is not really answering this question, right?

*This was in part a standard answer from Argos. We hope anyway to have explained it better*

4.1.2: you say there are two people here, but you listed three in the following point.

*We clarified this point*

6.1.1: it is not really concerned with ethics, it is just attribution, I would say.

*Rightfully so, we removed this point*

## DOAJ and Crossref aggregated DATASET

3.1.1.8: if it is possible, please add a brief description of the naming convention (how it works)

*We provided an example*

3.1.1.15: I doubt you have 8-bit ASCII honestly, considering that they do not allow you to represent all the characters. Are you sure about it?

*We removed this part as we had misunderstood it*

4.1.2: you say there are two people here, but you listed three in the following point.

*We hope to have clarified this point*

## DOAJ cleaned articles DATASET

3.1.1.8: if it is possible, please add a brief description of the naming convention (how it works)

*We provided an example of it.*

3.1.1.15: I doubt you have 8-bit ASCII honestly, considering that they do not allow you to represent all the characters. Are you sure about it?

*We removed this part as we had misunderstood it*

4.1.2: you say there are two people here, but you listed three in the following point.

*We hope to have clarified this point*

## Protocol
No particular comments, please just check again the text to correct a few typos.

*We hope to have removed typos and we added some more specification for the new software*

## Software

The README.md in the GitHub repository does not contain an appropriate introduction to run the software and, in particular, how to and in which order to call the various scripts to run the process correctly. In addition, you should also specify with which configuration (i.e. computer, processor, RAM, HD, etc.) you have run the scripts to get your final output since this is crucial to foster reproducibility. Finally, if the software is somehow related to other documents (the protocol, the article, the website, etc.), please mention them here in the README.md.

*We added a better description to run the software as well as description of the configuration and links to all resources*

Finally, the item on Zenodo describing the software is not linked via GitHub. I think you did not use the GitHub+Zenodo approach for uploading it on GitHub, as introduced during the lectures. This would guarantee that also a new version of the software will be assigned with version DOIs and automatically linked with the GitHub repository and the previous versions uploaded on Zenodo. Please, use the appropriate method to upload the software.

*We added the sofware in Zenodo in the correct way*

## Article

"to evaluate the management of data linked to articles (references)": talk explicitly about references, since "management of data linked to articles" can refer also to something else (e.g. supplementary material of an article, which is not included in references).

*We corrected this point*

"More than 10 percent of the world’s peer-reviewed journals are now included in DOAJ": does it mean 10% of all the journals published or 10% of the OA journals?

*This point was wrong overall, so we rewrote it*

Table 3, "Median/average number of articles": which articles are considered for this computation? DOAJ articles? It must be specified.

*We separated these two aspects*

Table 4, "uncertain date": what do you mean by "uncertain"? Unknown?

*We rephrased this as bad date format or unknown date*

"Humanities": Usually, the macro category should be "Humanities and Social Sciences". Can you please check this?

*We revised the format of the categories as STM and SSH.*

"not distributed in a decisive way": what does it mean?

*We meant the distribution does not paint a clear picture; we hope to have clarified the point in the article.*

"they have very different degrees of metadata quality": what do you mean? Did you have checked every single field to measure its quality?

*This was referring to a possible explanation for the problem of ditribution of DOIs on Crossref; we could not check this, clearly, but we referred to other literature that had this point.*

"Some of the articles did not provide a DOI but a link (e.g., dx.DOI.org/DOI)": be aware that, in the community, specifying a DOI or a DOI URL (e.g. https://doi.org/10.1234/askdjsk), is equivalent! Of course, it is different if in Crossref there is the field DOI specified in the object defining a cited object or if it is only included in the plain text of the reference list.

*You are right, so we decided to use a different algorithm and normalise the DOIs that we were given.*

"Smaller journals have less attention to metadata": can you speculate about a reason for this situation?

*This could be linked to:*
- lack of funds
- lack of expertise or possibilities for the production of metadata
- journals that are not publishing anymore

"for the articles with alternative calendars from the Gregorian": it would be good to add examples.

*We added an example for this*

"Initiative for Open Citations": linked needed.

*Link added*

"For older articles": define "older" here. Before 2000? Before 1900?

*We clarified for before 2000*

"by the fact that newer articles tend to cite more recent articles that have a DOI": this claim should be supported somehow. It is very strong.

*We agree that this claim is too strong and we do not have data over cited entities publication to support it. Thus, we have rephrased our speculation and made clear that this is an hypothesis made after analysing the increasing or decreasing over time of the amount of DOIs in articles' reference lists. Therefore we suggest this point as a new research topic.*

All figures should be moved within the content, close to where they are mentioned for the very first time, otherwise, it is very difficult to read the article.

*We made this change*

Is figure 3 really necessary, considering that it includes just one piece of information that can be explained in one sentence? Maybe, it can be worth combining it with Figure 8.

*We decided to combine them*

Figure 15 is unreadable. My suggestion is to use colouring of the area of the countries instead of circles.

*We decided to substitute it with a different figure*

Figure 13 and Figure 16 can be collapsed into just one graph, I believe.

*We collapsed it in a sunburst visualization*

Please, carefully read the article again to correct typos and other mistakes.

*We proofread the article correcting the mistakes*

Thanks for the comments. Please notify us if any more change is needed.

Team La Chouffe