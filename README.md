# 2023-1 Lablup Internship Toy Project

## 프로젝트 소개 (Project Introduction)

2023년 Lablup 하계 인턴십에서 진행한 Toy Project로 single-room / multi-user / real-time 기능을 가진 간단한 web chat app입니다.

프로젝트 구현 과정에서 `aiohttp`와 `redis-py` 패키지가 이용 되었습니다.

<br>

## 프로젝트 실행 방법 (How to run a project)

1. terminal을 이용하여 프로젝트가 저장되길 원하는 경로로 이동한 뒤, 다음 명령어를 이용하여 저장소를 clone 합니다.

```bash
git clone https://github.com/Choi-Jiwon-38/2023_lablup_toy_project.git
```

2. 다음 명령어를 통하여 프로젝트의 root 디렉토리로 이동합니다.
```bash
cd 2023_lablup_toy_project
```

3. 프로젝트가 정상적으로 실행될 수 있도록 redis 서버를 실행합니다.
```bash
docker run 6379:6379 -it redis/redis-stack:latest
```

4. chat app의 서버를 실행합니다.
```bash
python server.py
```

5. [http://localhost:8080](http://localhost:8080)에 접속하여 프로젝트 결과물을 확인할 수 있습니다.
