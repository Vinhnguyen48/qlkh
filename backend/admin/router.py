from datetime import datetime
from flask import Blueprint, jsonify, render_template, current_app, request, redirect, url_for, flash
from sqlalchemy import or_
from backend.app import db
from werkzeug.utils import secure_filename
import os
import uuid
from backend.model.qlkh import Customer, Message, User
from werkzeug.security import generate_password_hash
from flask_login import login_required, logout_user, current_user

admin = Blueprint('admin', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

'''
-lay danh sach id tin nhắn 
- 1-2,2-1,3-1,4-1,1-4 {2,3,4} loai bỏ id là 1 => số người nhắn tin 
for hien thi so nguoi nhắn tin với ad --> lay id tung item de hien thị tin nhắn 
-phân chia theo từng id khách hàng 
- su dung list chua tin nhan list 1 = [{id:1,mes : xxx}]
-chuyển đổi về json  api tin nhan
-sd api chuyen du lieu sang frontend
'''
@admin.route('/', methods=['GET'])
@login_required
def index():
    if current_user.role != 'admin': 
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('accounts.index'))

    page = request.args.get('page', 1, type=int)
    per_page = 8
    search = request.args.get('search_tt', '')
    if search:
        customerds = Customer.query.join(User).filter(
            (Customer.full_name.ilike(f'%{search}%')) |
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        customerds = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', customerds=customerds, searchtk=search)


@admin.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('accounts.index'))

    customer = Customer.query.get_or_404(id)
    user = User.query.get_or_404(customer.user_id)

    if request.method == 'POST':
        customer.full_name = request.form['fullname']
        
        # Upload ảnh
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

        
        customer.age = request.form['age']
        customer.gender = request.form['gender']
        customer.cccd = request.form['cccd']
        customer.address = request.form['address']
        customer.sdt = request.form['sdt']

        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form['password']

        if password:
            user.password = generate_password_hash(password)
        
        db.session.commit()
        return redirect(url_for('admin.index'))

    return render_template('update.html', customer=customer, user=user)


@admin.route('/delete/<int:id>', methods=[ 'GET','POST'])
@login_required
def delete(id):
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('accounts.index'))

    customer = Customer.query.get_or_404(id)
    user = User.query.get_or_404(customer.user_id)
    db.session.delete(user)
    db.session.delete(customer)
    db.session.commit()
    flash('Khách hàng đã được xóa thành công!', 'success')
    return redirect(url_for('admin.index'))

# Thêm khách hàng mới
@admin.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('accounts.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        cccd = request.form.get('cccd')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        sdt = request.form.get('sdt')
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

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email đã tồn tại. Vui lòng chọn email khác.', 'error')
            return redirect(url_for('admin.index'))
        if not username or not email or not password or not fullname or not cccd:
            flash('Vui lòng điền đầy đủ thông tin.', 'error')
            return redirect(url_for('admin.index'))

        mh_pass = generate_password_hash(password)
        role = 'kh'

        new_user = User(username=username, email=email, password=mh_pass, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        user_id = new_user.id
        
        new_customer = Customer(
            user_id=user_id,
            full_name=fullname,
            cccd=cccd,
            age=age,
            gender=gender,
            sdt=sdt,
            image=image,
            address=address,
        )
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('admin.index'))
    
    return render_template('index.html') 


@admin.route('/chat_mes',methods=['GET','POST'])
@login_required
def chat_mes():
   messages = Message.query.filter(
    or_(Message.sender_id != 1, Message.receiver_id != 1)).all()
   ds_id = set()
   for message in messages:
        if message.sender_id != 1:
            ds_id.add(message.sender_id)
        if message.receiver_id != 1:
            ds_id.add(message.receiver_id)

   ds_id = sorted(list(ds_id))
   customers = Customer.query.filter(Customer.id.in_(ds_id)).all()
   user_names = {customer.id: customer.full_name for customer in customers}
   return render_template('admin_chat.html', ds_id=ds_id, user_names=user_names)
  
'''
- id gui :1 id nhan 2 ;id  ||| gui :2 id nhan:1 || tin nhan || thoi gian
'''

@admin.route('/get_messages/<int:id>', methods=['GET'])
@login_required
def get_messages(id):
    sender_id = id  
    receiver_id = 1  
    messages = Message.query.filter(
        ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
    ).order_by(Message.timestamp.asc()).all()
    messages_data = [{"sender": msg.sender.username, "message": msg.message, "timestamp": msg.timestamp} for msg in messages]
    print(f"sender_id: {sender_id}, receiver_id: {receiver_id}")
    return jsonify(messages_data)


@admin.route('/send_mes/<int:id>', methods=['POST'])
@login_required
def send_mes(id):
    sender_id = 1  
    receiver_id = id  
    data = request.get_json()
    message = data['message']
    if message:
        message_obj = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
            timestamp=datetime.utcnow()
        )
        db.session.add(message_obj)
        db.session.commit()
    else:
        return jsonify({"status": "error", "message": "Tin nhắn trống"}), 400


# Đăng xuất
@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accounts.index'))
