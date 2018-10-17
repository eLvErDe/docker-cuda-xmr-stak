# nvidia-docker image for XMR Stak (CUDA)

This image uses [XMR Stak] from my own [Debian/Ubuntu mining packages repository].
It requires a CUDA compatible docker implementation so you should probably go
for [nvidia-docker].
It has also been tested successfully on [Mesos] 1.5.0.

## Build images

```
git clone https://github.com/eLvErDe/docker-cuda-xmr-stak
cd docker-cuda-xmr-stak
docker build -t cuda-xmr-stak .
```

## Publish it somewhere

```
docker tag cuda-xmr-stak docker.domain.com/mining/cuda-xmr-stak
docker push docker.domain.com/mining/cuda-xmr-stak

```

## Test it (using dockerhub published image)

```
nvidia-docker pull acecile/cuda-xmr-stak:latest
nvidia-docker run -it --rm acecile/cuda-xmr-stak /usr/bin/xmr-stak --help
```

A simple Python script has been added to generate `nvidia.txt` configuration file:

```
nvida-docker run -it --rm --name cuda-xmr-stak acecile/cuda-xmr-stak gen-nvidida-txt.py --help
```

```
usage: gen-nvidida-txt.py [-h] [-i 0 [1 ...]] [-t THREADS] [-b BLOCKS]
                          [-bf BFACTOR] [-bs BSLEEP] [-a] [-s SYNC_MODE]
                          [-m MEM_MODE]

https://github.com/fireice-uk/xmr-stak/blob/master/doc/tuning.md#nvidia-
backend

optional arguments:
  -h, --help            show this help message and exit
  -i 0 [1 ...], --index 0 [1 ...]
                        GPU index (auto for autodetect all GPUs) (default:
                        auto)
  -t THREADS, --threads THREADS
                        Number of threads to run per block (default: 17)
  -b BLOCKS, --blocks BLOCKS
                        Number of CUDA blocks started (default: 60)
  -bf BFACTOR, --bfactor BFACTOR
                        Increase if running on in-use workstation (default: 0)
  -bs BSLEEP, --bsleep BSLEEP
                        Increase if running on in-use workstation (default: 0)
  -a, --affine-to-cpu   Keep GPU thread with along CPU one, can help if both
                        backend are enabled (default: False)
  -s SYNC_MODE, --sync-mode SYNC_MODE
                        CUDA sync mode (?) (default: 3)
  -m MEM_MODE, --mem-mode MEM_MODE
                        CUDA memory mode (?) (default: 1)
```

An example command line to mine Monero on MiningPoolHub (xmr-stak supports nearly all algorythm so check its documentation and picks what you want):
```
nvidia-docker run -it --rm -p 42001:42001 --name cuda-xmr-stak acecile/cuda-xmr-stak /bin/sh -c 'cd /etc/xmr-stak && gen-nvidida-txt.py > nvidia.txt && /usr/bin/xmr-stak --url europe.cryptonight-hub.miningpoolhub.com:20580 --user acecile.catch-all --pass x --rigid catch-all --currency cryptonight_v8 --httpd 42001 --noCPU'
```

Ouput will looks like:
```
Brought to you by fireice_uk and psychocrypt under GPLv3.
Based on CPU mining code by wolf9466 (heavily optimized by fireice_uk).
Based on NVIDIA mining code by KlausT and psychocrypt.
Based on OpenCL mining code by wolf9466.

Configurable dev donation level is set to 0.0%

-------------------------------------------------------------------
You can use following keys to display reports:
'h' - hashrate
'r' - results
'c' - connection
-------------------------------------------------------------------
Upcoming xmr-stak-gui is sponsored by:
   #####   ______               ____
 ##     ## | ___ \             /  _ \
#    _    #| |_/ /_   _   ___  | / \/ _   _  _ _  _ _  ___  _ __    ___  _   _
#   |_|   #|    /| | | | / _ \ | |   | | | || '_|| '_|/ _ \| '_ \  / __|| | | |
#         #| |\ \| |_| || (_) || \_/\| |_| || |  | | |  __/| | | || (__ | |_| |
 ##     ## \_| \_|\__, | \___/ \____/ \__,_||_|  |_|  \___||_| |_| \___| \__, |
   #####           __/ |                                                  __/ |
                  |___/   https://ryo-currency.com                       |___/

This currency is a way for us to implement the ideas that we were unable to in
Monero. See https://github.com/fireice-uk/cryptonote-speedup-demo for details.
-------------------------------------------------------------------
[2018-10-17 17:14:12] : Mining coin: cryptonight_v7
[2018-10-17 17:14:12] : NVIDIA: try to load library 'xmrstak_cuda_backend_cuda10_0'
WARNING: NVIDIA cannot load backend library: libxmrstak_cuda_backend_cuda10_0.so: cannot open shared object file: No such file or directory
[2018-10-17 17:14:12] : NVIDIA: try to load library 'xmrstak_cuda_backend_cuda9_2'
WARNING: NVIDIA cannot load backend library: libxmrstak_cuda_backend_cuda9_2.so: cannot open shared object file: No such file or directory
[2018-10-17 17:14:12] : NVIDIA: try to load library 'xmrstak_cuda_backend'
NVIDIA: found 1 potential device's
[2018-10-17 17:14:12] : Starting NVIDIA GPU thread 0, no affinity.
CUDA [9.1/9.1] GPU#0, device architecture 61: "GeForce GTX 1080 Ti"... device init succeeded
[2018-10-17 17:14:12] : NVIDIA: use library 'xmrstak_cuda_backend'
WARNING: AMD cannot load backend library: libxmrstak_opencl_backend.so: cannot open shared object file: No such file or directory
[2018-10-17 17:14:12] : WARNING: backend AMD (OpenCL) disabled.
[2018-10-17 17:14:12] : Fast-connecting to europe.cryptonight-hub.miningpoolhub.com:20580 pool ...
[2018-10-17 17:14:12] : MEMORY ALLOC FAILED: mlock failed
[2018-10-17 17:14:12] : Pool europe.cryptonight-hub.miningpoolhub.com:20580 connected. Logging in...
[2018-10-17 17:14:13] : Difficulty changed. Now: 500054.
[2018-10-17 17:14:13] : Pool logged in.
[2018-10-17 17:14:13] : New block detected.
[2018-10-17 17:14:47] : New block detected.
[2018-10-17 17:15:43] : Difficulty changed. Now: 350009.
```


## Background job running forever

```
nvidia-docker run -dt --restart=unless-stopped -p 42001:42001 --name cuda-xmr-stak acecile/cuda-xmr-stak /bin/sh -c 'cd /etc/xmr-stak && gen-nvidida-txt.py > nvidia.txt && /usr/bin/xmr-stak --url europe.cryptonight-hub.miningpoolhub.com:20580 --user acecile.catch-all --pass x --rigid catch-all --currency cryptonight_v8 --httpd 42001 --noCPU'
```

You can check the output using `docker logs cuda-xmr-stak -f` 


## Use it with Mesos/Marathon

Edit `mesos_marathon.json` to replace miner parameter, change application path as well as docker image address (if you dont want to use public docker image provided).
Then simply run (adapt application name here too):

```
curl -X PUT -u marathon\_username:marathon\_password --header 'Content-Type: application/json' "http://marathon.domain.com:8080/v2/apps/mining/cuda-xmr-stak?force=true" -d@./mesos\_marathon.json
```

You can check CUDA usage on the mesos slave (executor host) by running `nvidia-smi` there:

```
Wed Oct 17 22:17:44 2018       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.77                 Driver Version: 390.77                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 108...  On   | 00000000:04:00.0 Off |                  N/A |
| 37%   64C    P2   131W / 150W |   2213MiB / 11178MiB |    100%      Default |
+-------------------------------+----------------------+----------------------+
|   1  GeForce GTX 108...  On   | 00000000:05:00.0 Off |                  N/A |
| 44%   68C    P2   130W / 150W |   2213MiB / 11178MiB |    100%      Default |
+-------------------------------+----------------------+----------------------+
|   2  GeForce GTX 108...  On   | 00000000:06:00.0 Off |                  N/A |
| 30%   59C    P2   125W / 150W |   2213MiB / 11178MiB |    100%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      4910      C   /usr/bin/xmr-stak                           2203MiB |
|    1      4910      C   /usr/bin/xmr-stak                           2203MiB |
|    2      4910      C   /usr/bin/xmr-stak                           2203MiB |
+-----------------------------------------------------------------------------+
```

[XMR Stak]: https://github.com/fireice-uk/xmr-stak
[Debian/Ubuntu mining packages repository]: https://packages.le-vert.net/mining/
[nvidia-docker]: https://github.com/NVIDIA/nvidia-docker
[Mesos]: http://mesos.apache.org/documentation/latest/gpu-support/
