from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from backend.app import db
from werkzeug.utils import secure_filename
import os
from backend.model.qlkh import Customer, User
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}



@admin.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int) 
    per_page = 8 
    search =  request.args.get('search_tt', '')
    if search:
       
        customerds = Customer.query.join(User).filter(
            (Customer.full_name.ilike(f'%{search}%')) |  
            (User.username.ilike(f'%{search}%')) |      
            (User.email.ilike(f'%{search}%'))           
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        customerds = Customer.query.paginate(page=page, per_page=per_page, error_out=False)  
    return render_template('index.html', customerds=customerds,searchtk=search)


@admin.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    customer = Customer.query.get_or_404(id)
    user = User.query.get_or_404(customer.user_id)
  
    

    if request.method == 'POST':
        customer.full_name = request.form['fullname']
        
        #up image
        file = request.files['file']
        if file :
            upload_folder = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)  
            customer.image =  filepath
        customer.age = request.form['age']
        customer.gender = request.form['gender']
        customer.cccd = request.form['cccd']
        customer.address = request.form['address']
        customer.email = request.form['emaillh']
        
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form['password']



        if password:
            user.password = generate_password_hash(password)
        
        db.session.commit()
        flash('Cập nhật thông tin thành công!', 'success')
        return redirect(url_for('admin.index'))

    return render_template('update.html', customer=customer, user=user)
@admin.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    customer = Customer.query.get_or_404(id)
    user = User.query.get_or_404(customer.user_id)
    db.session.delete(user)
    db.session.delete(customer)
    db.session.commit()
    flash('Khách hàng đã được xóa thành công!', 'success')
    return redirect(url_for('admin.index'))
@admin.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        cccd = request.form.get('cccd')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        emaillh = request.form.get('emaillh')

        file = request.files['file']
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)  
        image_kh = filepath.split("..", 1)[-1]
        image =  image_kh
        
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
            image=image,
            address=address,
            emaillh=emaillh
        )
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('admin.index'))
    
    return render_template('index.html') 


