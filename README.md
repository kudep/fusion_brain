## prochtenie

pam-pam

## Main description

pam-pam

## Requirements

* docker
* docker-compose
* make

## QuickStart

Make sure all dependencies are installed, you cat init env after `git clone` :

``` bash
make install_env # build a linter docker image, create 'data' dirs, download datasets. 
```

Build and up docker-compose environment:

``` bash
make up_build_env # or docker-compose up -d --build ; bash tools/ping_services.sh
```
``` 
Before sending a PR, please, check tests and fix style:
```bash
make run_test # or docker run -v ${PWD}:/data prochtenie_linter:1.0 bash lint.sh; bash tools/test_services.sh
```

and

``` bash
make run_format # or docker run -v ${PWD}:/data prochtenie_linter:1.0 bash format.sh
```
To create greedy report you can run 
```bash
make run_greedy_report
```

### What's happened?

The commands shown above are described in `makefile`

### Extended guide

After installation you can run all services:

``` bash
docker-compose up -d
```

To observe the status of all services, run:

``` bash
docker-compose ps
```
Output:
``` 
              Name                           Command                State         Ports  
-----------------------------------------------------------------------------------------
agent                              /bin/sh -c ./server_run.sh    Up (healthy)            
basic_reader                       /bin/sh -c ./server_run.sh    Up (healthy)            
demo_service                       /bin/sh -c ./server_run.sh    Up (healthy)            
dupl_error_solver                  /bin/sh -c ./server_run.sh    Up (healthy)            
fact_kb_skill                      /bin/sh -c ./server_run.sh    Up (healthy)            
rule_based_response_selector       /bin/sh -c ./server_run.sh    Up (healthy)            
sentence_argumentation_extractor   /bin/sh -c ./server_run.sh    Up (healthy)
```

Running tests of a specific service:

``` bash
docker-compose exec $service python test_server.py
```

To get a log of your service:

``` bash
docker-compose logs -f $service
```

Check and run agent:

``` bash
docker-compose exec agent python run.py
```

If you want to get access to a container by ports you can extend `docker-compose.yml` . For an example you can create custom `dev.yml` file with content:

``` yaml
services:
  YOUR_SERVICE_NAME:
    ports:

      - LOCAL_PORT:CONTAINER_PORT

version: "3.7"

```

After that just run your yml file with `docker-compose.yml` :

``` bash
docker-compose -f docker-compose.yml -f dev.yml up -d
```

Now you can send request to `localhost:{LOCAL_PORT}/{ENDPOINT}` for your contained service. For an example you can just run a local tests of service.
 

``` bash
python ${PATH_TO_YOUR_SERVICE_DIR}/test_server.py
```

If you change `Dockerfile` after that you have to run `docker-compose build` or `docker-compose run -d --build` .

To use the GPU, you have to change the base docker image. Check out the available base images for [pytorch](https://hub.docker.com/r/pytorch/pytorch) or for [tensorflow](https://hub.docker.com/r/tensorflow/tensorflow). For example look at the `services/annotators/morphosyntactic_parser/Dockerfile` and `services/annotators/morphosyntactic_parser/requirements.txt`.

Update `CUDA_VISIBLE_DEVICES` in file `gpus.yml` for example:
```yaml
services:
  morphosyntactic_parser:
    environment:
      - CUDA_VISIBLE_DEVICES=0,1,2,3

```

## Tests
For creating test by auto needs updated `services/agent/pipeline_conf.yml` and `docker-compose.yml` files by corresponding changes of new service. The service has to be run.

For example, to create new input test file for `demo_service` you need to change
`services/agent/pipeline_conf.yml` file:
```yaml
+    demo_service:
+      connector:
+        protocol: http
+        url: http://demo_service:2087/model
+      dialog_formatter: formatters:base_formatter_in
+      response_formatter: formatters:base_formatter_out
+      previous_services:
+        - basic_reader_annotator
+      state_manager_method: add_hypothesis
```
and `docker-compose.yml` file:
```yaml
+  demo_service:
+    build:
+      args:
+        SERVICE_NAME: demo_service
+        SERVICE_PORT: 2087
+      context: ./services/solvers/demo_service/
+    environment:
+      - STORE_DATA_ENABLE=true
+    tty: true
+    volumes:
+      - ./services/solvers/demo_service:/src
+      - ./data:/data
+      - ./common_packages:/common_packages
```
after that run this command to use  `data/datasets/neznaika.v*/eng/train/eng-write_2833_parsed.json` file as base of test:
```bash
bash tools/create_service_test.sh \
    --service_name=demo_service \
    --instance_name=eng-write_2833_parsed

```
now you created input test file, then run this command for create output file by default:
```bash
docker-compose exec demo_service python test_server.py
```
you can see:
```
----------------------------------------
cand = {'ping': 'pong'}
New output file is created
request_file = test_data/eng-write_2833_parsed_input.json
response_file = test_data/eng-write_2833_parsed_output.json
Traceback (most recent call last):
  File "test_server.py", line 47, in <module>
    test_skill(args.rewrite_ground_truth)
  File "test_server.py", line 42, in test_skill
    assert warnings == 0
AssertionError

```
If all are rihgt you can see `services/solvers/demo_service/test_data/eng-write_2833_parsed_input.json` and `services/solvers/demo_service/test_data/eng-write_2833_parsed_input.json` new files.

A default directory for test samples is `teat_data`. You can set another directory for that you have to use environment variable `TEST_DATA_DIR`. Set up it in docker-compose.yml file. 

If you want rewrite outputs files use key `-r`:
```bash
docker-compose exec demo_service python test_server.py -r
```

## Structure of Data
You can get struct of data by looking in `test_data` directory.

### Solver/Annotator Input Data

``` json
{
    "input_data": [
        {
            "raw_input": "RAW_TEXT_1",
            "annotations": {
                "basic_reader": "OUTPUT_DATA",
                "ANNOTATOR_1_NAME": "OUTPUT_DATA",
                "ANNOTATOR_2_NAME": "OUTPUT_DATA"
            },
            "solvers": [
                {"SOLVER_1_NAME": "OUTPUT_DATA"},
                {"SOLVER_2_NAME": "OUTPUT_DATA"}
    ],
            "post_annotations": {
                "POST_ANNOTATOR_1_NAME": "OUTPUT_DATA",
                "POST_ANNOTATOR_2_NAME": "OUTPUT_DATA"
            }
        },
        "(OTHER_ELEMENTS_OF_BATCH)"
    ]

```

### basic_reader Output Data

``` json
{
    "annotations": {
        "sections": [
            {
                "link": [
                    "#LINK_LABEL"
                ],
                "link_information": [
                    "#TEXT_WITH_TAG"
                ],
                "raw_text": "TEXT",
                "raw_type": "SECTION_TYPE",
                "start_span": "INDEX",
                "end_span": "INDEX",
                "text": "TEXT",
                "type": "SECTION_TYPE"
            }
        ],
        "mistakes": [
            {
                "link": [
                    "#LINK_LABEL"
                ],
                "link_information": [
                    "#TEXT_WITH_TAG"
                ],
                "raw_text": "TEXT",
                "raw_type": "ERROR_TYPE",
                "start_span": "INDEX",
                "end_span": "INDEX",
                "text": "TEXT",
                "type": "ERROR_TYPE"
            }
        ],        
    },
    "clear_essay": "TEXT",
    "clear_essay_sentences": [
       [
          "SENTENCE"
       ]
    ],
    "criteria": {
        "К_NAME": "K_VAL"
    },
    "raw_essay": "TEXT",
    "subject": "SUBJECT_NAME",
    "meta": {
        "тема": "TOPIC",
        "год": "YEAR",
        "тест": "TEST_TYPE",
        "эксперт": "EXPERT_ID",
        "класс": "GRADE",
        "линия": "LINE",
        "отрывок": "TEXT"
    }
}

```

## Dataset

`tools/load_data.sh` loads `prochtenie_labeled_preview` and `prochtenie_unlabeled_preview` parts to `data/datasets`


## TODO
- OTAR on python to speedup calculations
- ML for esembling of gector and bertgec
- a thrashhold for gector native esembling by ` model_paths=["/model_data/xlnet_0_gector.th", "/model_data/roberta_1_gector.th"],`

## Contributing

Contributing information is placed in `CONTRIBUTING.md` file.

## License

This project is licensed under the terms of the Apache 2.0 license.
