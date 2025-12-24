from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import os
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dictionary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_reviewed = db.Column(db.DateTime)
    review_count = db.Column(db.Integer, default=0)
    mastered = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('words', lazy=True))

# 初始化数据库
with app.app_context():
    db.create_all()
    # 创建默认用户（如果没有的话）
    if not User.query.first():
        default_user = User(
            username='congcong',
            password_hash=bcrypt.hashpw('congcong1996'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        db.session.add(default_user)
        db.session.commit()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True, 'message': '登录成功！'})
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
    
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/words', methods=['GET'])
def get_words():
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    words = Word.query.filter_by(user_id=session['user_id']).order_by(Word.created_at.desc()).all()
    return jsonify([{
        'id': w.id,
        'word': w.word,
        'meaning': w.meaning,
        'example': w.example,
        'created_at': w.created_at.isoformat(),
        'review_count': w.review_count,
        'mastered': w.mastered
    } for w in words])

@app.route('/api/words', methods=['POST'])
def add_word():
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    data = request.get_json()
    word = Word(
        user_id=session['user_id'],
        word=data.get('word'),
        meaning=data.get('meaning'),
        example=data.get('example', '')
    )
    db.session.add(word)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '单词添加成功！',
        'word': {
            'id': word.id,
            'word': word.word,
            'meaning': word.meaning,
            'example': word.example
        }
    })

@app.route('/api/words/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    word = Word.query.filter_by(id=word_id, user_id=session['user_id']).first()
    if word:
        db.session.delete(word)
        db.session.commit()
        return jsonify({'success': True, 'message': '单词删除成功！'})
    return jsonify({'error': '单词不存在'}), 404

@app.route('/api/words/<int:word_id>/review', methods=['POST'])
def review_word(word_id):
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    word = Word.query.filter_by(id=word_id, user_id=session['user_id']).first()
    if word:
        data = request.get_json()
        mastered = data.get('mastered', False)
        
        word.last_reviewed = datetime.utcnow()
        word.review_count += 1
        word.mastered = mastered
        db.session.commit()
        
        return jsonify({'success': True, 'message': '复习记录已更新'})
    return jsonify({'error': '单词不存在'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    total = Word.query.filter_by(user_id=session['user_id']).count()
    mastered = Word.query.filter_by(user_id=session['user_id'], mastered=True).count()
    to_review = Word.query.filter_by(user_id=session['user_id'], mastered=False).count()
    
    return jsonify({
        'total': total,
        'mastered': mastered,
        'to_review': to_review
    })

@app.route('/api/lookup', methods=['GET'])
def lookup_word():
    """自动获取单词释义和例句"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    word = request.args.get('word', '').strip().lower()
    if not word:
        return jsonify({'error': '请输入单词'}), 400
    
    try:
        # 使用 Free Dictionary API (完全免费，无需API key)
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                entry = data[0]
                
                # 提取释义和例句
                meanings = []
                example_text = ''
                
                if 'meanings' in entry:
                    for meaning in entry['meanings']:
                        part_of_speech = meaning.get('partOfSpeech', '')
                        if 'definitions' in meaning:
                            for definition_obj in meaning['definitions']:
                                definition = definition_obj.get('definition', '')
                                
                                # 提取释义（只取前3个）
                                if definition and len(meanings) < 3:
                                    meaning_str = f"{part_of_speech}: {definition}" if part_of_speech else definition
                                    meanings.append(meaning_str)
                                
                                # 提取例句（查找第一个有效的例句）
                                if not example_text:
                                    if 'example' in definition_obj:
                                        example = definition_obj.get('example', '')
                                        if example and isinstance(example, str):
                                            example = example.strip()
                                            if example:
                                                example_text = example
                
                meaning_text = '; '.join(meanings) if meanings else '未找到释义'
                
                return jsonify({
                    'success': True,
                    'word': word,
                    'meaning': meaning_text,
                    'example': example_text
                })
        
        return jsonify({
            'success': False,
            'message': '未找到该单词的释义'
        })
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': '请求超时，请稍后重试'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取释义失败: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5120)

