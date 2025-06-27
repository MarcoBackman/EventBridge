# VS Event Bridge Service

### 해당 API 서비스는 다음과 같은 큰 항목의 서비스를 제공한다

- (클라이언트 & 플랫폼) 라이선스 토큰 발급, 라이선스 토큰 관리
- 이메일 전송 서비스
- 슬랙 포스팅 서비스
- 공용(클라이언트 & 웹 & 인공지능) S3 버킷 서비스 업로드, 다운로드
- 클라이언트 & 웹 공용 DB

## 외부 파이선 라이브러리 설정, 설치, 그리고 실행 법

1. 루트 경로에서 venv 설치 (가상 파이선 부트 환경 제공) 후 even 환경으로 진입

> python -m venv venv
> venv\Scripts\activate

2. 필요 파이선 라이브러리 설치
> pip install -r requirements.txt

3. 실행에 필요한 .env 파일 설정 (루트 경로에 제작)

## 환경변수 설정
```
# .env
APP_PORT=
APP_URL=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SES_REGION=
SES_SENDER_EMAIL=

SLACK_CLIENT_ID=
SLACK_BOT_TOKEN=

DB_HOST=localhost
DB_PORT=
DB_NAME=
DB_USER_ID=
DB_PASS=
DB_IS_SSL=

SECRET_KEY=
ALGORITHM="pbkdf2_sha256"

DATABASE_URL="mysql+aiomysql://${DB_USER_ID}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
```

4. 실행

>python -m app.main


### 사용 프레임워크
- fastAPI
- venv - uvicorn

### 사용되는 외부 서비스
- AWS SES (AWS 연결 필요)
- SLACK (슬랙봇 설정 및 토큰 발급 필요)
- MySQL - event_bridge


### API endpoint 정보



코드 구조

```
├── venv/
├── app/
│   ├── main.py                    # FastAPI app instance, API router inclusion
│   ├── api/
│   │   └── v1/
│   │       └── controller/
│   │           ├── __init__.py
│   │           ├── email_controller.py       # 이메일 API routes
│   │           ├── slack_controller.py       # 슬랙 API routes
│   │           └── license_controller.py        # 라이선스 API routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # .env 에서 환경 변수 로드
│   │   ├── database.py            # DB 연결
│   │   └── exceptions.py          # Custom exceptions (구현 필요)
│   ├── db-script/
│   │   └── V01__license_table.sql # 라이선스 발급용 mysql query script
│   ├── dto/
│   │   ├── __init__.py
│   │   ├── email_request_dto.py   # 이메일 REST API 요청 형식
│   │   ├── license_request_dto.py # 라이선스 REST API 요청 형식
│   │   ├── license_response_dto.py# 라이선스 REST API 응답 형식
│   │   └── slack_request_dto.py   # 슬랙 REST API 요청 형식
│   ├── enums/
│   │   ├── __init__.py
│   │   ├── license_type.py        # 라이선스 메시지 enum
│   │   └── slack_message_type.py  # 슬랙 메시지 enum
│   ├── models/
│   │   ├── schema/
│   │   │   ├── __init__.py
│   │   │   └── license_schema.py  # 라이선스용 ORM
│   │   ├── __init__.py
│   │   └── license.py             # 라이선스용 Python 오브젝트 모델
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── license_repository.py  # 사용자 토큰 DB 
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py       # 이메일 비지니스 로직
│   │   ├── slack_service.py       # 슬랙 비지니스 로직
│   │   ├── license_service.py     # 토큰 제작 및 색인 로직
│   ├─── utils/ 
│   │   ├── __init__.py
│   │   ├── logger.py                #로거 (색상, 레벨 제공)
│   │   └── license_key_generator.py #라이선스키 암호화 및 복호화 툴
│   ├─── __init__.py
│   └─── main.py
├── tests/
├── .env                           # 사용 토큰, API 키, 비밀번호
└── README.md
```

API Controller 테스트 방법
Swagger URL: http://localhost:8002/docs#/

## 개발 완료된 기능
- 라이선스 기능
- 슬랙봇 연결 및 채팅 전송

## 개발 보수가 필요한 기능
- 슬랙봇 채팅 형식 정규화 및 이쁜 레이아웃 (아이콘, 레벨 별 알림 메시지 변화 등)

## 개발이 필요 한 기능
- AWS SES 연계
- 메일 전송 레이어 및 DB 설정
- 공용(클라이언트 & 웹 & 인공지능) S3 버킷 서비스 업로드, 다운로드
- 클라이언트 & 웹 공용 DB

## 앞으로 할 일
- PROD가 현재 uvicorn 으로만 동작중, 트래픽이 많아지면 nginx로 전환 고려 해 볼 것
