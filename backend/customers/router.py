from datetime import datetime
from flask import Blueprint ,render_template,current_app,request,flash,redirect,url_for,jsonify
from backend.app import db
import os
import uuid
from werkzeug.utils import secure_filename
from backend.model.qlkh import Customer,User,Message
from flask_login import login_required, logout_user, current_user
from werkzeug.security import generate_password_hash


customer =Blueprint('customer',__name__)

@customer.route('/',methods=['GET'])
@login_required
def index():
    if current_user.role != 'kh':
        return redirect(url_for('accounts.index'))
    customer = Customer.query.get(current_user.id)
    user = User.query.get(current_user.id) 
    return render_template('user_nd.html',customer=customer,user=user)

@customer.route('/update', methods=['GET','POST'])
@login_required
def update_user():
    customer = Customer.query.get(current_user.id)
    user = User.query.get(current_user.id)
    ''' 
    file = request.files['file']
    if file:
        random_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename = secure_filename(random_filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        relative_path = os.path.relpath(filepath, start=os.path.abspath(os.path.join(upload_folder, '..')))
        image = f"../static/{relative_path}"
        print("image")
        customer.image = image
    '''
    #request.form.get('key', default_value): Truy cập với một giá trị mặc định nếu không tìm thấy khóa. 
    customer.full_name = request.form.get('full_name', customer.full_name)
    customer.cccd = request.form.get('cccd', customer.cccd)
    customer.sdt = request.form.get('sdt', customer.sdt)
    customer.gender = request.form.get('gender',customer.gender)
    customer.age = request.form.get('age', customer.age)
    customer.address= request.form.get('dc', customer.address)
   
    user.username = request.form.get('name_use', user.username)
    user.email = request.form.get('email_use', user.email)
    password = request.form['password']
    if password:
        user.password = generate_password_hash(password)
    db.session.commit()
    
    flash('Thông tin đã được cập nhật thành công!')
    return redirect(url_for('customer.index'))

@customer.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accounts.index'))

@customer.route('/send_mes', methods=['POST'])
@login_required
def send_mes():
    sender_id = current_user.id  
    receiver_id = 1 
    tn = request.get_json().get('message')  

    if tn:
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=tn,
            timestamp=datetime.utcnow()
        )
        db.session.add(message)
        db.session.commit()

@customer.route('/get_messages', methods=['GET', 'POST'])
@login_required
def get_messages():
    sender_id = current_user.id
    receiver_id = 1
    
    messages = Message.query.filter(
        (Message.sender_id == sender_id) & (Message.receiver_id == receiver_id) | 
        (Message.sender_id == receiver_id) & (Message.receiver_id == sender_id)
    ).order_by(Message.timestamp.asc()).all()
    
    # chuyen du lieu thanh dictionary để dễ xử lý trên frontend
    messages_data = [{"sender": msg.sender.username, "message": msg.message, "timestamp": msg.timestamp} for msg in messages]
    
    # Trả về dưới dạng JSON
    return jsonify(messages_data)
