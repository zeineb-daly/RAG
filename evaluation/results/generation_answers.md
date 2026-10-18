# Generation Evaluation — Answers side by side

## q01 (factual) — What does ACID stand for?

Retrieved pages: [5, 4, 11] · Expected pages: [4]

### llama3.2:3b  (keywords 75%, refused=False, 19s)

Short answer:
ACID stands for Atomicity, Consistency, Isolation, and Durability.

Explanation:
ACID is a set of properties that ensure database transactions are processed reliably. According to the context, ACID stands for Atomicity, Consistency, Isolation, and Durability. This is stated on page 4 of the document "1.1-comparison-NoSql-DB-vs-standard-DB.pdf".

Example: The context explicitly states that ACID has four components, and it is not Atomic, Consistent, or Isolated in certain cases, as shown on page 11.

### qwen2.5:7b  (keywords 100%, refused=False, 57s)

ACID stands for Atomic, Consistent, Isolated, and Durable.

Explanation:
ACID is a set of properties that guarantee the reliability of database transactions. Atomic means that each transaction is treated as a single, indivisible unit of work. If any part of the transaction fails, the entire transaction is rolled back, ensuring that the database remains in a consistent state. Consistent means that a transaction can only bring the database from one valid state to another. Isolated means that transactions are isolated from each other, so one transaction does not see the uncommitted changes of another. Durable means that once a transaction is committed, it will persist even if a system failure occurs.

For example, if you transfer money from one bank account to another, the transaction should be atomic, ensuring that both the deduction from the first account and the addition to the second account happen together or not at all.

## q02 (factual) — What does Atomic mean in ACID?

Retrieved pages: [5, 4, 11] · Expected pages: [5]

### llama3.2:3b  (keywords 75%, refused=False, 12s)

Short answer:
Atomic means "All or Nothing" in ACID.

Explanation:
In the context of ACID, Atomic refers to the concept that either the entire transaction is committed or it is rolled back completely. This means that if any part of the transaction fails, the entire transaction is not partially committed.

Example: Suppose you're transferring money from one account to another. If the transfer fails due to insufficient funds, the entire transaction should be rolled back, and the money should be returned to the original account. This is an example of Atomicity in action.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 4.

### qwen2.5:7b  (keywords 50%, refused=False, 25s)

Atomic in ACID means that all changes made during a transaction are treated as a single, indivisible unit of work. Either all changes are committed and saved permanently, or if an error occurs, all changes are rolled back, leaving the database in a consistent state.

Explanation:
Atomicity ensures that a transaction is treated as a single, indivisible unit. If any part of the transaction fails, the entire transaction is aborted, and the database remains unchanged. This is crucial for maintaining data integrity. For example, if you are transferring money from one bank account to another, both the deduction from the first account and the addition to the second account must succeed. If only one part succeeds, the transaction is rolled back to maintain consistency.

## q03 (factual) — What are the main features of standard OLTP databases?

Retrieved pages: [2, 1, 12] · Expected pages: [2]

### llama3.2:3b  (keywords 75%, refused=False, 22s)

Short answer:
Standard OLTP databases are based on ACID, use read isolation, and support SQL SELECT, INSERT, UPDATE, and DELETE operations.

Explanation:
Standard OLTP databases, such as traditional relational databases, follow the ACID principles to ensure data consistency and reliability. They use read isolation to provide consistent reads and prevent dirty reads. These databases support standard SQL operations like SELECT, INSERT, UPDATE, and DELETE, and use transactional log files (e.g., WAL files in PostgreSQL) to manage transactions and ensure data integrity.

Example: In standard OLTP databases, when you update a row, the modified block is marked as "dirty" and needs to be saved later to disk. This process involves writing the commit changes to the WAL file and immediately syncing the changes to disk.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 2.

### qwen2.5:7b  (keywords 100%, refused=False, 45s)

Standard OLTP databases have several key features:
- They support ACID properties.
- They use read isolation techniques like read consistency and multiversion concurrency control (MVCC).
- They handle SQL operations such as SELECT, INSERT, UPDATE, and DELETE.
- They use transaction write-ahead logging (WAL) files.
- They modify binary files.
- They employ B-Trees and indexes for fast lookup by rowid or addresses in file blocks.

Explanation:
Standard OLTP databases are designed for transactional processing, ensuring data integrity and consistency. They use advanced techniques like ACID properties and MVCC to manage transactions and concurrent access. For example, when updating a row, the database marks the block as "dirty" and writes the changes to a transaction log file for later disk saving. This ensures that the database can recover from failures and maintain data integrity.

## q04 (factual) — What is the _SUCCESS file used for?

Retrieved pages: [7, 28, 10] · Expected pages: [7]

### llama3.2:3b  (keywords 100%, refused=False, 19s)

The _SUCCESS file is used as an empty marker file for Hadoop to indicate the end of a task.

Here's an explanation: The _SUCCESS file is used to mark the end of a task in Hadoop. It's an empty file that is created when a task is completed successfully. This file is used to indicate that the task has been finished, and it helps Hadoop to keep track of the status of tasks.

For example, in the given context, the _SUCCESS file is mentioned as an example of a hidden file starting with an underscore, specifically « _SUCCESS ». This file is used to indicate the end of a task, and it's an important file in Hadoop's workflow.

### qwen2.5:7b  (keywords 100%, refused=False, 35s)

The _SUCCESS file is used as an empty marker file for Hadoop to indicate the success end of a task.

Explanation:
The _SUCCESS file is a special file that Hadoop creates to signal the completion of a task. In the context of a Hadoop job, when a task is successfully completed, Hadoop writes an empty _SUCCESS file to the output directory. This file serves as a confirmation that the task has finished without errors, allowing the next phase of the job to proceed or indicating to the user that the job has completed successfully.

## q05 (conceptual) — What is the purpose of the _temporary directory when writing data?

Retrieved pages: [6, 8, 15] · Expected pages: [6, 7, 8]

### llama3.2:3b  (keywords 67%, refused=False, 17s)

The _temporary directory is used to store new data temporarily while writing data to the main database.

The purpose of the _temporary directory is to allow for atomic file operations, ensuring that data is written to the main database in a consistent and reliable manner. By using the _temporary directory, the writer can perform operations such as deleting old files and renaming new files in a way that ensures data integrity.

For example, when writing data to the main database, the writer creates a new file in the _temporary directory, performs operations on it, and then renames it to the new file name. This ensures that the data is written to the main database in a single, atomic operation.

### qwen2.5:7b  (keywords 67%, refused=False, 31s)

The purpose of the _temporary directory when writing data is to store new files temporarily before they are renamed and made visible.

Explanation:
When writing data, new files are first stored in the _temporary directory. This allows the system to ensure that all new data is properly processed and then safely moved to the main directory. This process ensures data integrity by first writing to a temporary location and then renaming the files to make them accessible. For example, in the context provided, new files are written to the _temporary directory and then renamed and moved to the main directory after processing.

## q06 (conceptual) — Why is the commit with _temporary directories not really atomic?

Retrieved pages: [9, 11, 8] · Expected pages: [8, 9]

### llama3.2:3b  (keywords 75%, refused=False, 20s)

Short answer:
The commit with _temporary directories is not really atomic because it may not delete all old files and rename all new files.

Explanation:
The context explains that the commit process with _temporary directories is not atomic because it may not complete all steps. In the example, the first 50 steps remove all old files, but the remaining steps (51-250) rename all new files. This means that not all files may be deleted or renamed, resulting in partially committed task results.

Example: Suppose the first 50 steps remove all old files, but the 51st step fails to rename a new file. In this case, the commit is not atomic because the file is not deleted or renamed.

Page: 9

### qwen2.5:7b  (keywords 25%, refused=False, 45s)

The commit with _temporary directories is not really atomic because the process of renaming files and deleting old ones can take a long time, leading to potential timeouts or failures. This means that during the commit, some files might still be in the temporary state, making them partially committed and potentially visible to other processes.

Explanation:
The process of renaming and deleting files in the temporary directory is not instantaneous. It can take a considerable amount of time, especially when dealing with large numbers of files. During this time, the commit process might time out or fail, leaving some files in a temporary state. This can result in a situation where the commit is not fully completed, and some files are partially committed, which can cause issues when other processes try to access the data.

## q07 (conceptual) — Why does a Spark read fail when another process overwrites the same table?

Retrieved pages: [10, 11, 28] · Expected pages: [10]

### llama3.2:3b  (keywords 50%, refused=False, 33s)

Short answer:
Spark read fails when another process overwrites the same table because NoSQL databases like Spark do not follow ACID principles, which include Atomicity, Consistency, Isolation, and Durability.

Explanation:
Spark is designed to be a NoSQL database, which means it does not follow the same rules as traditional relational databases. Specifically, Spark does not follow ACID principles, which are designed to ensure that database transactions are processed reliably and securely.

In the context of Spark, when a process writes to a table, it does not guarantee that the write operation will be atomic, meaning that it will either succeed completely or not at all. This is because Spark is designed to be highly scalable and flexible, which means it can handle multiple writers and readers simultaneously.

When another process overwrites the same table, it can overwrite the data that was written by the previous process. This means that the Spark read operation will fail because it will not be able to retrieve the expected data.

For example, suppose process A writes to a table and commits the transaction. Then, process B overwrites the same table. When process C tries to read the table, it will not be able to retrieve the data that was written by process A because process B has overwritten it.

This is a common problem in NoSQL databases like Spark, and it is known as the "write-overwrite" problem. It is a trade-off between scalability and consistency, and it requires careful consideration when designing and implementing data processing pipelines.

### qwen2.5:7b  (keywords 100%, refused=True, 30s)

I could not find this information in your course materials.

The context provided discusses issues with Spark's handling of data when another process overwrites the same table, but it does not explicitly state why a Spark read fails in such a scenario. The context mentions that Spark fails to return the "new refreshed" result and throws a `FileNotFoundException`, but it does not provide a detailed explanation for this behavior.

## q08 (conceptual) — Why is Spark not isolated when writing to several partitions?

Retrieved pages: [11, 10, 26] · Expected pages: [11]

### llama3.2:3b  (keywords 33%, refused=False, 24s)

Short answer:
Spark is not isolated when writing to several partitions because it tries to be ACID, but it is not Isolated.

Explanation:
Spark's goal is to achieve ACID compliance, which means it aims to be Atomic, Consistent, Isolated, and Durability. However, when writing to multiple partitions, Spark's Isolation property is compromised. This is because Spark is not designed to maintain a single, unified view of the data across all partitions. Instead, it allows multiple writer processes to write to different partitions independently, which can lead to inconsistent results.

For example, suppose two writer processes are writing to different partitions of the same table. If one process commits its changes, the other process may not see those changes immediately, even if it reads the same partition later. This is because Spark does not guarantee Isolation across partitions.

In the context of the provided slides, this issue is illustrated on page 11, where it is mentioned that Spark tries to be ACID but is not Isolated.

### qwen2.5:7b  (keywords 67%, refused=False, 42s)

Spark is not isolated when writing to several partitions because it may see some committed partitions (partially committed task results) but not others, even from different writer processes.

Explanation:
When writing to multiple partitions in Spark, the system might encounter a situation where some partitions are already committed (meaning they have been successfully written to), while others are still in the process of being written. This can lead to inconsistencies because different writer processes might see different states of the data. For example, one process might see some committed partitions, while another might not see them yet, leading to partial results or errors when trying to read the data again. This lack of isolation means that the system does not guarantee a consistent view of the data across different operations or processes.

## q09 (conceptual) — How is a row update written in a standard OLTP database?

Retrieved pages: [12, 2, 28] · Expected pages: [12]

### llama3.2:3b  (keywords 80%, refused=False, 27s)

Short answer:
In a standard OLTP database, a row update is written by modifying the RAM memory, marking the modified block as "Dirty", and then writing the changes to the WAL Transactional Log File and the UNDO File in Oracle.

Explanation:
In a standard OLTP database, when a row update is performed, the modified block is marked as "Dirty" to indicate that it needs to be saved later to disk. The update is then written directly to the RAM memory. After the update is committed, the changes are written to the WAL Transactional Log File and the UNDO File in Oracle. The UNDO File contains a copy of the old row, which is overwritten by the new row.

Example: In Oracle, when a row update is performed, the modified block is marked as "Dirty" and then written to the WAL Transactional Log File and the UNDO File. The UNDO File contains a copy of the old row, which is overwritten by the new row.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 12.

### qwen2.5:7b  (keywords 80%, refused=False, 53s)

A row update in a standard OLTP database is marked as "Dirty" in the Modified Block and will be saved later to disk. The changes are also written directly to the RAM memory and appended to the Transactional Log File (or "REDO File" in Oracle). Additionally, in Oracle, the old row is written to the "UNDO File".

Explanation:
When you update a row in a standard OLTP database, the system marks the row as "Dirty" to indicate that it needs to be saved. This is done to ensure that the changes are not lost. The updated data is also stored in the RAM to make the system faster. To maintain consistency, the changes are also recorded in a log file, which helps in recovery if something goes wrong. In Oracle, the old version of the row is also saved in a separate file called the "UNDO File" to support rollback operations.

## q10 (conceptual) — Why can't we modify a file in the middle in Big Data storage?

Retrieved pages: [13, 30, 12] · Expected pages: [13, 22]

### llama3.2:3b  (keywords 25%, refused=False, 22s)

Short answer:
In Big Data storage, we cannot modify a file in the middle.

Explanation:
In Big Data storage, files are stored in a way that makes it difficult to modify them in the middle. According to the context, files in Big Data storage can only be written to in append mode, meaning new data can be added to the end of the file, but not in the middle. This is because the files are stored in a compressed format and are not suitable for random access.

Example: The context states that "In BigData: No B-Tree files… only PARQUET « Splittable + Columnar » files". This suggests that the file format used in Big Data storage is not conducive to random access or modification in the middle.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 30.

### qwen2.5:7b  (keywords 25%, refused=True, 27s)

I could not find this information in your course materials.

The context provided discusses the limitations of modifying files in Big Data storage, but it does not explicitly state why modifications in the middle of a file are not possible. It mentions that files in Big Data storage can only be written to by appending to them or by deleting and re-creating them from the beginning.

## q11 (factual) — When does a newly written file become visible to readers?

Retrieved pages: [15, 17, 10] · Expected pages: [15, 17]

### llama3.2:3b  (keywords 100%, refused=False, 20s)

A newly written file becomes visible to readers after flush().

Here's an explanation: According to the context, when a file is created, the writer can only write to a temporary "opened-file" and then flush it. After flushing, the file becomes visible to readers. This is because the reader can only see fully written and flushed files, not intermediate write operations that are still in progress. 

For example, if a writer writes to a file and then flushes it, the reader can then read the file and see the new content. However, if the writer writes to the file again before flushing, the reader will not see the new content until the file is flushed.

### qwen2.5:7b  (keywords 100%, refused=False, 31s)

A newly written file becomes visible to readers after it has been fully written and flushed.

Explanation:
For a file to be visible to readers, it must go through two steps: it needs to be fully written and then flushed. Only after these steps are completed can the file be seen by readers. This ensures that readers do not see any intermediate, incomplete data.

Example:
If a file is written and flushed, it will be visible to readers. However, if the file is only written but not flushed, readers will not see it until it is flushed.

## q12 (factual) — What is a memory-mapped file and why do databases use it?

Retrieved pages: [23, 30, 12] · Expected pages: [23]

### llama3.2:3b  (keywords 67%, refused=False, 24s)

Short answer:
A memory-mapped file is a file that is directly visible as virtual memory from the Linux OS, allowing for faster access than sequential reading files.

Explanation:
Databases use memory-mapped files because they provide faster access to data compared to sequential reading files. This is because the operating system can map the file directly into virtual memory, allowing the database to access the data without having to read it from disk. This can improve performance, especially for large datasets.

Example: In the context, it is mentioned that most databases use memory-mapped files, which are "directly visible as virtual Memory from the Linux OS". This illustrates how memory-mapped files can be accessed directly from memory, bypassing the need to read from disk.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 23.

### qwen2.5:7b  (keywords 67%, refused=False, 41s)

A memory-mapped file is a file that is mapped into the address space of a process, allowing the process to read from and write to the file as if it were a memory block. Databases use memory-mapped files to directly access virtual memory from the Linux OS, which is faster than sequential reading of files (reading per block/pages).

Explanation:
Memory-mapped files allow the operating system to manage the file's contents in memory, making it easier for the database to read and write data. This method is faster because it reduces the overhead of traditional file I/O operations, allowing the database to access data more quickly. For example, when a database needs to read a piece of data, it can directly access the corresponding memory location without the need for additional system calls or file operations.

## q13 (conceptual) — How does Iceberg solve the read isolation problem of Hive tables?

Retrieved pages: [26, 28, 11] · Expected pages: [25, 26]

### llama3.2:3b  (keywords 67%, refused=False, 17s)

Short answer:
Iceberg solves the read isolation problem of Hive tables by allowing Read Isolation.

Explanation:
Iceberg allows Read Isolation by providing a way to solve the problems of concurrent read/write operations occurring with Hive (Partitioned) Tables. This is stated in the context on page 26 of the document "1.1-comparison-NoSql-DB-vs-standard-DB.pdf".

In simple terms, Iceberg helps to isolate reads from writes, ensuring that reads are consistent and accurate, even in the presence of concurrent updates. This is achieved by allowing the database to maintain a separate copy of the data, which can be read without affecting the original data.

### qwen2.5:7b  (keywords 67%, refused=False, 35s)

Iceberg solves the read isolation problem of Hive tables by allowing read isolation and consistency. This means that concurrent read/write problems occurring with Hive (partitioned) tables can be managed effectively.

Explanation:
Iceberg ensures that when you read data, you get a consistent snapshot of the data at the time of the read operation. This is particularly useful in environments where multiple processes might be writing to the same table. In Hive, this can be problematic because concurrent writes can lead to inconsistent reads. Iceberg's design allows for a clear separation between reading and writing, ensuring that readers see a consistent view of the data, even if writers are still processing their changes.

## q14 (factual) — What time travel features does Iceberg offer?

Retrieved pages: [27, 26, 28] · Expected pages: [27]

### llama3.2:3b  (keywords 100%, refused=False, 14s)

Short answer:
Iceberg offers time travel features similar to Oracle's "SELECT AS OF ...".

Explanation:
Iceberg provides time travel features that allow for querying data at a specific point in time, similar to Oracle's "SELECT AS OF ...". This feature is also available in Git. 

Example: This feature is mentioned in the context as an example of a time travel feature, but no specific details about how it works are provided.

### qwen2.5:7b  (keywords 100%, refused=False, 37s)

Iceberg offers time travel features similar to those found in Oracle and Git. Specifically, it allows for "SELECT AS OF …" queries, enabling users to read data as it was at a specific point in time, just like in Oracle.

Explanation:
Time travel in Iceberg means you can query data as it existed at a particular moment in the past. This is useful for analyzing historical data or ensuring that you can see the state of the database at different points in time, similar to how you can check the history of files in Git. For example, if you want to see how your data looked on a specific date, you can use the "SELECT AS OF …" command to retrieve that version of the data.

## q15 (conceptual) — What is the difference between Copy on Write and Merge on Read in Iceberg?

Retrieved pages: [28, 26, 25] · Expected pages: [28]

### llama3.2:3b  (keywords 100%, refused=False, 25s)

Short answer:
Copy on Write and Merge on Read are two different strategies used in Iceberg to handle updates.

Explanation:
In Iceberg, these two strategies are used to handle updates to data in a NoSQL database. 

Copy on Write is a strategy where the entire file needs to be duplicated when updating a row. This is done to prevent data corruption and ensure data consistency.

Merge on Read is a strategy where a new file is created containing only the updated row, and the ids of the rows to be deleted are marked. This approach reduces the number of files created and the amount of data that needs to be duplicated.

For example, when updating a row in a file, instead of duplicating the entire file, a new file is created with only the updated row, and the ids of the rows to be deleted are marked. This reduces the number of files created and the amount of data that needs to be duplicated.

This approach is different from the other strategy mentioned, which involves an "explosion of files" and "explosion of compute treatments for read".

### qwen2.5:7b  (keywords 0%, refused=True, 18s)

I could not find this information in your course materials.

The context provided discusses the strategies Iceberg uses for handling updates, mentioning "Copy on Write" and "Merge on Read" but does not directly compare or explain the differences between these two strategies.

## q16 (conceptual) — Why are B-Trees not used in Big Data storage?

Retrieved pages: [30, 31, 32] · Expected pages: [30, 31]

### llama3.2:3b  (keywords 33%, refused=False, 18s)

Short answer:
B-Trees are not used in Big Data storage because they lose their interest if not cached and accessing page blocks is not efficient.

Explanation:
The context states that B-Trees are not used in Big Data storage because they lose their interest if not cached and accessing page blocks is not efficient. This means that B-Trees require frequent caching and page access to maintain their efficiency, which is not feasible in Big Data storage where storing petabytes of files in RAM is generally not a good idea.

Example: The context mentions that even page blocks of B-TREE files are not stored in RAM, highlighting the inefficiency of B-Trees in Big Data storage.

Document: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf
Page: 30

### qwen2.5:7b  (keywords 100%, refused=False, 40s)

B-Trees are not used in Big Data storage because they lose their efficiency if not cached in memory, and accessing them page by page is not ideal. Instead, Big Data systems use files like PARQUET, which are splittable and columnar, making them more efficient for large-scale data processing.

Explanation:
B-Trees are efficient data structures for managing data in memory, but they become less effective when dealing with large datasets that don't fit into memory. In Big Data scenarios, where data volumes can be petabytes, keeping such large files entirely in RAM is not practical. B-Trees rely on being cached in memory to perform efficiently, and accessing them page by page can be slow. Therefore, Big Data systems prefer file formats like PARQUET, which are designed to be read efficiently in chunks and are optimized for columnar storage, making them more suitable for big data processing.

## q17 (factual) — Which Parquet optimizations are mentioned in the course?

Retrieved pages: [33, 30, 32] · Expected pages: [33]

### llama3.2:3b  (keywords 100%, refused=False, 13s)

The Parquet optimizations mentioned in the course are:

1/ Partition Pruning
2/ Column Pruning
3/ Predicate Push Down
4/ Using Statistics
5/ Using Bloom Filters

These optimizations are mentioned in the course on Parquet Optimizations, page 33 of the 1.1-comparison-NoSql-DB-vs-standard-DB.pdf document.

### qwen2.5:7b  (keywords 100%, refused=False, 24s)

The course mentions the following Parquet optimizations:
1. Partition Pruning
2. Column Pruning
3. Predicate Push Down
4. Using Statistics
5. Using Bloom Filters

These optimizations help in efficiently processing Parquet files, which are used in BigData scenarios. For example, Column Pruning allows the system to read only the necessary columns, reducing the amount of data processed.

## p01 (paraphrased) — If a database transaction fails halfway, what happens to the changes that were already made?

Retrieved pages: [12, 28, 13] · Expected pages: [5]

### llama3.2:3b  (keywords 0%, refused=False, 21s)

Short answer:
In a standard OLTP database, the changes made during a transaction are written to the WAL Transactional Log File and the RAM memory, and then committed to disk later.

Explanation:
When a transaction fails halfway, the changes made so far are not written to disk immediately. Instead, they are written to the RAM memory and the WAL Transactional Log File. The WAL Transactional Log File is used to record the changes made during the transaction, and it is later written to disk when the transaction is committed. This allows the database to recover the changes made during the transaction if it fails.

Example: In Oracle, when a transaction fails, the changes made so far are written to the REDO File, which is a part of the WAL Transactional Log File. The changes are then written to disk later, and the database can recover them if the transaction fails.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 12.

### qwen2.5:7b  (keywords 0%, refused=True, 18s)

I could not find this information in your course materials.

The context provided does not contain specific details about what happens to changes if a database transaction fails halfway. The context mainly discusses how changes are handled in standard OLTP databases and NoSQL databases, but it does not address transaction failures directly.

## p02 (paraphrased) — Why can't Hadoop update a single record in place inside a file?

Retrieved pages: [13, 18, 28] · Expected pages: [13, 22]

### llama3.2:3b  (keywords 50%, refused=False, 17s)

Short answer:
Hadoop cannot update a single record in place inside a file because NoSQL databases like Hadoop do not support direct modification of files in the middle.

Explanation:
This is because NoSQL databases, such as Hadoop, use immutable data sets and do not support direct modification of files. This means that a file cannot be modified in the middle, and instead, only "write append" or "delete and recreate" operations are allowed. This is in contrast to standard databases, which allow direct modification of files.

Example:
For example, in Hadoop, when updating a single record in a file, the entire file needs to be copied, which can lead to performance problems and "explosions of files" or "compute treatments for read". This is because Hadoop uses a "Copy on Write" approach, where the entire file needs to be duplicated when updating a single record.

### qwen2.5:7b  (keywords 50%, refused=True, 22s)

I could not find this information in your course materials.

The context provided does not directly address why Hadoop cannot update a single record in place inside a file. However, it does mention that files in NoSQL databases are immutable and can only be written to by appending or deleting and re-creating the file from the beginning. This immutability and the way files are managed in Hadoop reflect a design choice that avoids in-place updates to maintain data integrity and simplify operations.

## p03 (paraphrased) — Which hidden marker tells you that a Hadoop job finished correctly?

Retrieved pages: [7, 22, 27] · Expected pages: [7]

### llama3.2:3b  (keywords 50%, refused=False, 8s)

The hidden marker that tells you a Hadoop job finished correctly is « _SUCCESS ».

This is an example of a hidden file, as shown in the document on page 7. The file is used as an indicator of the success of a Hadoop task, and its presence confirms that the task has completed successfully.

### qwen2.5:7b  (keywords 50%, refused=False, 20s)

The hidden marker file that tells you a Hadoop job finished correctly is « _SUCCESS ».

Explanation:
The « _SUCCESS » file is a special marker file used by Hadoop to indicate that a task has completed successfully. When a Hadoop job is finished, this file is created in the output directory to signal that the job has ended without errors. This is useful for monitoring job statuses and ensuring that data processing has been completed as expected.

## p04 (paraphrased) — What can go wrong when a huge Spark job replaces its old output with new output?

Retrieved pages: [10, 9, 28] · Expected pages: [8, 9]

### llama3.2:3b  (keywords 67%, refused=False, 23s)

Short answer:
When a huge Spark job replaces its old output with new output, it can fail to return the new, refreshed result.

Explanation:
This is because Spark's "Atomic" renaming of files can take too long, causing a timeout or failure inside the "commit" process. This can happen even if the commit is not fully complete, resulting in partially "uncommitted" files being read. As a result, the Spark job may not return the expected, new output.

Example:
Consider a huge Spark job that replaces its old output with new output. If the "Atomic" renaming of files takes too long, the job may fail to return the new, refreshed result. This can happen even if the commit process is not fully complete, resulting in partially "uncommitted" files being read.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 28.

### qwen2.5:7b  (keywords 0%, refused=True, 21s)

I could not find this information in your course materials.

The context provided discusses issues with Spark jobs, but it does not directly address what can go wrong when a huge Spark job replaces its old output with new output. The context mentions failures and issues related to file handling and commit processes, but it does not provide a specific scenario for the replacement of old output by a new one.

## p05 (paraphrased) — Can a program see a file while another program is still writing it in HDFS?

Retrieved pages: [15, 17, 10] · Expected pages: [15, 17]

### llama3.2:3b  (keywords 100%, refused=False, 18s)

Short answer:
No, a program cannot see a file while another program is still writing it in HDFS.

Explanation:
In HDFS, a file is not visible to readers until it has been flushed, which means all its contents have been written to disk. This is because the writer is still modifying the file, and the reader needs to see the final, complete contents of the file.

Example: If a writer is still writing to a file, and a reader tries to read from that file using `readAt(0)`, it will throw a `FileNotFoundException` because the file is still in an intermediate state.

Page 17 of the document explains that readers can only see fully written and flushed files, not intermediate write-in-progress files. This is why the reader in the example cannot see the file until the writer has finished writing to it and flushed the file.

### qwen2.5:7b  (keywords 50%, refused=True, 12s)

I could not find this information in your course materials.

The context provided discusses how a writer can only write and append to a file and that a reader can only see fully written and flushed files, not intermediate writes. However, it does not explicitly state whether a program can see a file while another program is writing it in HDFS.

## p06 (paraphrased) — Why does my Spark job crash with a missing file error after running for a long time?

Retrieved pages: [10, 9, 11] · Expected pages: [10]

### llama3.2:3b  (keywords 0%, refused=False, 21s)

Short answer:
Your Spark job crashes with a missing file error after running for a long time because NoSQL databases like Spark do not follow the ACID principles, which include Atomicity, Consistency, Isolation, and Durability.

Explanation:
The context explains that Spark tries to follow the ACID principles, but only per directory. This means that while Spark may ensure consistency within a single directory, it does not guarantee atomicity, isolation, or durability across multiple directories. In your case, the long-running Spark job may have caused a delay in the commit process, leading to a situation where some files were not fully written or deleted, resulting in a missing file error.

Example:
The context provides an example at SG ( likely a Spark job) where the "Atomic" renaming of files takes too long, leading to a timeout or failure inside the commit process. This illustrates how the lack of atomicity in NoSQL databases like Spark can cause issues with file consistency and lead to crashes like the one you're experiencing.

### qwen2.5:7b  (keywords 0%, refused=True, 14s)

I could not find this information in your course materials.

The context provided discusses issues with Spark jobs, such as failures due to file operations and partial commits, but it does not directly explain why a Spark job would crash with a missing file error after running for a long time.

## p07 (paraphrased) — How do traditional databases make sure committed changes survive a crash?

Retrieved pages: [12, 28, 10] · Expected pages: [2, 12]

### llama3.2:3b  (keywords 100%, refused=False, 24s)

Short answer:
Traditional databases ensure committed changes survive a crash by writing them to the Transactional Log File (WAL) and then flushing the changes to disk immediately.

Explanation:
Traditional databases use a process called "Write-Ahead Logging" (WAL) to ensure that committed changes are written to disk before the transaction is committed. This means that even if the database crashes, the changes will still be written to disk, allowing the database to recover the changes when it starts up again. The changes are then flushed to disk using an Immediate Sync-FLUSH File, which ensures that the changes are written to disk in a timely manner.

Example:
In Oracle, for example, when a transaction is committed, the changes are written to both the REDO File (WAL) and the UNDO File. This ensures that even if the database crashes, the changes will still be recoverable.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 12.

### qwen2.5:7b  (keywords 33%, refused=False, 34s)

Traditional databases ensure committed changes survive a crash by marking the modified block as "Dirty" and saving the changes later to disk. Additionally, they modify the RAM memory directly and write the changes to a Transactional Log File (like the "REDO File" in Oracle) for immediate synchronization.

Explanation:
When you make changes in a traditional database, the system marks the changed block as "Dirty" to indicate that it needs to be saved. This ensures that even if the system crashes, the changes will be written to the disk later. The database also keeps a copy of the old data in the "UNDO File" (in Oracle) so that in case of a crash, the system can revert to the previous state. This process helps in maintaining data consistency and ensuring that committed changes are not lost in case of a system failure.

## p08 (paraphrased) — Why is looking up a row by its key fast in a relational database?

Retrieved pages: [31, 32, 29] · Expected pages: [29, 31]

### llama3.2:3b  (keywords 50%, refused=True, 10s)

Short answer:
I could not find this information in your course materials.

Explanation:
The context does not provide information on why looking up a row by its key is fast in a relational database. The context only discusses the performance of B-TREE indexes in NoSQL and relational databases, but does not address the specific case of relational databases.

### qwen2.5:7b  (keywords 100%, refused=False, 39s)

Looking up a row by its key is fast in a relational database because B-TREE is efficient for this operation, and it is mostly cached in memory. This means that the database can quickly find the row using a logarithmic time complexity, log(N).

Explanation:
When you look up a row by its key in a relational database, the database uses a data structure called B-TREE. B-TREE is designed to provide efficient access to data, especially when you need to find a specific row by its ID. The B-TREE structure allows the database to search for the row in a logarithmic time, which means the time it takes to find the row grows very slowly as the number of rows increases. For example, if you have 1,000 rows, the B-TREE can find the row you're looking for in just a few steps, making the process very fast. Additionally, because the B-TREE is often cached in memory, the lookup operation can be performed even faster.

## p09 (paraphrased) — How can I query an older version of a table in a data lake?

Retrieved pages: [12, 27, 10] · Expected pages: [27]

### llama3.2:3b  (keywords 50%, refused=False, 20s)

Short answer:
You can query an older version of a table in a data lake using the "SELECT AS OF" statement, which is similar to Oracle's "SELECT AS OF" statement and Git's "SELECT AS OF" statement.

Explanation:
The context mentions that the "Iceberg Bonus" feature, which is similar to Oracle's "SELECT AS OF" statement, allows you to query an older version of a table in a data lake. This feature is also similar to Git's "SELECT AS OF" statement. This means that you can use the "SELECT AS OF" statement to query a previous version of a table, allowing you to retrieve data from a previous point in time.

Example: Unfortunately, the context does not provide an example of using the "SELECT AS OF" statement to query an older version of a table.

### qwen2.5:7b  (keywords 100%, refused=True, 30s)

I could not find this information in your course materials.

The context provided does not contain specific details on how to query an older version of a table in a data lake. However, it mentions that "Time Travel Queries" are similar to "SELECT AS OF …" in Oracle, which is also available in Git. This suggests that querying older versions of data might involve using a similar syntax or feature in the data lake system, akin to how you would use "SELECT AS OF" in Oracle or Git.

## p10 (paraphrased) — Why do frequent row updates make an Iceberg table slow?

Retrieved pages: [28, 26, 25] · Expected pages: [28]

### llama3.2:3b  (keywords 33%, refused=False, 16s)

Short answer:
Frequent row updates make an Iceberg table slow because it requires fully duplicating the file or adding a new file containing only the new row.

Explanation:
Iceberg tables are designed to handle large amounts of data and provide high performance for read operations. However, when it comes to frequent row updates, Iceberg tables can become slow. This is because updating a row in an Iceberg table requires either fully duplicating the file, which can lead to an explosion of files, or adding a new file containing only the new row, which can also lead to an explosion of compute treatments for read.

Example: Imagine you have an Iceberg table with millions of rows, and you need to update a single row. To do this, the table would need to be fully duplicated, which would result in a large number of new files being created. This can lead to performance issues and slow down the table.

Page: 28

### qwen2.5:7b  (keywords 33%, refused=False, 51s)

Frequent row updates make an Iceberg table slow because when updating a row, Iceberg needs to either fully duplicate the file or add a new file containing only the updated row and mark the old row for deletion. This leads to an explosion in the number of files and increases the computational load for read operations.

Explanation:
When you update a row in an Iceberg table, the system has to handle this change in a way that maintains data consistency and isolation. To do this, Iceberg uses strategies similar to Git's commit-blob model. Instead of modifying the existing file, it creates a new file with the updated row and marks the old file for deletion. This process can lead to a rapid increase in the number of files, which in turn increases the computational overhead required to manage and read these files. For example, if you frequently update a row, the system might end up creating many small files, each containing a single updated row, which can slow down read operations as the system needs to process more files.

## p11 (paraphrased) — How can a query avoid reading the whole dataset in Big Data?

Retrieved pages: [33, 13, 30] · Expected pages: [33]

### llama3.2:3b  (keywords 0%, refused=False, 18s)

Short answer:
A query can avoid reading the whole dataset in Big Data by using Parallelizing Optimized/Partial Scans.

Explanation:
In Big Data, due to the large size of the dataset, it's not always necessary to read the entire dataset. Instead, queries can be optimized to read only the necessary parts of the data. This is achieved by using Parallelizing Optimized/Partial Scans, which allows the query to process the data in smaller chunks, reducing the amount of data that needs to be read.

Example:
For instance, if a query only needs to filter data based on a specific column, the query can use Partial Scans to read only the rows that match the filter condition, rather than reading the entire dataset.

Source: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf, page 33.

### qwen2.5:7b  (keywords 67%, refused=True, 23s)

I could not find this information in your course materials.

The context provided discusses methods for optimizing Big Data storage and query performance, such as partition pruning, column pruning, predicate push down, and using statistics. However, it does not directly address how to avoid reading the whole dataset with a query.

## p12 (paraphrased) — Why is it a bad idea to keep huge data files in RAM?

Retrieved pages: [30, 23, 28] · Expected pages: [30]

### llama3.2:3b  (keywords 100%, refused=False, 15s)

Short answer:
In BigData, it's generally not a good idea to keep petabyte of file in RAM.

Explanation:
The context states that in BigData, it's not even recommended to keep Page Blocks of files in RAM, as B-TREE files lose their interest if they are not "cached" and accessed per page. This suggests that keeping large files in RAM can be inefficient and may lead to performance issues. The context also mentions that it's better to read compressed files rather than following binary "pointers" within files, which implies that keeping large files in RAM may not be the most efficient way to handle data.

### qwen2.5:7b  (keywords 50%, refused=True, 32s)

I could not find this information in your course materials.

The context does not directly state why it is a bad idea to keep huge data files in RAM. However, it does mention that in BigData, it is generally not a good idea to keep a petabyte of file in RAM, indicating that doing so is impractical due to memory limitations.

## p13 (paraphrased) — How does a database use the operating system to access its files faster?

Retrieved pages: [23, 28, 27] · Expected pages: [23]

### llama3.2:3b  (keywords 100%, refused=False, 13s)

The database uses the operating system to access its files faster by using Memory-Mapped-Files, which are directly visible as virtual Memory from the Linux OS.

This means that the database can access the files without having to read them sequentially, which can be slower. Instead, the operating system maps the files directly into the database's memory, allowing for faster access. This is an optimization provided by the operating system for disk access.

For example, some databases like Oracle prefer to access the files directly through the block devices, bypassing the file system abstraction. This allows for even faster access to the files.

### qwen2.5:7b  (keywords 100%, refused=False, 37s)

A database uses the operating system to access its files faster by utilizing Memory-Mapped-Files (MMAP). This method allows the files to be directly visible as virtual memory from the Linux OS, which is faster than sequential reading of files (reading per block/pages).

Explanation:
Memory-Mapped-Files (MMAP) is a technique where a file is mapped into memory, allowing the file to be accessed like an array. This means that the operating system handles the details of reading and writing to the file, which can be faster than traditional file I/O operations. When a database uses MMAP, it can directly access the data in memory, reducing the overhead of file operations and improving performance.

## p14 (paraphrased) — Can several clients read the same part of a big file at the same time?

Retrieved pages: [16, 13, 30] · Expected pages: [16]

### llama3.2:3b  (keywords 50%, refused=False, 17s)

Short answer:
Yes, several clients can read the same region in "duplicate reads".

Explanation:
According to the context, in NoSQL databases, "duplicate reads" allow several clients to read the same region of a file at the same time. This is illustrated by the example: "Read by client1 Read by client2". This means that multiple clients can access the same part of the file simultaneously, without any issues.

Example: In a NoSQL database, if client1 and client2 both want to read the same part of a large file, the database will allow both clients to access that region at the same time, thanks to "duplicate reads".

### qwen2.5:7b  (keywords 50%, refused=True, 27s)

I could not find this information in your course materials.

The context provided discusses parallel reads and concurrent reads in NoSQL databases, but it does not specifically address whether several clients can read the same part of a big file at the same time in the context of big data storage.

## q18 (out_of_scope) — What is MongoDB and how does it store documents?

Retrieved pages: [23, 13, 30] · Expected pages: none (out of scope)

### llama3.2:3b  (keywords -, refused=True, 13s)

Short answer:
I could not find information about MongoDB in the provided context.

Explanation:
The context only discusses comparisons between NoSQL databases and standard databases, specifically focusing on file systems and storage methods. It mentions MongoDB, but only in the context of comparing it to standard databases, but does not provide information about how MongoDB stores documents.

Example: The context does not provide an example of how MongoDB stores documents.

Document: 1.1-comparison-NoSql-DB-vs-standard-DB.pdf
Page: Not applicable (no information about MongoDB)

### qwen2.5:7b  (keywords -, refused=True, 22s)

I could not find this information in your course materials.

The context provided does not contain specific details about MongoDB or how it stores documents. It discusses general concepts related to NoSQL databases and BigData storage, such as Memory-Mapped-Files and file storage practices, but does not mention MongoDB specifically.

## q19 (out_of_scope) — How does Kafka replicate messages between brokers?

Retrieved pages: [26, 16, 27] · Expected pages: none (out of scope)

### llama3.2:3b  (keywords -, refused=True, 8s)

Short answer:
I could not find information on how Kafka replicates messages between brokers in the provided context.

Explanation:
The context does not mention Kafka replication. It discusses NoSQL databases, their characteristics, and how they solve problems like concurrent read/write issues. The information about Kafka is not present in the provided document.

### qwen2.5:7b  (keywords -, refused=True, 21s)

I could not find this information in your course materials.

The provided context focuses on the Iceberg table and its capabilities for read isolation, concurrent reads, and time travel queries. It does not contain any information about Kafka or how messages are replicated between brokers.

