# FROM python:3.7.6
# FROM cr.msk.sbercloud.ru/aijcontest2021/fusion:0.0.1
# FROM cr.msk.sbercloud.ru/aijcontest2021/deeppavlov:sc0_c1
FROM cr.msk.sbercloud.ru/aijcontest2021/deeppavlov:sc0_c1.h2.v3.z2

USER user

ADD . /mnt
ADD ./htr_data /htr_data
WORKDIR /mnt
RUN pip install -r requirements.txt && pip install --upgrade . && python test.py

WORKDIR /home/user
