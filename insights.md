---
source: https://chatgpt.com/c/69fc23ad-b9c8-83ea-a6eb-13ced1a7c281
---

# Recommendations

> Here is the DuckDB dataset. What are the top recommendations you can share for each publisher to improve their impact factor, and why?

I treated this as an **impact-factor proxy**, not true JIF, because the DuckDB has `cited_by_count` but not citation-year data or citable-item classification. So the analysis answers: “Which actions are most likely to improve citation density and future impact-factor-like performance?”

Dataset caveats: 1,128 works, 106 sources, 5 publishers. Funders table is empty, so I cannot make funding-body recommendations from this file. The domain slice is also noisy: it includes broad sources like The Lancet, CHEST, British Journal of Surgery, Value in Health, Advanced Functional Materials, etc. So these are MVP recommendations, not final client-grade claims.

## Overall finding

In this OpenAlex slice, the publisher-level citation-density ranking is:

| Publisher               | Works | Avg citations/work | Median | OA share | Retracted |
| ----------------------- | ----: | -----------------: | -----: | -------: | --------: |
| Springer Nature         |   103 |               50.1 |   15.0 |    77.7% |         0 |
| PLOS                    |   299 |               15.2 |    6.0 |   100.0% |         0 |
| Wiley                   |   452 |                7.8 |    0.0 |    64.4% |         0 |
| Oxford University Press |   120 |                6.2 |    0.0 |    85.8% |         0 |
| Elsevier BV             |   154 |                5.7 |    1.0 |    42.9% |         1 |

The strongest cross-publisher opportunity topics in this slice are:

**visual perception and processing**, **neuroendocrine regulation and behavior**, **functional brain connectivity**, **action observation and synchronization**, **nerve injury and regeneration**, **face recognition and perception**, **neural dynamics and brain function**, **mental health research topics**, **advanced memory and neural computing**, and **stress responses/cortisol**.

These combine reasonable recent momentum with high mature citation density.

## Elsevier BV

**Top recommendation: rebuild the neuroscience topic mix around cognitive/neural systems rather than broad biomedical residue.**

Elsevier has the weakest average citation density in this slice: **154 works, 5.7 citations/work**, with several low-yield sources contributing volume: Biophysical Journal has **24 works, 2.8 avg citations**, CHEST has **17 works, 0.9**, Value in Health has **8 works, 0.0**, and Journal of Biological Chemistry has **8 works, 2.6**. Brain Research is the bright spot at **22 works, 12.9 avg citations**.

Elsevier is under-indexed in several high-opportunity topics: **visual perception and processing** has 26 market works and 58.5 mature avg citations, but Elsevier has zero; **face recognition and perception** has 21 market works and strong growth, but Elsevier has zero; **functional brain connectivity** has 128 market works and 38.5 mature avg citations, but Elsevier has only 8 works and low publisher share.

**Action:** commission special issues or invited reviews in visual perception, functional connectivity, face recognition, mental health, and neural dynamics. Use Brain Research as the natural anchor journal, not the broad biomedical journals.

**Institution outreach:** Elsevier has little or no presence among high-citation peer institutions in this slice: Allen Institute for Brain Science, Allen Institute, HHMI, NYU, Columbia, Trinity College Dublin, Yonsei, University Hospital Heidelberg, Washington University in St. Louis. These are the first outreach targets.

**Integrity action:** one Elsevier work is flagged as retracted. Not a large count, but useful in the demo: “impact improvement is not just more papers; it is better topic, institution, and risk selection.”

## Oxford University Press

**Top recommendation: reduce over-concentration in Neuro-Oncology and diversify into high-citation cognitive neuroscience.**

OUP has **120 works, 6.2 citations/work**, but the portfolio is extremely concentrated: **Neuro-Oncology has 54 works but only 0.17 avg citations** in this slice. This may partly be citation lag because many are recent, but it still creates an impact-factor risk: lots of recent denominator, weak observed citation pull so far.

The best-performing OUP sources are elsewhere: **Physical Therapy has 11 works, 26.5 avg citations**, **Genetics has 5 works, 29.2**, and **Nucleic Acids Research has 6 works, 17.2**.

OUP is nearly absent from the strongest opportunity topics: **visual perception**, **action observation**, **neural dynamics**, **mental health**, **advanced memory/neural computing**, and **memory/neural mechanisms**. It has some glioma volume, but glioma is not the highest citation-density opportunity in this slice.

**Action:** keep Neuro-Oncology, but do not make “more neuro-oncology articles” the core impact strategy. Instead, launch invited reviews / special collections at the intersection of neuro-oncology with functional brain connectivity, neuroimaging, cognition, and mental health outcomes.

**Institution outreach:** high-priority targets where peers are getting stronger citation pull include Universidade de São Paulo, HHMI, Yale, Trinity College Dublin, Yonsei, Allen Institute, EPFL, MIT, UCLA, and UC Berkeley.

**Operational action:** distinguish “recent uncited because too new” from “structurally low-citation.” For OUP, this matters because Neuro-Oncology has many 2024–2025 works. The next dataset should add article type, citation-year, and early attention/downloads.

## Public Library of Science

**Top recommendation: PLOS should use its OA advantage to win emerging translational and computational neuroscience clusters.**

PLOS is healthy in this slice: **299 works, 15.2 citations/work, 100% OA**, with strong source performance from **PLOS Computational Biology: 108 works, 20.0 avg citations** and **PLOS Biology: 31 works, 19.6**. PLOS ONE is lower but still respectable at **154 works, 11.5**.

PLOS is under-indexed in high-opportunity topics such as **nerve injury and regeneration**, **neurotransmitter receptor influence on behavior**, **glioma diagnosis and treatment**, **traumatic brain injury**, **psychedelics and drug studies**, and **genetics/neurodevelopmental disorders**.

**Action:** create three editorial packages: “Computational neuroscience and functional connectivity,” “Translational neuro-regeneration and injury,” and “Psychedelics / mental health / neurobehavioral interventions.” Route the strongest computational papers to PLOS Computational Biology or PLOS Biology rather than letting everything land in PLOS ONE.

**Quality action:** PLOS has some high-volume but weaker topic areas: photoreceptor/optogenetics has 19 PLOS works but only 6.0 avg citations versus 11.7 market average; neuroendocrine regulation has 7 PLOS works at 4.7 avg citations versus 35.2 market average. This suggests either lower-fit submissions or weaker article formats in otherwise attractive topics.

**Institution outreach:** prioritize Yonsei, Emory, Universidade de São Paulo, Vrije Universiteit Brussel, KIST, University of Kentucky, University of Maryland Baltimore, Ghent, Renmin University of China, and Pain in Motion.

## Springer Nature

**Top recommendation: defend the premium psychiatry/neuropsychopharmacology position, but add adjacent cognitive-neuroscience growth topics.**

Springer is the clear citation-density leader in this slice: **103 works, 50.1 citations/work**. This is driven mainly by **Neuropsychopharmacology: 37 works, 73.5 avg citations** and **Molecular Psychiatry: 33 works, 65.5**. This is exactly the kind of concentrated, high-citation portfolio that improves an impact-factor-like metric.

The risk is over-narrowness. Springer is under-indexed in **visual perception**, **action observation**, **face recognition**, **advanced memory/neural computing**, **EEG and brain-computer interfaces**, and **glioma diagnosis**. It has some functional connectivity, but still a low share relative to the market.

**Action:** do not chase volume. Instead, commission high-selectivity reviews and perspective pieces connecting molecular psychiatry/neuropsychopharmacology to functional connectivity, cognition, digital phenotyping, and computational psychiatry.

**Portfolio hygiene:** low-yield/noisy sources in this slice include Scientific American and Pediatric Research with zero citations in the selected set, plus Molecular Biology Reports at 6.7 avg citations. For impact-factor improvement, keep these out of the hero journal cohort unless they are intentionally part of the client story.

**Institution outreach:** Springer’s biggest gaps are Allen Institute, University of Maryland Baltimore, HHMI, Yonsei, Pain in Motion, MIT, Vrije Universiteit Brussel, Princeton, Broad Institute, and KIST.

## Wiley

**Top recommendation: fix citation dilution from high-volume, low-citation source/topic pockets.**

Wiley has the largest volume in the dataset: **452 works**, but only **7.8 citations/work** and median citation count is **0**. The main dilution is obvious: **Alzheimer’s & Dementia has 193 works but only 1.5 avg citations**, and **The FASEB Journal has 71 works but only 1.3**. In contrast, Wiley has strong pockets: **Annals of the New York Academy of Sciences: 26 works, 35.0 avg citations**, **Advanced Functional Materials: 23 works, 23.6**, **Small: 11 works, 18.9**, **Journal of Physiology: 32 works, 13.1**, and **Angewandte Chemie International Edition: 9 works, 32.4**.

Wiley is under-indexed in **face recognition and perception**, **glioma diagnosis and treatment**, **child/adolescent psychosocial development**, **genetics and neurodevelopmental disorders**, **musculoskeletal pain/rehabilitation**, and **advanced fluorescence microscopy**.

**Action:** separate “volume management” from “impact-factor improvement.” For impact improvement, push more invited reviews, methods papers, and synthesis articles into the high-performing journals. For Alzheimer’s & Dementia and FASEB, analyze article type and submission source; the current volume looks like denominator expansion without enough citation return.

**Specific red flag:** Wiley has **6 works in nerve injury/regeneration at 0.17 avg citations**, while the market average for that topic is **39.9**. That topic is not necessarily bad; Wiley’s slice of it appears bad. This is a perfect demo example of “topic alone is not enough; author/institution/article-type quality matters.”

**Institution outreach:** prioritize Allen Institute, Pain in Motion, Vrije Universiteit Brussel, HHMI, Central Institute of Mental Health, University of Liège, University of Tokyo, Norwegian University of Life Sciences, Allen Institute for Brain Science, and EPFL.

## Best demo narrative

The strongest story is:

“Impact factor is not improved by publishing more. It is improved by changing the numerator/denominator economics: fewer low-citation articles, more high-citation article types, better topic timing, stronger institutions, and lower research-integrity risk.”

For the client demo, show three levers per publisher:

1. **Topic lever:** which rising topics they are missing.
2. **Institution lever:** which high-citation institutions publish with competitors but not them.
3. **Portfolio lever:** which journals/topics are adding volume without citation return.

The most commercially useful pitch is: “We can deliver this quarterly as an editorial intelligence report, then track whether recommended topic/institution interventions improve citation momentum.”

# Changes

> For each of them, share what's happened in 2025 that's a change compared with before and therefore represents a risk or an opportunity to their impact factor. Share recommendations with supporting evidence. Give concrete / specific evidence and examples to make it real.

I used **2020–2024 as the baseline** and **2025 as the change year**. I’m ignoring 2026 because it is partial.

Important caveat: 2025 papers are still young, so their citations are early signals. The real impact-factor risk/opportunity is not “2025 papers have few citations now”; it is whether 2025 has changed the **future numerator/denominator economics**: more citable items, weaker article mix, fewer reviews, weaker journals, better topics, better institutions, or more OA visibility.

## Executive takeaways

The most important 2025 pattern is this:

| Publisher       | 2025 change vs 2020–24 annual avg | Main impact-factor signal                                                                                                                                                                                         |
| --------------- | --------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Elsevier BV     |                        -2% volume | Stable volume, but OA share dropped and one 2025 retraction appeared. Brain Research produced one very strong review.                                                                                             |
| OUP             |                       +57% volume | Big Neuro-Oncology surge, mostly very low-citation early items. Potential denominator risk unless these are non-citable meeting abstracts or later convert to strong citations.                                   |
| PLOS            |                       +24% volume | More PLOS ONE volume, but strongest early signals are in PLOS Computational Biology / Digital Health. Risk of diluting impact if volume stays too generic.                                                        |
| Springer Nature |                        -4% volume | Still has the best high-impact assets, but 2025 shifts away from its historically review-heavy, high-citation pattern.                                                                                            |
| Wiley           |                       -12% volume | Good news: volume fell in low-yield FASEB / Alzheimer’s & Dementia pockets and OA share rose sharply. Opportunity to double down on reviews and high-performing physiology/materials/neural-engineering journals. |

One cross-cutting recommendation: **commission more high-quality reviews and perspective articles.** In this dataset, reviews have a strong citation premium almost everywhere:

| Publisher       | 2020–24 avg cites/article | 2020–24 avg cites/review |
| --------------- | ------------------------: | -----------------------: |
| Elsevier BV     |                       4.2 |                     24.5 |
| PLOS            |                      18.5 |                     50.3 |
| Springer Nature |                      16.2 |                     95.6 |
| Wiley           |                       5.5 |                     36.9 |

## Elsevier BV

**What changed in 2025**

Elsevier’s volume stayed roughly flat: **24 works in 2025 vs 24.6/year during 2020–24**. But the mix worsened on two dimensions.

First, **OA share fell** from **46% before 2025 to 29% in 2025**. In a citation-growth strategy, that is a visibility risk.

Second, Elsevier has **one 2025 retraction/withdrawal flag**: “WITHDRAWN: 2212eP Outcomes in pain management following a pain neuroscience education program…” in **Annals of Oncology**. It has zero citations, but the risk is reputational/editorial, not citation count.

The positive change is **Brain Research**. It rose to **6 works in 2025 vs 2.8/year before**, and one paper is already a standout: **“The neuroplastic brain: current breakthroughs and emerging frontiers”**, a 2025 review in Brain Research, already at **50 citations**. That is the kind of paper that can move future impact metrics.

**Risk**

Elsevier has too much 2025 activity in weakly aligned or low-early-citation sources. For example:

| Source                                             | 2020–24 works | 2025 works | 2025 avg cites |
| -------------------------------------------------- | ------------: | ---------: | -------------: |
| International Journal of Biological Macromolecules |             3 |          3 |            0.3 |
| Food Chemistry                                     |             1 |          2 |            1.0 |
| Chemical Engineering Journal                       |             2 |          2 |            3.5 |

Some of these are scientifically adjacent but not strong neuroscience editorial bets. Examples include fruit/vegetable preservation films, food-flavor EEG, spinal cord scaffolds, and amyloid-binding cryogels. They may be valid papers, but they do not build a coherent neuroscience impact story.

**Opportunity**

Elsevier’s strongest opportunity is to make **Brain Research** the editorial spearhead and commission more frontier/review pieces. The 2025 evidence is very clear: Elsevier’s 2025 reviews average **12.8 citations**, while 2025 articles average **1.2**.

Also, Elsevier is missing several 2025 market-growth topics where competitors are active:

| Missed topic                            | Market signal                                             |
| --------------------------------------- | --------------------------------------------------------- |
| Stress responses and cortisol           | 2.5x 2025 growth vs baseline; 2020–24 avg 108.8 citations |
| Functional brain connectivity           | 8 market works in 2025; 2020–24 avg 36.1 citations        |
| Single-cell and spatial transcriptomics | 4x 2025 growth; 2020–24 avg 28.0 citations                |
| Behavioral health interventions         | 5x 2025 growth; 2020–24 avg 49.0 citations                |

**Recommendation**

For Elsevier, recommend: **“Turn Brain Research into a frontier-review engine.”**

Concrete actions:

Commission 6–8 invited reviews in neuroplasticity, functional connectivity, stress/cortisol, single-cell neurobiology, and behavioral-health interventions. Use the successful 2025 Brain Research review as the proof point: one review already has 50 citations.

Raise OA availability for the target neuroscience journals. The 2025 OA share drop from 46% to 29% is a citation-risk signal.

Add a research-integrity screen for conference/proceeding-like items and pain/intervention studies. The 2025 withdrawal gives a real example for why this belongs in the service.

## Oxford University Press

**What changed in 2025**

OUP had the biggest volume jump: **28 works in 2025 vs 17.8/year during 2020–24**, a **57% increase**.

Almost all of that jump came from **Neuro-Oncology**:

| Source         | 2020–24 works | 2025 works |                   Change |
| -------------- | ------------: | ---------: | -----------------------: |
| Neuro-Oncology |            32 |         22 | +15.6 vs annual baseline |

This creates a potential impact-factor denominator risk. Many 2025 Neuro-Oncology items have titles that look like meeting abstracts or short proceedings-style outputs, for example:

“CNSC-66. Spatially constrained gliomagenesis…”
“NCOG-06. Multimodal management of meningioma…”
“IMG-98. Metabolic response using the PET RANO 1.0 criteria…”
“CAN A DEDICATED NEURO-ONCOLOGY AHP SERVICE REDUCE LENGTH OF STAY…”

In the dataset, Neuro-Oncology’s 2025 works average only **0.05 citations** so far.

**Risk**

If these 2025 items are counted as citable articles, OUP has a real denominator problem: many new citable items, very low early citation return. If they are not citable JIF items, then the risk is smaller, but the portfolio still looks noisy.

The topic-level concentration is also sharp. **Glioma diagnosis and treatment** rose to **9 OUP works in 2025 vs 1.8/year before**, but those 2025 OUP glioma works average only **0.11 citations** so far.

**Opportunity**

The opportunity is to convert the Neuro-Oncology volume into higher-impact article formats. OUP’s stronger 2025 signals are not from the bulk Neuro-Oncology items; they are from more substantial articles/reviews:

“Elucidating brain transport pathways and cell type-dependent gene silencing…” in **Nucleic Acids Research**, **5 citations**.

“Taking the Next Step in Neurologic Rehabilitation…” in **Physical Therapy**, a review, **4 citations**.

OUP is also lightly present or absent in higher-value topics that are relevant to neuro-oncology:

| Topic                                   | Market evidence                                    |
| --------------------------------------- | -------------------------------------------------- |
| Single-cell and spatial transcriptomics | 4x 2025 growth; 2020–24 avg 28.0 citations         |
| Functional brain connectivity           | 8 market works in 2025; 2020–24 avg 36.1 citations |
| Neuroscience and neural engineering     | 8 market works in 2025; 2020–24 avg 27.8 citations |
| RNA interference / gene delivery        | OUP’s 2025 NAR example already has 5 citations     |

**Recommendation**

For OUP, recommend: **“Stop treating Neuro-Oncology as a volume engine; turn it into a high-citation translational neuro-oncology engine.”**

Concrete actions:

Audit whether 2025 Neuro-Oncology items are JIF-citable. If yes, tighten what gets counted as article-like content.

Commission special issues on glioma plus **single-cell/spatial transcriptomics**, **immunotherapy distribution**, **functional connectivity**, **AI-driven neuro-oncology reporting**, and **RNA/gene-delivery therapies**.

Use Nucleic Acids Research and Physical Therapy as internal exemplars: fewer, deeper, more citable papers beat more low-citation proceedings-style items.

## Public Library of Science

**What changed in 2025**

PLOS volume rose: **56 works in 2025 vs 45.2/year during 2020–24**, a **24% increase**.

The increase is concentrated in **PLOS ONE**:

| Source                     | 2020–24 works | 2025 works | 2025 avg cites |
| -------------------------- | ------------: | ---------: | -------------: |
| PLOS ONE                   |           115 |         32 |           1.25 |
| PLOS Computational Biology |            87 |         16 |           2.69 |
| PLOS Biology               |            22 |          5 |           4.20 |
| PLOS Digital Health        |             0 |          2 |           6.00 |

PLOS remains **100% OA**, which is a structural advantage.

**Risk**

The risk is not OA; PLOS already has that. The risk is **volume drifting into PLOS ONE instead of higher-signal venues**. PLOS ONE has 32 of the 56 PLOS works in 2025, but the strongest early signals are elsewhere.

Only **1 of 56 PLOS 2025 works is a review**, even though PLOS reviews in 2020–24 averaged **50.3 citations**, versus **18.5** for articles. That is a missed impact-factor lever.

**Opportunity**

PLOS has several strong 2025 examples that show what to scale:

“A comprehensive investigation of intracortical and corticothalamic models of the alpha rhythm” — **PLOS Computational Biology**, 9 citations.

“Meta-Reinforcement Learning reconciles surprise, value, and control in the anterior cingulate cortex” — **PLOS Computational Biology**, 8 citations.

“Revealing non-trivial information structures in aneural biological tissues via functional connectivity” — **PLOS Computational Biology**, 7 citations.

“Community perspectives regarding brain-computer interfaces…” — **PLOS Digital Health**, 7 citations.

“DomeVR: Immersive virtual reality for primates and rodents” — **PLOS ONE**, 5 citations.

The topic changes are also promising. In 2025, PLOS newly or increasingly entered:

| Topic                            | PLOS 2025 signal                                      |
| -------------------------------- | ----------------------------------------------------- |
| Advanced fluorescence microscopy | 3 works, up from zero before                          |
| Behavioral health interventions  | 2 works, market topic has 49.0 baseline avg citations |
| Zebrafish biomedical research    | 2 works, market growing 3.75x                         |
| Advanced neuroimaging            | 2 works                                               |
| Virtual reality applications     | 1 work, already 5 citations                           |

**Recommendation**

For PLOS, recommend: **“Use PLOS Computational Biology, PLOS Biology, and PLOS Digital Health as the impact engines; use PLOS ONE as discovery volume, not the main impact lever.”**

Concrete actions:

Create quarterly calls for papers on computational neuroscience, BCI, VR/neurotech, neuroimaging, and behavioral-health interventions.

Increase invited reviews. A 2025 portfolio with only 1 review is underusing the strongest historical citation lever.

Route strong computational/neurotech papers away from generic PLOS ONE placement when possible. The early 2025 evidence shows PCBio and Digital Health are already producing better citation velocity.

## Springer Nature

**What changed in 2025**

Springer’s volume stayed roughly flat: **15 works in 2025 vs 15.6/year during 2020–24**. But the **article-format mix changed in a risky way**.

During 2020–24, Springer’s dataset was unusually review-heavy:

| Period  | Articles | Reviews | Review share |
| ------- | -------: | ------: | -----------: |
| 2020–24 |       30 |      48 |          62% |
| 2025    |       10 |       5 |          33% |

That matters because Springer’s 2020–24 reviews averaged **95.6 citations**, versus **16.2** for articles.

**Risk**

Springer’s strongest impact assets remain **Molecular Psychiatry** and **Neuropsychopharmacology**, but 2025 volume in both is lower than baseline:

| Source                  | 2020–24 works | 2025 works | Change vs annual baseline |
| ----------------------- | ------------: | ---------: | ------------------------: |
| Neuropsychopharmacology |            30 |          4 |                      -2.0 |
| Molecular Psychiatry    |            26 |          4 |                      -1.2 |

Meanwhile, 2025 includes some noisy or low-impact sources in this domain slice: **Scientific American**, **BDJ**, and a strange source label, **Journal of materials research/Pratt's guide to venture capital sources**, all with zero citations in 2025. This may be a data-selection artifact, but it is exactly the kind of thing the production workflow should filter out.

**Opportunity**

Springer’s 2025 high-citation examples are excellent and very concrete:

“Precision psychiatry roadmap: towards a biology-informed framework for mental disorders” — **Molecular Psychiatry**, review, **32 citations**.

“Brain circuits that regulate social behavior” — **Molecular Psychiatry**, review, **30 citations**.

These map to historically strong topics:

| Topic                                   | Springer evidence                                                                   |
| --------------------------------------- | ----------------------------------------------------------------------------------- |
| Mental health research topics           | Springer 2025 work has 32 citations; market baseline avg 78.8                       |
| Neuroendocrine regulation and behavior  | Springer 2025 work has 30 citations; market baseline avg 84.8                       |
| Psychedelics and drug studies           | Existing market baseline avg 31.3; Springer has 2025 DMT/connectome-harmonics paper |
| Single-cell and spatial transcriptomics | 4x market growth in 2025; Springer has 2 new 2025 works                             |

**Recommendation**

For Springer, recommend: **“Protect the premium review-led psychiatry franchise; do not let the portfolio become article-heavy and noisy.”**

Concrete actions:

Restore the review/perspective ratio in Molecular Psychiatry and Neuropsychopharmacology. The 2025 review share drop from 62% to 33% is the clearest risk.

Commission reviews on precision psychiatry, social-behavior circuits, psychedelics, single-cell psychiatry, and connectome-based mental-disorder classification.

Filter the domain-source set more tightly before showing clients. Springer looks strongest when the analysis focuses on Molecular Psychiatry / Neuropsychopharmacology, not broad or noisy sources.

## Wiley

**What changed in 2025**

Wiley volume fell: **66 works in 2025 vs 74.6/year during 2020–24**, a **12% decline**.

That sounds bad, but the mix improved in important ways.

First, OA share rose sharply: **61% before 2025 to 86% in 2025**. That is a discoverability opportunity.

Second, volume fell in some historically low-yield pockets:

| Source                 | 2020–24 works | 2025 works | 2020–24 avg cites |
| ---------------------- | ------------: | ---------: | ----------------: |
| The FASEB Journal      |            70 |          0 |               1.3 |
| Alzheimer’s & Dementia |           170 |         23 |               1.6 |

Third, volume rose in stronger sources:

| Source                                     | 2020–24 works | 2025 works | 2020–24 avg cites |
| ------------------------------------------ | ------------: | ---------: | ----------------: |
| The Journal of Physiology                  |            23 |          8 |              16.8 |
| Annals of the New York Academy of Sciences |            18 |          7 |              49.8 |
| Advanced Functional Materials              |            17 |          5 |              30.6 |
| Small                                      |             8 |          2 |              24.9 |

**Risk**

Wiley still has a dilution problem. **Alzheimer’s & Dementia** has 23 works in 2025, but only **0.96 avg citations** so far. Some may be late-2025 and too new, but this remains a watch item.

Also, Wiley’s 2025 reviews average **5.1 citations**, much lower than its 2020–24 review average of **36.9**. That may be pure citation lag, but it means the 2025 review portfolio needs monitoring.

**Opportunity**

Wiley has several strong 2025 signals:

“Clinical neurocardiology: defining the value of neuroscience-based cardiovascular therapeutics – 2024 update” — **The Journal of Physiology**, review, **22 citations**.

“The science does not yet support regulatory approval of amyloid-targeting therapies…” — **Alzheimer’s & Dementia**, **16 citations**.

“Conducting Polymer Microelectrode Arrays for Simultaneous Electrophysiology and Advanced Brain Imaging” — **Advanced Functional Materials**, **8 citations**.

“Molecular insights into modulation of the 5-HT2A receptor by serotonin, psilocin…” — **FEBS Letters**, **7 citations**.

“A neuroscience perspective on the plasticity of the social and relational brain” — **Annals of the NYAS**, review, **7 citations**.

The 2025 topic mix also improved in some useful directions:

| Topic                                  | Wiley 2025 signal                               |
| -------------------------------------- | ----------------------------------------------- |
| Neuroscience and neural engineering    | 6 works, market growing 2.1x                    |
| Action observation and synchronization | 2 works, market growing sharply                 |
| Advanced MRI techniques                | 2 works                                         |
| Photochromic / fluorescence chemistry  | 2 works                                         |
| Stress responses and cortisol          | 1 work, high historical market citation density |

**Recommendation**

For Wiley, recommend: **“Keep shifting away from low-yield volume and toward review-led physiology, neuroengineering, materials-neuroscience, and translational Alzheimer’s debates.”**

Concrete actions:

Double down on The Journal of Physiology, Annals of NYAS, Advanced Functional Materials, Small, and FEBS Letters as the impact-improvement engines.

Use Alzheimer’s & Dementia selectively: fewer routine items, more debate-setting reviews, guidelines, consensus pieces, and high-controversy translational articles. The 16-citation amyloid-therapy article shows that critical/regulatory-position pieces can travel.

Exploit the OA jump. Wiley’s 2025 OA share rose to 86%; now pair OA with stronger article formats and institutional outreach rather than treating OA alone as sufficient.

## The recommendations I would put in the client-facing report

For each publisher, the report should say:

Elsevier: **“Brain Research is working; the rest of the 2025 neuroscience slice is too diffuse. Increase OA, commission frontier reviews, and tighten integrity screening.”**

OUP: **“Neuro-Oncology volume surged in 2025. This is an opportunity only if converted from proceedings-style volume into high-citation translational neuro-oncology themes.”**

PLOS: **“The OA machine is strong, but the 2025 growth is too PLOS ONE-heavy. Move the best computational, BCI, VR, and neuroimaging work into higher-signal journals and commission more reviews.”**

Springer Nature: **“The premium psychiatry franchise is still the benchmark, but 2025 became less review-heavy. Restore the review/perspective engine around precision psychiatry, circuits, psychedelics, and single-cell psychiatry.”**

Wiley: **“Wiley’s 2025 mix improved: less low-yield FASEB/Alzheimer’s volume, more OA, more physiology/materials/neural-engineering. Now make it review-led and selective.”**
