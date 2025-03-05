from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

@app.route('/categories', methods=['GET'])
def get_categories():
    db = get_db()
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM categories')
            return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'news',
    'charset': 'utf8mb4'
}

# 数据库连接函数
def get_db():
    return pymysql.connect(**db_config)

@app.route('/news', methods=['GET', 'POST'])
def handle_news():
    db = get_db()
    try:
        if request.method == 'GET':
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute('''
                    SELECT n.*, c.name as category_name 
                    FROM news n
                    LEFT JOIN categories c ON n.category_id = c.id
                ''')
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            data = request.json
            with db.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO news (title, content, category_id, author_id, status)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    data['title'],
                    data['content'],
                    data['category_id'],
                    1,  # 临时使用固定作者ID
                    'draft'
                ))
                db.commit()
                return jsonify({'id': cursor.lastrowid}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/news/<int:news_id>', methods=['PUT', 'DELETE'])
def single_news(news_id):
    db = get_db()
    try:
        if request.method == 'PUT':
            data = request.json
            with db.cursor() as cursor:
                cursor.execute('''
                    UPDATE news SET
                        title = %s,
                        content = %s,
                        category_id = %s,
                        status = %s
                    WHERE id = %s
                ''', (
                    data['title'],
                    data['content'],
                    data['category_id'],
                    data['status'],
                    news_id
                ))
                db.commit()
                return jsonify({'status': 'success'})

        elif request.method == 'DELETE':
            with db.cursor() as cursor:
                cursor.execute('DELETE FROM news WHERE id = %s', (news_id,))
                db.commit()
                return jsonify({'status': 'success'})

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/news/<int:news_id>/status', methods=['PATCH'])
def update_news_status(news_id):
    db = get_db()
    try:
        data = request.json
        with db.cursor() as cursor:
            # 更新状态并记录发布时间
            cursor.execute('''
                UPDATE news SET
                    status = %s,
                    publish_time = CASE 
                        WHEN %s = 'published' THEN NOW()
                        ELSE publish_time 
                    END
                WHERE id = %s
            ''', (data['status'], data['status'], news_id))
            db.commit()
            return jsonify({'status': 'success'})

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# 添加用户查询接口
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT id, username FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            if user:
                return jsonify(user)
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    db = get_db()
    try:
        data = request.json
        with db.cursor() as cursor:
            cursor.execute('''
                UPDATE news 
                SET title = %s, content = %s, category_id = %s
                WHERE id = %s
            ''', (data['title'], data['content'], data['category_id'], news_id))
            db.commit()
            return jsonify({'status': 'success'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)