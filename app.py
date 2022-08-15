from flask import Flask, request
# JWT 사용을 위한 SECRET_KEY 정보가 들어있는 파일 임포트
from config import Config
from flask.json import jsonify
from http import HTTPStatus

from flask_restful import Api

from flask_jwt_extended import JWTManager
from resources.blocklist import check_blocklist

from resources.login import UserLoginResource
from resources.logout import LogoutResource, jwt_blacklist
from resources.memo import MemoListResource
from resources.memo_change import MemoResource
from resources.register import UserRegisterResource



app = Flask(__name__)

# 환경 변수 세팅
app.config.from_object(Config)

# JWT 토큰 만들기
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    # jti = jwt_payload['jti']
    # return jti in jwt_blacklist
    jti = jwt_payload['jti']
    result = check_blocklist(jti)
    
    return result


api = Api(app)

api.add_resource(UserRegisterResource, '/v1/user/register')
api.add_resource(UserLoginResource, '/v1/user/login')
api.add_resource(LogoutResource, '/v1/user/logout')
api.add_resource(MemoListResource, '/v1/memo')
api.add_resource(MemoResource, '/v1/memo/<int:memo_id>')


@app.route('/')
def route_page():
    return "hello!!!!! it is work~"

if __name__ == "__main__" :
    app.run()
