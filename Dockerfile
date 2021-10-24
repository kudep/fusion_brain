FROM python:3.7.6
#
# c2c
#

RUN apt-get update && \
    apt-get install -y --no-install-recommends --allow-unauthenticated \
        locales curl libgl1-mesa-glx gcc ffmpeg libsm6 libxext6 &&\
    printf '%s\n%s\n' 'en_US.UTF-8 UTF-8' 'ru_RU.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false &&  \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache

ENV LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

WORKDIR /src/c2c

RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py # Fetch get-pip.py for python 2.7 
RUN python2 get-pip.py && python -m pip install python-multipart

ADD services/c2c/*tar.gz /src/c2c/
RUN cd /src/c2c/antlr-3.1.3/runtime/Python && python2 setup.py install
RUN cd /src/c2c/java2python-0.5.1 && python2 setup.py install


ADD services/c2c/sample.java /src/c2c
ADD services/c2c/java2python3.sh /src/c2c
ADD services/c2c/server.py /src/c2c

#
# htr
#


# RUN git clone https://github.com/puleon/SimpleHTR.git /src/htr

WORKDIR /src/htr
ADD services/htr2/server.py /src/htr

RUN pip3 install -r requirements.txt

RUN rm -r model && wget http://files.deeppavlov.ai/htr_fb/model.tar.gz && tar -xvzf model.tar.gz && rm -rf model.tar.gz

RUN cp model/corpus.txt data

WORKDIR /src/htr/src

COPY services/htr/run.py .
COPY services/htr/img.png .

#
# zsod
#

WORKDIR /src/zsod


COPY services/zsod/requirements.txt /src/zsod/requirements.txt
RUN pip3 install -r /src/zsod/requirements.txt

COPY services/zsod/docker_cache_models.py /src/zsod/docker_cache_models.py
RUN python3 /src/zsod/docker_cache_models.py

COPY services/zsod /src/zsod

#
# vqa
#

WORKDIR /data
RUN wget https://dl.fbaipublicfiles.com/pythia/data/answers_vqa.txt

WORKDIR /src/vqa

COPY services/vqa/reqs.txt /src/vqa/requirements.txt
RUN pip3 install -r /src/vqa/requirements.txt

COPY services/vqa/utils.py /src/vqa/
COPY services/vqa/processing_image.py /src/vqa/
COPY services/vqa/translate.py /src/vqa/
COPY services/vqa/modeling_frcnn.py /src/vqa/
COPY services/vqa/docker_cache_models.py /src/vqa/
RUN python3 /src/vqa/docker_cache_models.py

COPY services/vqa /src/vqa


CMD while true; do sleep 30; done;