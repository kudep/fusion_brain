# FROM python:3.7.6
# FROM cr.msk.sbercloud.ru/aijcontest2021/fusion:0.0.1
FROM cr.msk.sbercloud.ru/aijcontest2021/deeppavlov:sc0_c1

USER user

ADD . /mnt
ADD ./htr_data /htr_data
WORKDIR /mnt
RUN pip install -r requirements.txt && pip install . && python test.py

WORKDIR /hime/user
