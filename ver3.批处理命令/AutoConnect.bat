@echo off
REM 使用curl执行GET请求访问校园网登录URL

set USERNAME=你的学号
set PASSWORD=你的密码
set LOGIN_URL=http://172.21.0.54/drcom/login?callback=dr1003^&DDDDD=%USERNAME%^&upass=%PASSWORD%^&0MKKey=123456^&R1=0^&R2=^&R3=0^&R6=0^&para=00^&v6ip=^&terminal_type=1^&lang=zh-cn^&jsVersion=4.1^&v=2952^&lang=zh

curl -X GET "%LOGIN_URL%"

exit
