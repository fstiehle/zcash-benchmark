# zcash-benchmark
Zcash - Verification Benchmark

Block verification benchmark `/benchmark-client` of the Zcash client 3.0 and evaluation `/offline-analysis`. See our [report](https://github.com/fstiehle/zcash-benchmark/blob/crypto_bench/paper.pdf) for more info. 

## Data

The raw data is contained in `/offline-analysis/raw_data`, and is zipped. It contains results of benchmarks run on two systems, _HDD_ and _SSD_, for short. 

|            | HDD                         | SSD                         |
|------------|-----------------------------|-----------------------------|
| Cores      | 2                           | 6                           |
| Processor  | Intel Core i5               | AMD Ryzen 5 2600X           |
| Clock rate | $2.6\,GHz$                  | $3.60\,GHz$                 |
| RAM, SWAP  | $5\,GB$, $2\,GB$            | $12\,GB$, $2\,GB$           |
| Disk       | WD Elements\newline USB 3.0 | Samsung\newline SSD 860 Evo |
| Disk I/O   | 100\,MB/s                   | 540\,MB/s                   |

The archives contain entries for a benchmark timing the entire block verification time in `data_block.csv`. This amounts to the time the client processes the `ProcessNewBlock` function in `/zcash/src/main.cpp` during synchronization with the network. It also contains benchmarks of more fine grained operations, `data_ecdsa.csv` which captures signature checks in transparent transactions, `data_joinsplit.csv`, `data_shieldedOutput.csv`, `data_shieldedSpend.csv`, which captures the zero-knowledge proofs. All files follow the same scheme: `column1: block hash`, `column2: time in nanoseconds`. 

Additionally, `eval_all_blocks.csv` contain a second, and our most recent benchmark, we performed only for the complete block verification time (the time the client processes the `ProcessNewBlock` function), and is the basis for our model evaluation. 

`offline_analysis/get_blocks.py` can be used to generate an enriched file from a file with `column1: block hash`, `column2: time in nanoseconds`. `offline_analysis/get_blocks.py` will interact with a defined zcash node to generate a csv containing `blockNumber`, `blockSize`, `blockVersion`, `numberTx`, `numberVin`, `numberVout`, `numberJoinSplit`, `numbervShieldedSpend`, `numbervShieldedOutput`, `blockTime`.

The file `/offline-analysis/data/enhanced_block.csv` contains the following columns: block hash, block size, block version, number of transactions, number of inputs, number of outputs, number of joinsplits, number of shielded spends, number of shielded outputs; and was used for our statistical analysis.

# Analysis

See the annotated python notebooks `/offline-analysis/evaluation.py` for our model evaluation, `/offline-analysis/benchmark_analysis.py` for an explorative analysis of our benchmars, and `/offline-analysis/topology.py` for an analysis of the transaction topology of zcash.

## Repeat the benchmark

The benchmark is implemented in `zcash/src/main.cpp`.

Allow at least 4GB of RAM. As the benchmark is run inside a docker container, basic familarity with docker is required. Execute the following commands:

`docker build -t zcash`

`docker run -it --entrypoint /bin/bash zcash`

Inside the container, run the Zcash client via `./zcashd`.

The RPC API is exposed over port 8232. Benchmark data is saved in `zcash/src` as `data_*.csv` file and can be recovered via `docker cp`. 
