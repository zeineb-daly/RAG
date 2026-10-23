# Generation test — k=3 vs k=5

- LLM: qwen2.5:7b, retriever: Dense (nomic-embed-text + prefix), same prompt as the app
- 15 in-scope questions (3 per type, random seed 0) + 2 out-of-scope

| | k=3 | k=5 |
|---|---:|---:|
| Relevant page in context | 13 / 15 | 14 / 15 |
| False refusals (in-scope answered with refusal) | 2 / 15 | 1 / 15 |
| Correct refusals (out-of-scope) | 2 / 2 | 2 / 2 |
| Average latency (s) | 44.9 | 40.9 |

## Answers side by side

### nosql-fact-05 (factual) — What time travel features does Iceberg offer?

**k=3** (page in context: yes, refusal: no, 40s)

Iceberg offers time travel features similar to those found in Oracle and Git. Specifically, you can use the `SELECT AS OF ...` command, which is the same as in Oracle, to query data as it was at a specific point in time. This feature helps in solving the problems of concurrent read/write issues, much like how Git handles version control.

Explanation:
Time travel in Iceberg allows you to view data as it existed at a particular moment in the past. This is useful for analyzing historical data or ensuring data consistency during concurrent operations. For example, if you need to see how your data looked on a specific date, you can use the `SELECT AS OF ...` command to retrieve that version of the data. This is similar to how you might use version control in Git to check out previous states of a file.

**k=5** (page in context: yes, refusal: no, 38s)

Iceberg offers time travel features similar to those in Oracle and Git. Specifically, you can use queries like `SELECT AS OF ...` to read data as it was at a specific point in time, just like in Oracle. Similarly, Iceberg supports branching and merging, akin to Git.

Explanation:
Time travel in Iceberg allows you to query data as it existed at a particular point in time. This is useful for analyzing historical data or ensuring data consistency during concurrent operations. For example, if you want to see how your data looked on a specific date, you can use a query like `SELECT AS OF '2023-01-01'` to retrieve that version of the data. This feature is powerful for auditing, compliance, and data analysis tasks.


### nosql-fact-06 (factual) — Which Parquet optimizations are mentioned in the course?

**k=3** (page in context: yes, refusal: no, 29s)

The course mentions the following Parquet optimizations:
1/ Partition Pruning
2/ Column Pruning
3/ Predicate Push Down
4/ Using Statistics
5/ Using Bloom Filters

These optimizations are aimed at improving the efficiency of data processing and storage in Parquet files. For example, Column Pruning allows the system to read only the necessary columns, reducing the amount of data processed and improving performance.

**k=5** (page in context: yes, refusal: no, 24s)

The course mentions the following Parquet optimizations:
1/ Partition Pruning
2/ Column Pruning
3/ Predicate Push Down
4/ Using Statistics
5/ Using Bloom Filters

These optimizations are designed to improve the efficiency of data processing and storage in Parquet files. For example, Column Pruning allows the system to read only the necessary columns, reducing the amount of data processed and improving performance.


### hadoop-fact-02 (factual) — What is the default replication factor in HDFS?

**k=3** (page in context: yes, refusal: no, 30s)

The default replication factor in HDFS is 3.

Explanation:
In the context provided from "4-hadoop-ecosystem.pdf," it explicitly states that the default replication factor (RF) in HDFS is set to 3. This means that each file block in HDFS is replicated three times by default to ensure data availability and fault tolerance.

**k=5** (page in context: yes, refusal: no, 31s)

The default replication factor in HDFS is 3.

Explanation:
In HDFS, the default replication factor is set to 3. This means that each block of data is replicated three times across the cluster. This setup helps ensure data reliability and availability, as even if some DataNodes fail, the data can still be accessed from other replicas.

Example:
If you write a file in HDFS, it will be split into blocks, and each block will have three copies stored across different DataNodes to ensure redundancy.


### nosql-conc-01 (conceptual) — Why is the commit with temporary directories not really atomic?

**k=3** (page in context: yes, refusal: no, 74s)

The commit with temporary directories is not really atomic because the process of renaming files and deleting old ones can take a long time, leading to potential timeouts or failures. During this process, some files might still be in a temporary state, making the commit appear partially completed.

Explanation:
The commit process in NoSQL databases, especially when dealing with large-scale operations like Spark jobs, involves moving files from a temporary directory to the final directory. This operation is not atomic because it consists of multiple steps: first, deleting old files, and then renaming new files. Each step can take considerable time, and if the process is interrupted, it can leave the system in an inconsistent state with some files partially committed. This is why the commit might fail or timeout, and you might end up with a mix of old and new files, not all of which are fully committed.

**k=5** (page in context: yes, refusal: no, 52s)

The commit with temporary directories is not really atomic because the process of renaming files and deleting old ones can take a long time, leading to potential timeouts or failures. This means that during the commit, some files might still be in a temporary state, making the commit appear partially completed.

Explanation:
When performing a commit, the system tries to rename new files and delete old ones to finalize the changes. However, this process can be lengthy, especially with large numbers of files. During this time, the system might experience timeouts or failures, causing the commit to appear incomplete. Some temporary files might remain, and old files might not be fully deleted, leading to a situation where the commit is not fully atomic. This can result in partially committed data being visible, which is not ideal for ensuring data integrity and consistency.


### spark-conc-01 (conceptual) — What is the difference between narrow and wide transformations?

**k=3** (page in context: yes, refusal: no, 50s)

Narrow Transformations are locally independent and can be parallelized. Each partition of the dataset can be transformed independently without affecting others. There is no network data movement between partitions. For example, if you apply a transformation to each partition of a dataset, the transformation can be done in parallel without needing to shuffle data across partitions.

Wide Transformations, on the other hand, are inter-dependent, meaning the output of one partition depends on the output of another. This can lead to a shuffle operation where data is redistributed across partitions, potentially changing the partition topology. This often results in network data movements between partitions.

These differences are explained in the Spark documentation and the lecture slides on page 58 and 73 of the document "1-Introduction-Spark-Distributed-Dataset-Operations.pdf".

**k=5** (page in context: yes, refusal: no, 40s)

Narrow Transformations are locally independent and do not necessarily involve "row by row" processing but operate partition by partition. They do not cause network data movements between partitions. For example, if you have a dataset partitioned across multiple nodes, a narrow transformation will process each partition independently without needing to shuffle data between partitions.

Wide Transformations, on the other hand, are inter-dependent and may not preserve the partition topology. This means that the output partitions can depend on multiple input partitions, leading to network data movements between partitions. For instance, when you perform a wide transformation, data might need to be shuffled across different nodes to ensure the transformation can be applied correctly.

These differences are explained in more detail on pages 58 and 73 of the document "1-Introduction-Spark-Distributed-Dataset-Operations.pdf".


### nosql-conc-08 (conceptual) — Why are B-Trees not used in Big Data storage?

**k=3** (page in context: yes, refusal: no, 42s)

B-Trees are not used in Big Data storage because they lose their efficiency if not cached in memory, and accessing them page by page is not ideal. Additionally, keeping a petabyte of data in RAM is generally not a good idea in Big Data scenarios.

Explanation:
B-Trees are efficient when most of their data is cached in memory, but in Big Data environments, where data volumes can be extremely large (like petabytes), keeping such a large amount of data in RAM is impractical and inefficient. B-Trees rely on accessing data page by page, which can be slow for large datasets. Instead, Big Data systems often use file formats like PARQUET, which are splittable and columnar, allowing for more efficient processing and querying of large datasets.

**k=5** (page in context: yes, refusal: no, 53s)

B-Trees are not generally used in Big Data storage because they lose their efficiency if not cached in memory, and accessing them page by page is not ideal. Instead, Big Data systems often use files like PARQUET, which are splittable and columnar, making them more efficient for reading and processing large datasets.

Explanation:
B-Trees are efficient when they are mostly cached in memory, but in Big Data environments, keeping petabytes of data in RAM is not a good idea. Big Data systems like Hadoop use distributed file systems such as HDFS, which are designed to handle large volumes of data across multiple commodity hardware nodes. These systems rely on file formats like PARQUET, which are optimized for reading and processing data in a distributed manner. B-Trees, on the other hand, are not well-suited for this because they require frequent disk access and are not easily split for parallel processing.


### spark-para-02 (paraphrased) — How do I change a value in a row if datasets cannot be modified?

**k=3** (page in context: no, refusal: yes, 40s)

I could not find this information in your course materials.

The context provided discusses the immutability of datasets in Spark, meaning you cannot directly modify a dataset. However, it does not provide specific methods for changing values in a row. Typically, to change a value in a row, you would need to create a new dataset by applying transformations such as `.map()` or `.withColumn()`. For example, if you want to change a value in a column, you can use the `.withColumn()` method to create a new column with the updated values and then drop the old column.

**k=5** (page in context: yes, refusal: no, 60s)

You cannot directly modify a row in a dataset because datasets are immutable. To change a value, you need to create a new dataset. For example, if you want to update a value in a row, you can use the `.map()` function to create a new dataset with the updated values.

Explanation:
Datasets in Spark are designed to be immutable, which means you cannot change their content directly. If you need to update a value in a row, you have to create a new dataset that reflects the changes. The `.map()` function is a powerful tool for transforming datasets. It allows you to apply a function to each row, effectively creating a new dataset with the updated values.

Example:
Suppose you have a dataset with user information and you want to update the age of a specific user. You would use the `.map()` function to create a new dataset where the age of that user is updated.

```scala
val updatedDs = ds.map(row => {
  if (row.getString(0) == "user1") {
    row.copy(age = 30)
  } else {
    row
  }
})
```

In this example, `updatedDs` is a new dataset with the age of "user1" updated to 30.


### nosql-para-10 (paraphrased) — Why do frequent row updates make an Iceberg table slow?

**k=3** (page in context: yes, refusal: no, 52s)

Frequent row updates in an Iceberg table can make it slow because when you update a row, Iceberg needs to handle the update in a way that maintains consistency and isolation. According to the context, Iceberg has to either fully duplicate the file containing the row being updated or add a new file with the updated row and mark the old file for deletion. This process can lead to an explosion in the number of files and an increase in the number of compute treatments required for reads, making the table slower.

Explanation:
When you update a row in an Iceberg table, the system must ensure that the data remains consistent and that reads do not interfere with writes. To achieve this, Iceberg uses a strategy where it either duplicates the entire file containing the row or creates a new file with the updated row and marks the old file for deletion. This approach helps maintain read consistency but can lead to a large number of files, which increases the overhead for read operations. As a result, frequent updates can slow down the performance of the table.

**k=5** (page in context: yes, refusal: no, 52s)

Frequent row updates in an Iceberg table can make it slow because when updating a row, Iceberg needs to either fully duplicate the file or add a new file containing only the updated row and mark the old row for deletion. This leads to an explosion in the number of files and increases the computational load for read operations.

Explanation:
When you frequently update rows in an Iceberg table, the system has to handle these updates in a way that maintains data consistency and isolation. Unlike traditional databases where a single update operation can be performed directly on the row, Iceberg uses a strategy similar to Git commits, where each update is recorded as a new file or a change in the existing file. This approach ensures that reads can still see a consistent snapshot of the data, but it comes at the cost of increased file management and computational overhead. For example, if you update a row many times, Iceberg will keep adding new files or modifying existing ones, which can lead to a large number of files and more complex read operations to manage these changes efficiently.


### spark-para-07 (paraphrased) — Why are files starting with an underscore ignored when loading a folder?

**k=3** (page in context: yes, refusal: no, 39s)

Files starting with an underscore are ignored when loading a folder because they are considered hidden files and are typically used for internal purposes, such as marking the success of a task or checking data integrity.

Explanation:
In distributed computing environments like Hadoop and Spark, hidden files and directories are often used for internal operations. For instance, files like `_SUCCESS` and `.file1.csv.crc` are used to indicate the success of a task or to check the integrity of data files. When loading a directory, these files are not relevant to the main data processing tasks, so they are filtered out to avoid unnecessary processing and potential errors. This practice helps in maintaining the efficiency and reliability of the data processing operations.

**k=5** (page in context: yes, refusal: no, 43s)

Files starting with an underscore are ignored when loading a folder because Spark considers them as hidden files and excludes them from processing. This is to ensure that only relevant and non-hidden files are read and processed.

Explanation:
In distributed computing environments like Spark, it's common to have temporary or marker files that are not meant to be processed directly. These files often start with an underscore (e.g., `_SUCCESS`, `_temporary`). By default, Spark filters out such files to avoid unnecessary processing and potential errors. For example, when you use `sparkSession.read().load("hdfs://path/dir")`, Spark will automatically exclude files like `_SUCCESS` and `.part-*.crc` to focus on the actual data files.


### nosql-lex-02 (lexical) — What is a .crc file used for?

**k=3** (page in context: no, refusal: yes, 30s)

I could not find this information in your course materials.

The provided context focuses on how to create and read datasets in Apache Spark using different APIs and does not mention .crc files. These files are typically used for checksums to ensure data integrity, but this specific information is not covered in the given course materials.

**k=5** (page in context: no, refusal: yes, 13s)

I could not find this information in your course materials.


### nosql-lex-09 (lexical) — What is MVCC used for in OLTP databases?

**k=3** (page in context: yes, refusal: no, 45s)

MVCC is used for read isolation in OLTP databases, ensuring that readers do not see uncommitted data and maintaining consistency.

Explanation:
MVCC (Multi-Version Concurrency Control) helps in managing concurrent transactions in OLTP databases by maintaining multiple versions of data. This allows readers to see a consistent snapshot of the database at a particular point in time, even when writers are modifying data. For example, if a transaction is reading data, it can see the version of the data that was committed before the transaction started, without being affected by uncommitted changes made by other transactions. This ensures that the read operation is not blocked by write operations and maintains data consistency.

**k=5** (page in context: yes, refusal: no, 63s)

MVCC is used for read isolation in OLTP databases, ensuring that readers do not see uncommitted data and maintaining consistency.

Explanation:
MVCC (Multi-Version Concurrency Control) helps in managing concurrent transactions in OLTP databases by maintaining multiple versions of data. This allows readers to see a consistent snapshot of the database at a particular point in time, even when writers are modifying data. It ensures that transactions can read data without blocking other transactions that are writing to the same data, thus improving concurrency and performance.

Example:
Imagine two transactions, T1 and T2, running concurrently. T1 reads a piece of data, and before T1 commits, T2 modifies that same piece of data. With MVCC, T1 will still see the original version of the data it read, while T2 sees the updated version. This prevents T1 from seeing the uncommitted changes made by T2, maintaining data consistency.


### spark-lex-09 (lexical) — What does the 2^32 - 1 limit refer to?

**k=3** (page in context: yes, refusal: no, 52s)

The 2^32 - 1 limit refers to the maximum number of elements in an array indexed by "int" (32 bits) in the Java Virtual Machine (Java VM). This limit is approximately 2 billion elements.

Explanation:
In the context provided, it is mentioned that arrays in the Java VM are indexed by "int" (32 bits), which means they can hold up to 2^32 - 1 elements. This is because an "int" in Java is a 32-bit signed integer, and the maximum value it can hold is 2^32 - 1. This limit is a fundamental restriction imposed by the 32-bit integer type used for indexing arrays in the Java VM.

**k=5** (page in context: yes, refusal: no, 44s)

The 2^32 - 1 limit refers to the maximum number of elements in an array indexed by "int" (32 bits) in the Java Virtual Machine (Java VM) restrictions. This limit means that the number of elements, N, can be less than 2^32 - 1, which is approximately 2 billion.

Explanation:
In the context provided, it is mentioned that arrays in the Java VM are indexed by "int" (32 bits), which means they can hold up to 2^32 - 1 elements. This is a fundamental limitation due to the size of the integer type used for indexing. For example, if you were to create an array in Java to store data, you would not be able to have more than 2 billion elements in that array without encountering an overflow error or exceeding the maximum limit.


### td-04 (conceptual) — Why does Spark first write its output files into a _temporary directory?

**k=3** (page in context: yes, refusal: no, 79s)

To Remember
Spark first writes its output files into a _temporary directory to ensure atomicity. This means that all new files are written in a temporary subdirectory before any old files are deleted. Only after all new files are successfully written does Spark move them to the final directory.

Explanation:
When writing data in Spark, it's crucial to maintain data integrity and avoid partial writes that could lead to inconsistent states. By writing to a temporary directory first, Spark ensures that all new files are complete before they are moved to the final directory. This process helps prevent data loss or corruption, as any issues during the write operation can be handled without affecting the existing data. Once the write operation is successful, the old files are deleted, and the new files are moved to the intended location.

Example:
For instance, when writing a large dataset, Spark might create a temporary directory named `_temporary` and write 26 JSON files there. After all these files are successfully written, Spark will rename or move these files to the final directory, ensuring that the entire operation is atomic and consistent.

**k=5** (page in context: yes, refusal: no, 61s)

To Remember
Spark first writes its output files into a _temporary directory to ensure atomicity. This means that all new files are written in a temporary subdirectory before the old files are deleted and the new ones are moved to the final location.

Explanation:
When Spark writes data, it needs to ensure that the write operation is atomic, meaning it should either complete fully or not at all. Writing directly to the final directory could lead to partial writes, which would leave the data in an inconsistent state. By writing to a temporary subdirectory first, Spark can complete the write operation without interruption. Once the write is complete, Spark can then delete the old files and move the new ones to the final location, ensuring that the data is consistent and complete.

Example:
For instance, if you are writing a large dataset, Spark might first write the files to a directory named `_temporary`. After all the files are written, it will delete the old files in the main directory and rename the `_temporary` directory to the main directory name. This way, the write operation is guaranteed to be atomic, and the data will always be in a consistent state.


### td-09 (factual) — Is there an UPDATE statement to modify rows in Spark?

**k=3** (page in context: yes, refusal: no, 38s)

There is no SQL "UPDATE" built-in in Spark. As per the context from page 25 of TD2-part1-spark-read-write.pdf, you cannot update a specific file or row in a file; instead, you delete the whole directory and replace it with new files.

To understand this better, imagine you have a directory of files representing a dataset. If you need to update a specific row, you would need to delete the entire directory and write the updated data back to it. This approach ensures that all data is consistent and avoids partial updates, which can be problematic in distributed systems like Spark.

**k=5** (page in context: yes, refusal: no, 37s)

No, there is no built-in SQL "UPDATE" statement in Spark.

Explanation: According to the context from page 25 of TD2-part1-spark-read-write.pdf, Spark does not support updating specific rows or files directly. Instead, if you need to modify data, you would typically delete the entire directory containing the data and replace it with the updated data. This approach ensures that all files are managed uniformly, which is necessary for Spark's distributed computing model.


### td-03 (factual) — Why are the files written by Spark named part-000xx with a UUID?

**k=3** (page in context: yes, refusal: no, 73s)

The files are named with "part-000xx" and a UUID because Spark generates random UUID filenames and an index for each partition when writing data in a distributed way. This ensures that each partition's data is written to a unique file, making the process scalable and fault-tolerant.

Explanation:
When Spark writes data, it divides the data into partitions. Each partition gets a unique filename that includes an index (part-000xx) to identify which partition it belongs to, along with a UUID to ensure the filename is unique across different runs or executions. This naming convention helps in managing and identifying the files generated by Spark, especially when dealing with large datasets that are split into multiple partitions.

Example:
If you have a dataset split into 10 partitions, Spark might generate filenames like `part-00001-5f3e4b5c-6d7e-11ec-90d8-0242ac120002.json`, `part-00002-6f3e4b5c-6d7e-11ec-90d8-0242ac120002.json`, and so on, where the UUID part ensures that even if the same partition name is used in different runs, the files can still be uniquely identified.

**k=5** (page in context: yes, refusal: no, 38s)

The files written by Spark are named part-000xx with a UUID because Spark generates random UUID filenames and "part-000xx" index for each partition to write in a distributed way. This approach ensures that files are uniquely named and helps manage data across multiple partitions efficiently.

For example, when writing JSON or Parquet files, Spark uses filenames like `part-00001-<UUID>-c000.snappy.parquet` or `part-00001-<UUID>-c000.json` to uniquely identify each partition's data. This naming convention is used to avoid conflicts and to facilitate the handling of large datasets distributed across multiple partitions.


### oos-05 (out_of_scope) — What is GraphQL and how is it different from REST?

**k=3** (page in context: no, refusal: yes, 25s)

I could not find this information in your course materials.

The context provided does not contain any information about GraphQL or REST. The documents focus on NoSQL databases, HBase, and the Hadoop ecosystem, but do not cover web service architectures like GraphQL and REST.

**k=5** (page in context: no, refusal: yes, 23s)

I could not find this information in your course materials.

The course materials provided focus on comparisons between NoSQL databases and standard OLTP databases, HBase, and the Hadoop ecosystem, particularly YARN. They do not cover GraphQL or REST.


### oos-03 (out_of_scope) — How does Apache Flink handle event time?

**k=3** (page in context: no, refusal: yes, 26s)

I could not find this information in your course materials.

The provided context does not contain any information about how Apache Flink handles event time. The context focuses on batch processing times, cloud migration, and streaming data handling but does not discuss Apache Flink or its event time processing mechanisms.

**k=5** (page in context: no, refusal: yes, 23s)

I could not find this information in your course materials.

The provided context does not contain any information about how Apache Flink handles event time. The context focuses on the performance and implementation changes of a processing system from Hive SQL + UDF xpath to Spark + Java, as well as details about data feeding types and volumetry. It does not mention Apache Flink or its handling of event time.

