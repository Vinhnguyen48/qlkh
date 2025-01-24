from flask import Blueprint ,render_template,current_app,request,flash,redirect,url_for
from backend.app import db
import os
import uuid
from werkzeug.utils import secure_filename
from backend.model.qlkh import Customer,User
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
