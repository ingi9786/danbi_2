# 내 로컬 환경의 python version과 동일한 이미지
FROM python:3.9.5-slim
# backend 폴더의 내용을 container의 /app으로 옮긴다. 
COPY . /app
WORKDIR /app
# app에 바로 설치해도 되지만, 일반적으로 opt 디렉터리 밑에 저장된다. 
# 사실 local에도 backend 폴더 안에 venv는 없다.
RUN python3 -m venv /opt/venv
# pip install -r requirements.txt 인데 pip의 버전을 모른다. pip의 경로를 명시하자.
# local의 venv의 pip.exe위치와 다름에 주의하자. 이 image는 리눅스기반이므로.
# 설치한 가상환경의 gunicorn실행을 위한 명령어를 entrypoint.sh로 저장.

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]