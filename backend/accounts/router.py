from flask import Blueprint ,redirect,session, render_template,request,flash,url_for
from backend.app import db
from backend.model.qlkh import User
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

tk =Blueprint('accounts',__name__)
@tk.route('/')
def index():
    return render_template('login.html')
    
@tk.route('/dang_ky', methods=['POST', 'GET'])
def dang_ky():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email đã tồn tại. Vui lòng chọn email khác.', 'error')
            return redirect(url_for('accounts.index'))
        
        if not username or not email or not password:
            flash('Vui lòng điền đầy đủ thông tin.', 'error')
            return redirect(url_for('accounts.index'))
        
        mh_pass = generate_password_hash(password)
        role = 'kh'
        new_user = User(username=username, email=email, password=mh_pass, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('accounts.index'))
    
    return redirect(url_for('accounts.index'))

@tk.route('/dang_nhap',methods=['POST', 'GET'])
def dang_nhap():
     if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user :
            flash("Email không tồn tại. Vui lòng thử lại.","error")
            return redirect(url_for('accounts.index'))
        if not check_password_hash(user.password,password):
             flash("Sai mật khẩu. Vui lòng thử lại.", "error")
             return redirect(url_for('accounts.index'))
        flash("Đăng nhập thành công!", "success")
        session['namend']=user.username
        session['emailkh']=user.email
        if user.role == 'admin':
            return redirect(url_for('admin.index')) 
        elif user.role == 'kh':
            return redirect(url_for('customers.index'))
     return redirect(url_for('tk.index'))
