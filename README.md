# fast-web
fastapi web project


기술스택 : GCP,Centos:7,Docker,Nginx, FastAPI, Mongodb, Python 


# Getting Started


GCP : 
1. Nginx 인스턴스 
2. FastAPI server 인스턴스 

Docker :
인스턴스위에 Docker 설치하여 Container 로 운영 

Nginx 서버 : 모든 호스트로부터 요청을 받을수있게 하지만 Nginx 에서 특정 IP (개발 하는 팀원을 제외한 사람은 요청을 보낼수없도록 설정)
FastAPI 서버 VPC 방화벽 설정을 하여 Nginx 서버로만 요청이 올수있도록 설정 

Nginx 설치 특이사항 : 도메인 주소를 받지않고 IP로 서버에 접속하다보니 브루트포스방식으로 악의적인 공격이많이 들어온다. 가령 .env 파일을 요청하거나 
따라서 Nginx 를 앞단에 두어 악의적인 공격을 최대한 막고 신뢰할수있는 request만 받는다.


Mongodb : Motor library로 비동기로 작성. 최대한 fastAPI 아키텍쳐 특성을 살리기위해서







