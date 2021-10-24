FROM cr.msk.sbercloud.ru/aijcontest2021/deeppavlov:sc0_c1.h1.v2.z1

COPY vqa_data /vqa_data
ADD . /mnt
WORKDIR /mnt
RUN pip install --upgrade . && python test.py

WORKDIR /home/user
