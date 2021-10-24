# Zero-Shot Detection
## Baseline
### Build & Run
```shell
docker build -t detector --build-arg SERVICE_PORT=8088 .
docker run -p8088:8088 detector
```
### Test
```shell
./test.sh
```
or
```shell
python3 test.py
```