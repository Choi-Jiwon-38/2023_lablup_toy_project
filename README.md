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

3. Docker Compose 파일에 정의된 서비스를 build 하여 필요한 Docker 이미지, 의존성, 설정 등을 설치 및 적용합니다.
```bash 
docker compose build
docker-compose up
```
또한, 아래의 명령어를 통하여 compose up과 build를 동시에 진행할 수 있습니다.
```bash
docker-compose up --build
```

4. [http://localhost:8080](http://localhost:8080)에 접속하여 프로젝트 결과물을 확인할 수 있습니다.
