# zcash-benchmark
Zcash - Verification Benchmark

Block verification benchmark of the Zcash client 3.0 and evaluation. 

## Run the benchmark

Allow at least 4GB of RAM.

`docker build -t zcash`

`docker run -it --entrypoint /bin/bash zcash`

Run the Zcash client via `./zcashd`.

The RPC API is exposed over port 8232. Benchmark data is saved in `zcash/src` as `data_*.csv` file and can be recovered via `docker cp`. 
