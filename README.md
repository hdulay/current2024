# Real-Time RAG and Agentic Analytics

### What is a Vector?

A vector is an array of numbers that represents unstructured data like text and images. For example, let’s represent these sentences as vectors:


s1 = “I love data”

s2 = “I love candy”

We can take all the terms and create what is called a bag of words:

|ID|candy|data|I|love|
|-|-|-|-|-|
|s1|0|1|1|1|
|s2|1|0|1|1|

### What is an Embedding?

What is an embedding?
> A vector with a large number of dimensions created by a neural network, the vectors are created by predicting for each word what its neighboring words may be.

How is it different from a Bag of Words (BoW)?
> BoW rely on frequencies of words under the unrealistic assumption that each word occurs independently of all others. Example - “Good” vs “Not Good”

### What is a Vector Index?

> An "index" is a data structure that improves the speed of data retrieval operations on a database table.

> A “vector index” is a mechanism that efficiently organizes and retrieves vectors based on their content. 

### What is a Vector Database?

A vector database is a database that encompasses the features designed to manage vector data, including storage, retrieval, and query processing. It may utilize vector indexing as part of its strategy for efficient vector-oriented operations.

## Image Search Demo with pg_vector

What is `pg_vector`?
> Open-source vector similarity search for Postgres.

```bash



```

### Distance Algorithms

Store your vectors with the rest of your data. Supports exact and approximate nearest neighbor search single-precision, half-precision, binary, and sparse vectors L2 distance, inner product, cosine distance, L1 distance, Hamming distance, and Jaccard distance any language with a Postgres client Plus ACID compliance, point-in-time recovery, JOINs, and all of the other great features of Postgres.

