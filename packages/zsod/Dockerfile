FROM cr.msk.sbercloud.ru/aijcontest2021/deeppavlov:sc0_c1.h1.v3.z1


# gcc for detectron2, ffmpeg/libsm6/libxext6 for opencv (https://stackoverflow.com/a/63377623)


COPY zsod_data /zsod_data

WORKDIR /mnt

COPY ./requirements.txt /mnt/requirements.txt
RUN pip install -r /mnt/requirements.txt

ADD . /mnt
RUN pip install --upgrade . && python test.py


WORKDIR /home/user
