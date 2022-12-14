from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector.errors import Error

# 내가만든 커넥션 함수 임포트
from mysql_connection import get_connection
from flask_jwt_extended import jwt_required, get_jwt_identity


class MemoResource(Resource) : 
    @jwt_required()
    def put(self, memo_id) :

        user_id = get_jwt_identity()
        data = request.get_json()

        try : 
            # 1. DB에 연결
            connection = get_connection()
            # 2. 쿼리문 만들기 : mysql workbench 에서 잘 되는것을 확인한 SQL문을 넣어준다.
            query = '''update memo
                        set title = %s, date = %s, content = %s
                        where user_id =%s and id =%s;'''
            # 파이썬에서, 튜플만들때, 데이터가 1개인 경우에는 콤마를 꼭 써주자.
            record = (data['title'], data['date'], data['content'], user_id, memo_id)
            # 3. 커넥션으로부터 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서에 넣어서 실행한다. // 실제로 실행하는 것은 커서가 해준다.
            # 레코드는 직접입력말고 변수로 넣었을때 실행
            cursor.execute(query, record)

            # 5. 커넥션을 커밋한다. => 디비에 영구적으로 반영하라는 뜻.
            connection.commit()

        except Error as e:
            print('Error', e)
            return {'error' : 400, 'result' : str(e)}, HTTPStatus.BAD_REQUEST
        # finally는 필수는 아니다.
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')
                return {'error' : 200, 'result' : '잘 저장되었습니다.'}, HTTPStatus.OK

    @jwt_required()
    def delete(self, memo_id) :
        user_id = get_jwt_identity()
        try : 
            # 1. DB에 연결
            connection = get_connection()
            # 2. 쿼리문 만들기 : mysql workbench 에서 잘 되는것을 확인한 SQL문을 넣어준다.
            # 실제는 변수로 받아서 넣어준다. 


            query = '''delete from memo
                        where id = %s and user_id = %s;;'''
            # 파이썬에서, 튜플만들때, 데이터가 1개인 경우에는 콤마를 꼭 써주자.
            record = (memo_id, user_id )
            # 3. 커넥션으로부터 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서에 넣어서 실행한다. // 실제로 실행하는 것은 커서가 해준다.
            # 레코드는 직접입력말고 변수로 넣었을때 실행
            cursor.execute(query, record)

            # 5. 커넥션을 커밋한다. => 디비에 영구적으로 반영하라는 뜻.
            connection.commit()

        except Error as e:
            print('Error', e)
            return {'error' : 400, 'result' : str(e)}, HTTPStatus.BAD_REQUEST
        # finally는 필수는 아니다.
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')
                return {'error' : 200,'result' : '잘 삭제되었습니다.'}, HTTPStatus.OK







