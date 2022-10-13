#!/bin/bash
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"ingi9786@naver.com"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email ${SUPERUSER_EMAIL} --noinput || true

# django 3.0부터 createsupuser --noinput으로 
# 환경변수로 REQUIRED_FIEDLS의 필드들이 DJANGO_SUPERUSER_UPPER FIELD NAME이 설정되어있으면 non-interactive한 실행 시 자동으로 슈퍼유저를 생성.
# 내 모델에는 email, password, last_name이 필수이므로 .env에 설정해둠. username이 필요없다. 