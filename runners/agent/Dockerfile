FROM python:3.7.4

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        locales && \
    printf '%s\n%s\n' 'en_US.UTF-8 UTF-8' 'ru_RU.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false &&  \
	rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache

ENV LANG='en_US.UTF-8' LANGUAGE='en_US.UTF-8' LC_ALL='en_US.UTF-8'

RUN mkdir /src
COPY ./requirements.txt /src/requirements.txt
RUN cat /src/requirements.txt | cut -f1 -d"#" | sed '/^\s*$/d' | xargs -n 1 pip install


COPY ./core/db.py /usr/local/lib/python3.7/site-packages/deeppavlov_agent/core/db.py
COPY ./core/state_manager.py /usr/local/lib/python3.7/site-packages/deeppavlov_agent/core/state_manager.py

COPY . /src/
WORKDIR /src

# wait for a server answer ( INTERVAL + TIMEOUT ) * RETRIES seconds after that change stutus to unhealthy
HEALTHCHECK --interval=5s --timeout=5s --retries=3 CMD exit 0

CMD ./server_run.sh
