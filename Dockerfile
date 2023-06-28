# syntax=docker/dockerfile:1

# Python 이미지 가져오기
FROM python:latest

# Default 폴더 변경
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
COPY server.py .
COPY /template ./template

# 필요한 패키지 설치
RUN pip install -r requirements.txt

# 애플리케이션 실행
CMD python server.py
