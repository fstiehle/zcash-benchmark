# zcash-benchmark
Zcash - Verification Benchmark

Block verification benchmark `/benchmark-client` of the Zcash client 3.0 and evaluation `/offline-analysis`. See our [report](https://github.com/fstiehle/zcash-benchmark/blob/crypto_bench/paper.pdf) for more info. 

## Run the benchmark

Allow at least 4GB of RAM.

`docker build -t zcash`

`docker run -it --entrypoint /bin/bash zcash`

Run the Zcash client via `./zcashd`.

The RPC API is exposed over port 8232. Benchmark data is saved in `zcash/src` as `data_*.csv` file and can be recovered via `docker cp`. 
