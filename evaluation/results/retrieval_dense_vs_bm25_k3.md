# Retrieval Evaluation — Dense vs BM25

- Corpus: 9 PDFs, 613 chunks
- Questions: 124 (out-of-scope excluded)
- k = 3 retrieved chunks per question (same as the app)
- Dense = nomic-embed-text + prefix (the app's retriever)
- BM25 (raw) = keyword search on lowercase words
- BM25 + stopwords = same, without common English words (scikit-learn ENGLISH_STOP_WORDS)
- Hybrid = Dense + BM25 + stopwords, top 10 of each merged with Reciprocal Rank Fusion

## 1. Results per question type

| Type | Questions | Dense Hit@3 | Dense MRR | BM25 (raw) Hit@3 | BM25 (raw) MRR | BM25 + stopwords Hit@3 | BM25 + stopwords MRR | Hybrid Hit@3 | Hybrid MRR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| factual | 29 | 83% | 0.67 | 66% | 0.51 | 83% | 0.64 | 83% | 0.68 |
| conceptual | 31 | 81% | 0.71 | 65% | 0.59 | 68% | 0.59 | 74% | 0.71 |
| paraphrased | 34 | 53% | 0.40 | 44% | 0.37 | 47% | 0.39 | 59% | 0.50 |
| lexical | 30 | 90% | 0.85 | 73% | 0.52 | 97% | 0.82 | 97% | 0.93 |
| TD questions | 12 | 83% | 0.61 | 67% | 0.51 | 75% | 0.51 | 75% | 0.65 |
| **All** | 124 | 76% | 0.65 | 61% | 0.49 | 73% | 0.60 | 77% | 0.70 |

## 2. Complementarity (Dense vs BM25 + stopwords)

| | Questions |
|---|---:|
| Found by both | 77 |
| Missed by Dense, found by BM25 | 13 |
| Missed by BM25, found by Dense | 17 |
| Missed by both | 17 |
| **Found by at least one** | **107 / 124 (86%)** |

## 3. Missed by Dense, found by BM25

| id | Type | Question | Expected pages | Dense retrieved | BM25 retrieved |
|---|---|---|---|---|---|
| hadoop-fact-01 | factual | What are the low-level components of the Hadoop ecosystem presented in the course? | 4-hadoop-eco p2, 4-hadoop-eco p5 | 4-hadoop-eco p1, 4-hadoop-eco p4, 4-hadoop-eco p3 | 4-hadoop-eco p1, 4-hadoop-eco p5, 4-hadoop-eco p19 |
| hadoop-conc-06 | conceptual | What is the main difference between Yarn and Kubernetes? | 4-hadoop-eco p46 | intro.pdf p56, 4-hadoop-eco p37, 4-hadoop-eco p40 | 4-hadoop-eco p46, 4-hadoop-eco p40, 4-hadoop-eco p1 |
| hadoop-para-05 | paraphrased | How does the cluster keep data safe if a whole server rack goes down? | 4-hadoop-eco p32, intro.pdf p42 | 3-failure-an p27, intro.pdf p39, 4-hadoop-eco p31 | intro.pdf p10, 4-hadoop-eco p32, intro.pdf p42 |
| hadoop-para-07 | paraphrased | How can a company share cluster capacity between several teams? | 4-hadoop-eco p47, 4-hadoop-eco p48, intro.pdf p53 | 1-Introducti p7, 1-Introducti p35, intro.pdf p26 | 1-Introducti p35, 4-hadoop-eco p48, intro.pdf p5 |
| nosql-para-02 | paraphrased | Why can't Hadoop update a single record in place inside a file? | 1.1-comparis p13, 1.1-comparis p22, 4-hadoop-eco p23, TD2-part1-sp p25 | intro.pdf p91, 4-hadoop-eco p27, intro.pdf p42 | TD2-part1-sp p25, intro.pdf p90, 1-Introducti p44 |
| nosql-para-04 | paraphrased | What can go wrong when a huge Spark job replaces its old output with new output? | 1.1-comparis p8, 1.1-comparis p9 | 1-Introducti p22, TD2-part1-sp p7, 1-Introducti p87 | 4-hadoop-eco p77, intro.pdf p94, 1.1-comparis p9 |
| nosql-lex-02 | lexical | What is a .crc file used for? | 1.1-comparis p7 | 1-Introducti p42, TD2-part1-sp p27, 1-Introducti p43 | 1.1-comparis p7, intro.pdf p124, 1-Introducti p51 |
| spark-fact-02 | factual | What are the roles of the driver and the executors? | 1-Introducti p23, TD1-spark-sh p85 | 1-Introducti p59, 1-Introducti p55, intro.pdf p24 | 1-Introducti p94, TD1-spark-sh p85, 1-Introducti p55 |
| spark-fact-03 | factual | What is a task in Spark? | 1-Introducti p27 | TD1-spark-sh p30, TD1-spark-sh p44, TD1-spark-sh p93 | 1-Introducti p27, 1.1-comparis p7, 1.1-comparis p11 |
| spark-conc-08 | conceptual | Why does Spark use immutable datasets and a functional API instead of loops? | 1-Introducti p40, 1-Introducti p41, 1-Introducti p48 | TD1-spark-sh p85, 1-Introducti p47, TD2-part1-sp p3 | 1-Introducti p98, TD1-spark-sh p50, 1-Introducti p41 |
| spark-lex-04 | lexical | What is TimSort used for in Spark? | 1-Introducti p76, 1-Introducti p80 | TD1-spark-sh p58, TD1-spark-sh p85, TD1-spark-sh p30 | TD1-spark-sh p33, intro.pdf p124, 1-Introducti p76 |
| spark-lex-10 | lexical | What are DeltaLake and Iceberg used for in Spark? | 1-Introducti p44, 1-Introducti p45 | intro.pdf p65, TD2-part1-sp p25, 1.1-comparis p26 | 1-Introducti p45, 1-Introducti p44, 1.1-comparis p25 |
| td-01 | conceptual | Why is it better to write fewer, bigger Parquet files than many small files? | 4-hadoop-eco p27, 4-hadoop-eco p28, 1-Introducti p52, intro.pdf p91 | intro.pdf p92, TD2-part2-sp p9, TD2-part2-sp p3 | 1.1-comparis p30, 1-Introducti p52, intro.pdf p91 |

## 4. Missed by BM25, found by Dense

| id | Type | Question | Expected pages | Dense retrieved | BM25 retrieved |
|---|---|---|---|---|---|
| hadoop-fact-04 | factual | What kind of data store is ZooKeeper? | 4-hadoop-eco p10, 4-hadoop-eco p17 | 4-hadoop-eco p17, 4-hadoop-eco p8, 3-failure-an p48 | 4-hadoop-eco p18, 4-hadoop-eco p7, 4-hadoop-eco p19 |
| hadoop-fact-07 | factual | Which cluster managers can Spark run on? | 4-hadoop-eco p41 | 4-hadoop-eco p41, intro.pdf p64, intro.pdf p81 | intro.pdf p116, 3-failure-an p21, intro.pdf p116 |
| hadoop-conc-01 | conceptual | What happens when a DataNode disappears from the cluster? | 4-hadoop-eco p31 | 4-hadoop-eco p31, 3-failure-an p27, 4-hadoop-eco p28 | 4-hadoop-eco p36, 4-hadoop-eco p29, 3-failure-an p41 |
| hadoop-conc-05 | conceptual | How does HDFS place block replicas across racks? | 4-hadoop-eco p32, intro.pdf p42 | intro.pdf p42, 3-failure-an p61, 3-failure-an p60 | 3-failure-an p61, 4-hadoop-eco p34, intro.pdf p19 |
| hadoop-conc-08 | conceptual | How does a Yarn application get its containers launched? | 4-hadoop-eco p42, 4-hadoop-eco p44, intro.pdf p54 | 4-hadoop-eco p54, 4-hadoop-eco p44, 4-hadoop-eco p53 | 4-hadoop-eco p69, intro.pdf p97, 4-hadoop-eco p58 |
| hadoop-lex-07 | lexical | What does RF = 3 mean in HDFS? | 4-hadoop-eco p31, 4-hadoop-eco p30, intro.pdf p38 | 4-hadoop-eco p31, 4-hadoop-eco p29, 4-hadoop-eco p26 | 3-failure-an p2, intro.pdf p10, 4-hadoop-eco p27 |
| nosql-fact-03 | factual | What are the main features of standard OLTP databases? | 1.1-comparis p2 | 1-Introducti p9, 1.1-comparis p2, 1.1-comparis p1 | 1.1-comparis p1, 1.1-comparis p22, 1.1-comparis p12 |
| nosql-conc-08 | conceptual | Why are B-Trees not used in Big Data storage? | 1.1-comparis p30, 1.1-comparis p31 | 1.1-comparis p30, 1.1-comparis p31, 1.1-comparis p32 | intro.pdf p1, intro.pdf p66, intro.pdf p83 |
| nosql-para-05 | paraphrased | Can a program see a file while another program is still writing it in HDFS? | 1.1-comparis p15, 1.1-comparis p17 | 1-Introducti p51, intro.pdf p33, 1.1-comparis p15 | intro.pdf p43, 4-hadoop-eco p34, 3-failure-an p6 |
| nosql-para-07 | paraphrased | How do traditional databases make sure committed changes survive a crash? | 1.1-comparis p2, 1.1-comparis p12 | 1.1-comparis p12, intro.pdf p38, TD2-part1-sp p24 | 1-Introducti p9, 3-failure-an p13, 1.1-comparis p11 |
| nosql-para-08 | paraphrased | Why is looking up a row by its key fast in a relational database? | 1.1-comparis p29, 1.1-comparis p31 | 1.1-comparis p31, intro.pdf p88, 1-Introducti p63 | intro.pdf p88, 4-hadoop-eco p17, 3-failure-an p48 |
| nosql-para-10 | paraphrased | Why do frequent row updates make an Iceberg table slow? | 1.1-comparis p28 | 1.1-comparis p28, 1.1-comparis p26, 1-Introducti p44 | 1.1-comparis p25, 1-Introducti p44, 1-Introducti p45 |
| spark-conc-01 | conceptual | What is the difference between narrow and wide transformations? | 1-Introducti p58, 1-Introducti p73 | 1-Introducti p73, 1-Introducti p58, 1-Introducti p60 | 1-Introducti p57, 1-Introducti p39, 1-Introducti p46 |
| spark-para-03 | paraphrased | How do I remove some rows from a dataset? | 1-Introducti p45 | 1-Introducti p63, 1-Introducti p66, 1-Introducti p45 | TD1-spark-sh p60, 3-failure-an p27, TD1-spark-sh p57 |
| spark-para-07 | paraphrased | Why are files starting with an underscore ignored when loading a folder? | 1-Introducti p51 | 1.1-comparis p7, 1-Introducti p51, intro.pdf p91 | TD2-part1-sp p33, 1.1-comparis p7, intro.pdf p95 |
| td-02 | conceptual | Why does reading only one column of a Parquet dataset read fewer bytes than the same query on a CSV dataset? | 1.1-comparis p30, 1.1-comparis p33, 1-Introducti p9 | TD2-part2-sp p3, TD2-part2-sp p10, 1-Introducti p9 | TD2-part2-sp p10, 1-Introducti p66, 1.1-comparis p10 |
| td-12 | conceptual | Why does a Spark job become very slow when the data does not fit in memory? | 1-Introducti p25, intro.pdf p114, TD2-part1-sp p7 | 1-Introducti p22, TD1-spark-sh p85, TD2-part1-sp p7 | intro.pdf p10, 3-failure-an p15, 3-failure-an p51 |

## 5. Missed by both

| id | Type | Question | Expected pages | Dense retrieved | BM25 retrieved |
|---|---|---|---|---|---|
| hadoop-fact-05 | factual | Which operations does the HDFS API allow on files? | 4-hadoop-eco p23 | intro.pdf p59, intro.pdf p49, 4-hadoop-eco p29 | 4-hadoop-eco p27, 1-Introducti p2, 1-Introducti p72 |
| hadoop-conc-03 | conceptual | How does a ZooKeeper write get committed across the cluster? | 4-hadoop-eco p16 | 3-failure-an p47, 4-hadoop-eco p17, 3-failure-an p49 | 1.1-comparis p11, TD2-part2-sp p6, 1.1-comparis p10 |
| hadoop-para-01 | paraphrased | How can servers discover each other and know which ones are still alive? | 4-hadoop-eco p12, 4-hadoop-eco p13, 3-failure-an p48, 3-failure-an p49 | intro.pdf p39, 3-failure-an p38, 3-failure-an p35 | intro.pdf p5, intro.pdf p67, 1-Introducti p40 |
| hadoop-para-04 | paraphrased | When a storage machine joins the cluster again, what does it tell the master? | 4-hadoop-eco p31 | 3-failure-an p41, intro.pdf p39, 4-hadoop-eco p41 | 3-failure-an p51, 4-hadoop-eco p44, 3-failure-an p41 |
| hadoop-para-08 | paraphrased | How can I schedule a job to run automatically every weekday on Hadoop? | 4-hadoop-eco p61, 4-hadoop-eco p63 | intro.pdf p52, 3-failure-an p21, 4-hadoop-eco p49 | 3-failure-an p21, intro.pdf p52, 4-hadoop-eco p79 |
| hadoop-para-09 | paraphrased | How can I start a Spark job with a simple HTTP request? | 4-hadoop-eco p74, 4-hadoop-eco p75 | 4-hadoop-eco p53, TD2-part1-sp p5, TD1-spark-sh p4 | 4-hadoop-eco p71, 4-hadoop-eco p72, intro.pdf p50 |
| nosql-para-01 | paraphrased | If a database transaction fails halfway, what happens to the changes that were already made? | 1.1-comparis p5 | 1.1-comparis p12, intro.pdf p35, intro.pdf p39 | 3-failure-an p4, intro.pdf p73, 3-failure-an p22 |
| nosql-para-09 | paraphrased | How can I query an older version of a table in a data lake? | 1.1-comparis p27, 1-Introducti p44 | intro.pdf p113, intro.pdf p111, intro.pdf p65 | intro.pdf p65, intro.pdf p110, 3-failure-an p35 |
| spark-conc-03 | conceptual | How does Spark handle partitions that do not fit in an executor's RAM? | 1-Introducti p25 | 1-Introducti p36, TD1-spark-sh p85, TD2-part1-sp p7 | intro.pdf p10, 1-Introducti p24, 1-Introducti p33 |
| spark-conc-05 | conceptual | How does Spark sort a distributed dataset internally? | 1-Introducti p80 | 1-Introducti p36, 1-Introducti p47, TD1-spark-sh p85 | TD1-spark-sh p85, 1.1-comparis p10, TD1-spark-sh p84 |
| spark-para-01 | paraphrased | How can I process data that is far too big for the memory of one machine? | 1-Introducti p12, 1-Introducti p16 | intro.pdf p114, 1-Introducti p3, intro.pdf p115 | 1-Introducti p28, 2-brief-hist p2, 1-Introducti p3 |
| spark-para-02 | paraphrased | How do I change a value in a row if datasets cannot be modified? | 1-Introducti p44 | 1-Introducti p63, 1.1-comparis p13, TD1-spark-sh p88 | 4-hadoop-eco p16, 1.1-comparis p12, TD1-spark-sh p75 |
| spark-para-06 | paraphrased | Why do I get lots of tiny output files when I save my results? | 1-Introducti p52 | 1.1-comparis p10, intro.pdf p114, intro.pdf p91 | 1-Introducti p21, 1-Introducti p22, TD2-part1-sp p2 |
| spark-para-08 | paraphrased | Why should I not bring a whole big dataset back to the main program? | 1-Introducti p47 | intro.pdf p92, 1.1-comparis p30, 1-Introducti p94 | 4-hadoop-eco p1, 1-Introducti p91, intro.pdf p1 |
| spark-para-09 | paraphrased | How can machines be added or removed while a job is running? | 1-Introducti p35, 1-Introducti p37 | intro.pdf p50, 4-hadoop-eco p77, intro.pdf p50 | intro.pdf p50, intro.pdf p84, 4-hadoop-eco p57 |
| spark-para-10 | paraphrased | How does Spark decide which machine reads which input file? | 1-Introducti p49 | TD2-part1-sp p36, 1-Introducti p22, TD2-part1-sp p26 | 1-Introducti p47, 1.1-comparis p16, TD2-part2-sp p10 |
| td-08 | factual | What are the different ways to filter the rows of a Spark Dataset? | 1-Introducti p65, 1-Introducti p66, 1-Introducti p67, TD1-spark-sh p67, TD1-spark-sh p90 | 1-Introducti p50, TD1-spark-sh p95, TD2-part1-sp p26 | TD1-spark-sh p88, TD1-spark-sh p66, TD1-spark-sh p69 |

## 6. Wins / losses (Hybrid vs Dense)

| | Questions |
|---|---:|
| Wins (missed by Dense, found by Hybrid) | 9 |
| Losses (found by Dense, missed by Hybrid) | 7 |
| Unchanged | 108 |

### Wins

| id | Type | Question | Expected pages | Dense retrieved | Hybrid retrieved |
|---|---|---|---|---|---|
| hadoop-conc-06 | conceptual | What is the main difference between Yarn and Kubernetes? | 4-hadoop-eco p46 | intro.pdf p56, 4-hadoop-eco p37, 4-hadoop-eco p40 | 4-hadoop-eco p40, 4-hadoop-eco p46, 4-hadoop-eco p37 |
| hadoop-para-01 | paraphrased | How can servers discover each other and know which ones are still alive? | 4-hadoop-eco p12, 4-hadoop-eco p13, 3-failure-an p48, 3-failure-an p49 | intro.pdf p39, 3-failure-an p38, 3-failure-an p35 | intro.pdf p39, 3-failure-an p46, 4-hadoop-eco p13 |
| hadoop-para-05 | paraphrased | How does the cluster keep data safe if a whole server rack goes down? | 4-hadoop-eco p32, intro.pdf p42 | 3-failure-an p27, intro.pdf p39, 4-hadoop-eco p31 | intro.pdf p39, 4-hadoop-eco p31, intro.pdf p42 |
| nosql-para-02 | paraphrased | Why can't Hadoop update a single record in place inside a file? | 1.1-comparis p13, 1.1-comparis p22, 4-hadoop-eco p23, TD2-part1-sp p25 | intro.pdf p91, 4-hadoop-eco p27, intro.pdf p42 | TD2-part1-sp p25, 1.1-comparis p12, intro.pdf p91 |
| nosql-lex-02 | lexical | What is a .crc file used for? | 1.1-comparis p7 | 1-Introducti p42, TD2-part1-sp p27, 1-Introducti p43 | 1.1-comparis p7, 1-Introducti p51, 1-Introducti p42 |
| spark-fact-03 | factual | What is a task in Spark? | 1-Introducti p27 | TD1-spark-sh p30, TD1-spark-sh p44, TD1-spark-sh p93 | TD1-spark-sh p44, TD1-spark-sh p30, 1-Introducti p27 |
| spark-conc-03 | conceptual | How does Spark handle partitions that do not fit in an executor's RAM? | 1-Introducti p25 | 1-Introducti p36, TD1-spark-sh p85, TD2-part1-sp p7 | 1-Introducti p25, 1-Introducti p36, intro.pdf p10 |
| spark-para-02 | paraphrased | How do I change a value in a row if datasets cannot be modified? | 1-Introducti p44 | 1-Introducti p63, 1.1-comparis p13, TD1-spark-sh p88 | 1-Introducti p44, 1.1-comparis p12, 1-Introducti p63 |
| spark-lex-10 | lexical | What are DeltaLake and Iceberg used for in Spark? | 1-Introducti p44, 1-Introducti p45 | intro.pdf p65, TD2-part1-sp p25, 1.1-comparis p26 | 1-Introducti p45, 1.1-comparis p26, 1.1-comparis p25 |

### Losses

| id | Type | Question | Expected pages | Dense retrieved | Hybrid retrieved |
|---|---|---|---|---|---|
| hadoop-fact-07 | factual | Which cluster managers can Spark run on? | 4-hadoop-eco p41 | 4-hadoop-eco p41, intro.pdf p64, intro.pdf p81 | intro.pdf p116, intro.pdf p64, intro.pdf p81 |
| hadoop-conc-05 | conceptual | How does HDFS place block replicas across racks? | 4-hadoop-eco p32, intro.pdf p42 | intro.pdf p42, 3-failure-an p61, 3-failure-an p60 | 3-failure-an p61, 3-failure-an p60, 4-hadoop-eco p31 |
| hadoop-conc-07 | conceptual | Why is MapReduce no longer used? | 4-hadoop-eco p37 | 2-brief-hist p17, intro.pdf p69, 4-hadoop-eco p37 | intro.pdf p69, 2-brief-hist p17, 4-hadoop-eco p35 |
| nosql-para-05 | paraphrased | Can a program see a file while another program is still writing it in HDFS? | 1.1-comparis p15, 1.1-comparis p17 | 1-Introducti p51, intro.pdf p33, 1.1-comparis p15 | intro.pdf p43, 1-Introducti p51, intro.pdf p33 |
| spark-conc-01 | conceptual | What is the difference between narrow and wide transformations? | 1-Introducti p58, 1-Introducti p73 | 1-Introducti p73, 1-Introducti p58, 1-Introducti p60 | 1-Introducti p57, 1-Introducti p60, 1-Introducti p74 |
| spark-para-03 | paraphrased | How do I remove some rows from a dataset? | 1-Introducti p45 | 1-Introducti p63, 1-Introducti p66, 1-Introducti p45 | TD1-spark-sh p80, TD1-spark-sh p66, 1-Introducti p63 |
| td-02 | conceptual | Why does reading only one column of a Parquet dataset read fewer bytes than the same query on a CSV dataset? | 1.1-comparis p30, 1.1-comparis p33, 1-Introducti p9 | TD2-part2-sp p3, TD2-part2-sp p10, 1-Introducti p9 | TD2-part2-sp p10, TD2-part2-sp p3, TD2-part2-sp p10 |
