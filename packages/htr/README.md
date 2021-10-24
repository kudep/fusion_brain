# Handwritten Text Recognition with TensorFlow for FBC

The code was adapted from [SimpleHTR](https://github.com/githubharald/SimpleHTR) for [FBC](https://github.com/sberbank-ai/fusion_brain_aij2021).

## Install the code

The code was tested with `python3.7.6`.

```
pip install -r requirements.txt
```

## Prepare the data

Download FBC data, convert to grayscale and create LMDB:
```
cd $ROOT_DIR/data
wget https://dsworks.s3pd01.sbercloud.ru/aij2021/htr/train.zip
unzip train.zip
cd $ROOT_DIR/src
python create_lmdb.py --data_dir $ROOT_DIR/data/train
```

## Validate the model trained on FBC

Download the model, and validate on 5% validation split of FBC data: 
```
cd $ROOT_DIR
rm -r model
wget http://files.deeppavlov.ai/htr_fb/model.tar.gz
tar -xvzf model.tar.gz
cp $ROOT_DIR/corpus.txt $ROOT_DIR/data/
cd $ROOT_DIR/src
python main_fb.py --mode validate --fast --data_dir $ROOT_DIR/data/train  --batch_size 500
```

## Train model on FBC data:

```
cd $ROOT_DIR
rm -r model
mkdir model
cd $ROOT_DIR/src
python main.py --mode train --fast --data_dir $ROOT_DIR/data/train  --batch_size 500 --early_stopping 15
```

## Run inference

```
cd $ROOT_DIR/src
python main_fb.py --img_file $ROOT_DIR/data/59065.png
```
