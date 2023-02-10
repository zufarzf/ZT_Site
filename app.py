from flask import Flask, render_template, request, session, url_for, flash, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor, CKEditorField, upload_success, upload_fail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
# =====================================
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, BooleanField, SelectField, PasswordField, IntegerField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import check_password_hash, generate_password_hash
# ---------------------
from uuid import uuid4
import os
import random
from random import sample
from datetime import datetime, timedelta
import math
# =====================================
ckeditor_img_path = 'all-statics/admin-static/ckeditor_images'
# =====================================
# def cheked_session_is_user():
#     if 'user_active' in session: return True
#     return False

def cheked_session_is_admin():
    if 'admin_active' in session:
        admin_user = Personal.query.filter_by(id=session['admin_active']).first()
        if admin_user: return True
    return False

def cheked_session():
    if 'edit' in session: del session['edit']
    if 'add' in session:
        new_test = Test.query.filter_by(ques_id=session['add']).first()
        if new_test:
            if new_test.ques == None:
                if len(new_test.images_list) != 0:
                    for i in new_test.images_list:
                        img_path = f'{ckeditor_img_path}/{i}'
                        if os.path.isfile(img_path): os.remove(img_path)

                db.session.delete(new_test)
                db.session.commit()
        del session['add']


SECRET_KEY = '1a470d3cfd210ff67383e70fd9439a1647c1fa3b5522e61f43d061e31a26'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CKEditor configs
CKEDITOR_FILE_UPLOADER = 'upload'
CKEDITOR_UPLOAD_ERROR_MESSAGE = 'Error'
CKEDITOR_ENABLE_CSRF = True


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:MySQL.root.33@localhost:3306/zt_data'
DEBUG = True


app = Flask(__name__, template_folder='all-templates', static_folder='all-statics')
app.config.from_object(__name__)
# --------------------
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)
manager = LoginManager(app)
# --------------------

# this is for flask-login
@manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)






############################## MODELS ################################

class Personal(db.Model):
    __tablename__='personal'
    id = db.Column(db.Integer, primary_key=True)
    # ------------------------------------------
    name = db.Column(db.String(255))
    psw = db.Column(db.Text)
    # -----------------------------------------------j
    is_admin = db.Column(db.Boolean(), default=False)
    permission = db.Column(db.Boolean(), default=False)
    is_user = db.Column(db.Boolean(), default=True)



class Subject(db.Model):
    __tablename__='subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    count = db.Column(db.Integer, default=0)
    # ------------------------------------------
    yakka = db.Column(db.Boolean(), default=True)
    aralash = db.Column(db.Boolean(), default=False)
    # ----------------------------------------------
    test_item = db.relationship('Test', backref='subject', lazy='dynamic')

    def __repr__(self):
        return f"<{self.name}>"





class Test(db.Model):
    __tablename__='test'
    id = db.Column(db.Integer, primary_key=True)
    # ----------------------
    ques = db.Column(db.Text)
    # -----------------------
    true = db.Column(db.Text)
    # ------------------------
    false1 = db.Column(db.Text)
    false2 = db.Column(db.Text)
    false3 = db.Column(db.Text)
    # -------------------------
    ques_id = db.Column(db.Text)
    images_list = db.Column(db.PickleType)
    # ------------------------------------
    subject_item = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __repr__(self):
        return f"{self.ques}"



class Ozu(db.Model):
    __tablename__='ozu'
    id = db.Column(db.Integer, primary_key=True)
    # ------------------------------------------
    user_id = db.Column(db.Integer)
    test_id = db.Column(db.PickleType)
    # ----------------------------------
    starttime = db.Column(db.DateTime())
    endtime = db.Column(db.DateTime())

############################## MODELS ################################





############################## Forms ################################

class SubjectAddForm(FlaskForm):
    subject_name = StringField(validators=[DataRequired()])
    subject_count = IntegerField(validators=[DataRequired()])
    separate = BooleanField()
    mixed = BooleanField()
    submit = SubmitField()



class DeleteForm(FlaskForm):
    chekboxes_list = StringField(validators=[DataRequired()])
    submit = SubmitField()






class CkForm(FlaskForm):
    subjects = SelectField('subjects', choices=[])  # <--
    body = CKEditorField('Body')  # <--
    body_1 = CKEditorField('body_1')  # <--
    body_2 = CKEditorField('body_2')  # <--
    body_3 = CKEditorField('body_3')  # <--
    body_4 = CKEditorField('body_4')  # <--
    submit = SubmitField('Submit')



class Fancy(FlaskForm):
    radio = RadioField(choices=[('yes','Xa'),('no','Yo\'q')])


class UserAddForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    psw = StringField(validators=[DataRequired()])
    is_admin = BooleanField()
    permission = BooleanField()
    is_user = BooleanField()

    submit = SubmitField('Jo\'natish')\

class UserEditForm(FlaskForm):
    name = StringField()
    psw = StringField()
    is_admin = BooleanField()
    permission = BooleanField()
    is_user = BooleanField()

    submit = SubmitField('Jo\'natish')\


class ToifaForm(FlaskForm):
    subject = SelectField('Fan tanlovi', choices=[]) 
    type = SelectField('Amaldagi toifangiz', choices=[]) 
    ball = IntegerField('Maktab bergan ball',  validators=[DataRequired()])
    submit = SubmitField('Jo\'natish')\


#------------------------------------------------------------------
# forms.py

class LoginForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min = 4, message="Loginni kiriting!")], render_kw={'placeholder' : 'Login...'})
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max = 50, message="Parolni to'g'ri kiriting!")], render_kw={'placeholder' : 'Parol...'})
    rm = BooleanField("Eslab qolish")

    submit = SubmitField("Jo'natish")

class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min = 4, message="Loginni kiriting!")], render_kw={'placeholder' : 'Login...'})
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max = 50, message="Parolni to'g'ri kiriting!")], render_kw={'placeholder' : 'Parol...'})
    psw1 = PasswordField(validators=[DataRequired(), EqualTo("psw", "Parolni noto'g'ri qaytardingiz!"), Length(min=4, max = 50, message="Parolni to'g'ri kiriting!")], render_kw={'placeholder' : 'Parol...'})
    
    submit = SubmitField("Jo'natish")

# end forms.py
# -----------------------------------------------------------------


############################## MODELS ################################







############################## Views ################################

# ###################### Subjects ######################

@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def subjects_list():
    if cheked_session_is_admin():
        cheked_session()

        form = DeleteForm()
        subjects = Subject.query.all()


        subjects_li = []
        for i in subjects:
            tests = Test.query.filter_by(subject_item=i.id).all()
            test_lenth = 0
            if tests: test_lenth = len(tests)
            subject = {
                'id':i.id, 'name':i.name,
                'yakka':i.yakka, 'aralash':i.aralash,
                'aralash':i.aralash, 'test_lenth':test_lenth,
                'count':i.count,
            }
            subjects_li.append(subject)


        return render_template(
            'admin-templates/admin-subjects.html',
            page_name='Fanlar',
            form=form,
            url=url_for('subjects_list'),
            subjects=subjects_li
            )
    else: return redirect(url_for('main_page'))


# ========================================================
# ADD

@app.route('/admin/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    if cheked_session_is_admin():
        cheked_session()


        form = SubjectAddForm()
        
        if form.validate_on_submit():
            subject = Subject(
                name=form.subject_name.data,
                count=form.subject_count.data,
                yakka=form.separate.data,
                aralash=form.mixed.data
            )

            try:
                db.session.add(subject)
                db.session.commit()
                flash('Muvafocatlik saqlandi!', category='valide_message')
                return redirect(url_for('add_subject'))
            except:
                flash('Saqlashda hato!', category='invalide_message')
                return redirect(url_for('add_subject'))

        return render_template(
            'admin-templates/admin-add_subject.html',
            form=form, page_name='Fan qoshish',
            url=url_for('add_subject')
            )

    else: return redirect(url_for('main_page'))



# ========================================================
# EDIT

@app.route('/admin/edit_subject/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    if cheked_session_is_admin():
        cheked_session()

        form = SubjectAddForm()
        subject = Subject.query.filter_by(id=id).first()

        if form.validate_on_submit():
            subject.name = form.subject_name.data
            subject.count = form.subject_count.data
            subject.yakka = form.separate.data
            subject.aralash = form.mixed.data
            try:
                db.session.add(subject)
                db.session.commit()
                flash('Muvaffaqiyatli saqlandi!', category='valide_message')
                return redirect(url_for('subjects_list'))
            except:
                flash('Saqlashda hato!', category='invalide_message')
                return redirect(url_for('edit_subject', id=id))

        
        if subject:
            form.subject_name.data = subject.name
            form.subject_count.data = subject.count
            form.separate.data = subject.yakka
            form.mixed.data = subject.aralash

        return render_template(
            'admin-templates/admin-add_subject.html',
            form=form, page_name='Fanni o\'zgartirish',
            url=url_for('edit_subject', id=id)
            )

    else: return redirect(url_for('main_page'))




# ========================================================
# DELETE 

@app.route('/admin/delete_subjects', methods=['GET', 'POST'])
@login_required
def delete_subjects():
    if cheked_session_is_admin():
        cheked_session()


        form = DeleteForm()
        if form.validate_on_submit():
            subjects = str(form.chekboxes_list.data).split(',')
            for subject_id in subjects:
                subject = Subject.query.filter_by(id=int(subject_id)).first()

                print(subject_id)
                if subject: 
                    print(subject)
                    db.session.delete(subject)
            try:
                db.session.commit()
                flash('Muvaffaqiyatli о\'chirildi!', category='valide_message')
                return redirect(url_for('subjects_list'))
            except:
                flash('O\'shirishda hato boldi!', category='invalide_message')
                return redirect(url_for('subjects_list'))

    else: return redirect(url_for('main_page'))


# ========================================================


@app.route('/admin/delete_subject/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    if cheked_session_is_admin():
        cheked_session()


        subject = Subject.query.filter_by(id=id).first()
        if subject:
            try:
                db.session.delete(subject)
                db.session.commit()
                flash('Muvaffaqiyatli о\'chirildi!', category='valide_message')
                return redirect(url_for('subjects_list'))
            except:
                flash('O\'shirishda hato boldi!', category='invalide_message')
                return redirect(url_for('subjects_list'))

    else: return redirect(url_for('main_page'))


# ###################### Subjects ######################







# ######################## Tests #########################


@app.route('/admin/tests_list', methods=['GET', 'POST'])
@login_required
def tests_list():
    if cheked_session_is_admin():
        cheked_session()
        # -----------------
        form =DeleteForm()
        data = Test.query.order_by(Test.id.desc()).all()
        subjects = Subject.query.all()
        return render_template('admin-templates/tests_list.html',
                                data=data, form=form, subjects=subjects)

    else: return redirect(url_for('main_page'))


# ====================================================================


@app.route('/admin/test_add', methods=['GET', 'POST'])
@login_required
def test_add():
    if cheked_session_is_admin():


        form = CkForm()
        subject = Subject.query.first()
        form.subjects.choices = [
            (subject.id, subject.name) for subject in Subject.query.all()
        ]
        # ---------------------------------------
        if 'edit' in session: del session['edit']
        if 'add' not in session:
            session['add'] = str(uuid4())
            inf_ = Test(
                ques=None, true=None,
                false1=None, false2=None,
                false3=None, ques_id=session['add'],
                images_list=[], subject=subject
                )
            # ----------------------
            db.session.add(inf_)
            db.session.commit()
            # ----------------------
        # ---------------------------------------
        else:
            # --------------------------
            if form.validate_on_submit():
                # --------------------------
                inf = Test.query.filter_by(ques_id=session['add']).first()
                # ----------------------
                subject_ = Subject.query.filter_by(id=int(form.subjects.data)).first()
                if subject_: inf.subject = subject_
                # ----------------------
                inf.ques=form.body.data
                inf.true=form.body_1.data
                inf.false1=form.body_2.data
                inf.false2=form.body_3.data
                inf.false3=form.body_4.data
                # ----------------------
                db.session.add(inf)
                db.session.commit()
                # ----------------------
                if 'add' in session: del session['add']
                # ----------------------
                return redirect(url_for('test_add'))
        # ---------------------------------------
        return render_template(
            'admin-templates/test_add.html', form=form,
            url=url_for('test_add')
            )

    else: return redirect(url_for('main_page'))


# ========================================================


@app.route('/admin/edit_test/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_test(id):
    if cheked_session_is_admin():
        cheked_session()

        if id:
            # ---------------------------------------


            # ---------------------------------------
            inf = Test.query.filter_by(id=id).first()
            form = CkForm()
            form.subjects.choices = [
                (subject.id, subject.name) for subject in Subject.query.all()
                ]
            # --------------------------------------------------------------------
            if form.validate_on_submit():
                # --------------------------
                subject_ = Subject.query.filter_by(id=int(form.subjects.data)).first()
                if subject_: inf.subject= subject_
                # --------------------------------
                inf.ques=form.body.data
                inf.true=form.body_1.data
                # -------------------------
                inf.false1=form.body_2.data
                inf.false2=form.body_3.data
                inf.false3=form.body_4.data
                # ----------------------
                db.session.add(inf)
                db.session.commit()
                # ----------------------
                new_images_list = []
                for i in inf.images_list: new_images_list.append(i) 
                # ----------------------
                for i in new_images_list:
                    inf_ = Test.query.filter_by(id=id).first()
                    img_tag = f'src="/admin/files/{i}"'
                    # -----------------------------------
                    if img_tag not in form.body.data and\
                        img_tag not in form.body_1.data and\
                        img_tag not in form.body_2.data and\
                        img_tag not in form.body_3.data and\
                            img_tag not in form.body_4.data:
                        # ----------------------
                        img_path = f'{ckeditor_img_path}/{i}'
                        if os.path.isfile(img_path): os.remove(img_path)
                        # ----------------------
                        new_images_list.remove(i)
                        inf_.images_list = new_images_list
                        # ----------------------
                        db.session.add(inf_)
                        db.session.commit()
                # ---------------------------------------
                if 'edit' in session: del session['edit']
                return redirect(url_for('tests_list'))
            # ----------------------------------------------
            if inf:
                session['edit'] = inf.id
                # -----------------------
                form.body.data = inf.ques
                form.body_1.data = inf.true
                # ---------------------------
                form.body_2.data = inf.false1
                form.body_3.data = inf.false2
                form.body_4.data = inf.false3
                # ---------------------------
                if inf.subject:
                    # -----------------------------------------------------------
                    saubject = Subject.query.filter_by(id=inf.subject.id).first()
                    if saubject:
                        # ---------------------------
                        subjects_select_list = [(saubject.id, saubject.name)] + []
                        # ---------------------------
                        for i in Subject.query.all():
                            if saubject.id != i.id:
                                subjects_select_list.append((i.id, i.name))
                        # ---------------------------
                        form.subjects.choices = subjects_select_list
                    # ----------------------------------------------
            return render_template(
                'admin-templates/test_add.html', form=form,
                url=url_for('edit_test', id=id)
                )
        # -----------------------------------------------
        else: return redirect(url_for('tests_list'))
    else: return redirect(url_for('main_page'))


# ============================================================


@app.route('/admin/delete_test/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_test(id):
    if cheked_session_is_admin():
        cheked_session()
        if id:

            data = Test.query.filter_by(id=id).first()
            if data:
                if len(data.images_list) != 0:
                    for i in data.images_list:
                        img_path = f'{ckeditor_img_path}/{i}'
                        if os.path.isfile(img_path): os.remove(img_path)

                db.session.delete(data)
                db.session.commit()
            
            return redirect(url_for('tests_list'))

        else: return redirect(url_for('tests_list'))
    else: return redirect(url_for('main_page'))



# ============================================================


@app.route('/admin/delete_tests', methods=['GET', 'POST'])
@login_required
def delete_tests():
    if cheked_session_is_admin():
        cheked_session()

        
        form = DeleteForm()
        
        if form.validate_on_submit():
            tests = str(form.chekboxes_list.data).split(',')
            for test_id in tests:
                test = Test.query.filter_by(id=int(test_id)).first()
                
                print(test_id)
                if test: 
                    if len(test.images_list) != 0:
                        for i in test.images_list:
                            img_path = f'{ckeditor_img_path}/{i}'
                            if os.path.isfile(img_path): os.remove(img_path)
                    print(test)
                    db.session.delete(test)
            try:
                db.session.commit()
                flash('Muvafocatlik о\'chirildi!', category='valide_message')
                return redirect(url_for('tests_list'))
            except:
                flash('O\'shirishda hato boldi!', category='invalide_message')
                return redirect(url_for('tests_list'))
        
    else: return redirect(url_for('main_page'))



# ################################## end Tests ####################################





# ################################## CKEeditor uploder ####################################

dir_path = f"{ckeditor_img_path.split('/')[-2]}/{ckeditor_img_path.split('/')[-1]}"

@app.route('/admin/upload', methods=['POST'])
@login_required
def upload():
    if cheked_session_is_admin():
        # -----------------------------
        f = request.files.get('upload')
        extension = f.filename.split('.')[-1].lower()
        # -------------------------------------------
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return upload_fail(message='Image only!')
        filename = f'{uuid4()}.{extension}'
        # ---------------------------------
        if 'add' in session:
            # --------------
            inf = Test.query.filter_by(ques_id=session['add']).first()
            # --------------------------------------------------------
            images_list_ = inf.images_list + [filename]
            inf.images_list = images_list_
            # ----------------------------
            db.session.add(inf)
            db.session.commit()
        # ---------------------
        if 'edit' in session:
            # ---------------
            inf = Test.query.filter_by(id=session['edit']).first()
            # ----------------------------------------------------
            images_list_ = inf.images_list + [filename]
            inf.images_list = images_list_
            # -----------------------------
            db.session.add(inf)
            db.session.commit()

        # --------------------------------------
        f.save(f'{ckeditor_img_path}/{filename}')
        url = url_for('uploaded_files', filename=filename)
        # ------------------------------------------------------
        return upload_success(url, filename=filename)
    else: return redirect(url_for('main_page'))

# ============================================================


@app.route(f'/admin/files/<path:filename>')
@login_required
def uploaded_files(filename):
    return send_from_directory(ckeditor_img_path, filename)

# ################################## end CKEeditor uploder ####################################





# #################################### Users part ######################################

@app.route('/admin/users/', methods=['GET', 'POST'])
@login_required
def users():
    if cheked_session_is_admin():
        cheked_session()

        # --------------------------------------------------------------------
        form = DeleteForm()
        users = Personal.query.order_by(Personal.id.desc()).all()

        return render_template('admin-templates/admin-users.html', users=users, form=form)
    else: return redirect(url_for('main_page'))

# -----======= DELETE PERSONAL =======-------

@app.route('/admin/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if cheked_session_is_admin():
        cheked_session()
        if id:

            data = Personal.query.filter_by(id=id).first()
            if data:
                Personal.query.filter_by(id=id).delete()
                db.session.commit()
            
            return redirect(url_for('users'))

        else: return redirect(url_for('users'))
    else: return redirect(url_for('main_page'))
# ========================================================
# DELETE 

@app.route('/admin/delete_user', methods=['GET', 'POST'])
@login_required
def delete_users():
    if cheked_session_is_admin():
        cheked_session()


        form = DeleteForm()
        if form.validate_on_submit():
            users = str(form.chekboxes_list.data).split(',')
            for users_id in users:
                user = Personal.query.filter_by(id=int(users_id)).first()

                print(users_id)
                if user: 
                    print(user)
                    db.session.delete(user)
            try:
                db.session.commit()
                flash('Muvaffaqiyatli о\'chirildi!', category='valide_message')
                return redirect(url_for('users'))
            except:
                flash('O\'shirishda hato boldi!', category='invalide_message')
                return redirect(url_for('users'))

    else: return redirect(url_for('main_page'))

# ========================================================


# -----======= ADD PERSONAL =======-------

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if cheked_session_is_admin():
        cheked_session()

        form = UserAddForm()
        
        if form.validate_on_submit():
            users = Personal(
                name=form.name.data,
                psw=generate_password_hash(form.psw.data),
                is_admin=form.is_admin.data,
                permission=form.permission.data,
                is_user=form.is_user.data,
            )

            try:
                db.session.add(users)
                db.session.commit()
                flash('Muvaffaqiyatli saqlandi!', category='valide_message')
                return redirect(url_for('users'))
            except:
                flash('Saqlashda hato!', category='invalide_message')
                return redirect(url_for('users'))

        return render_template(
            'admin-templates/users-add.html',
            form=form, page_name='Foydalanuvchi qo\'shish',
            url=url_for('add_user')
            )
    else: return redirect(url_for('main_page'))
    

# ========================================================
# EDIT

@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if cheked_session_is_admin():
        cheked_session()

        form = UserEditForm()
        user = Personal.query.filter_by(id=id).first()

        if form.validate_on_submit():
            if len(form.psw.data) != 0:
                user.psw = generate_password_hash(form.psw.data)
                
            user.name = form.name.data
            user.is_admin = form.is_admin.data
            user.permission = form.permission.data
            user.is_user = form.is_user.data
            try:
                db.session.add(user)
                db.session.commit()
                flash('Muvaffaqiyatli saqlandi!', category='valide_message')
                return redirect(url_for('users'))
            except:
                flash('Saqlashda hato!', category='invalide_message')
                return redirect(url_for('users', id=id))

        
        if user:
            form.name.data = user.name
            form.is_admin.data = user.is_admin
            form.permission.data = user.permission
            form.is_user.data = user.is_user

        return render_template(
            'admin-templates/users-add.html',
            form=form, page_name='Fanni o\'zgartirish',
            url=url_for('edit_user', id=id)
            )
    else: return redirect(url_for('main_page'))

# ################################## end Users part ####################################



# ############################## MAIN APPLICATION ################################


# ================== FILES IN MAIN APPLICATION ===================


# ---------- =========== ----------- ========== --------- ========== --------- ==========

#------------------------------------------------------------------
# getTests.py

def getTest(test):
    answers = [test.true, test.false1, test.false2, test.false3]
    random.shuffle(answers)

    result = { 'ques': test.ques, 
               'answers' : answers, 
               'id' : test.id }

    return result

# end getTests.py
# -----------------------------------------------------------------

# ---------- =========== ----------- ========== --------- ========== --------- ==========

#------------------------------------------------------------------
# UserLogin.py

def getUser(user_id):
    user = Personal.query.filter_by(id=user_id).first()
    return user

class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)


# end UserLogin.py
# -----------------------------------------------------------------

# ---------- =========== ----------- ========== --------- ========== --------- ==========

#------------------------------------------------------------------
# views.py

@app.route('/')  # Главня страница
def main_page():       

    # for admin dashboard
    cheked_session()
    session['item_id'] = None
    session['del_id'] = None

    # end for the admin dashboard

    #--------- Unique admin ----------
    count = 0
    has_admin = Personal.query.filter_by(name='uniqueztadmin').first()
    psw = 'pbkdf2:sha256:260000$UU7OnTfqSlf0QSdP$0c3ef9523f1260a77c47d5661a26557019225ec2581e08434b72ddd56e52e523'

    if has_admin == None:
        user = Personal(name='uniqueztadmin', psw=psw, is_admin=True)
        db.session.add(user)
        db.session.commit()


      # ------- end of the unique admin --------

    return render_template("main-templates/main.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    cheked_session()
    form = RegisterForm()
    if form.validate_on_submit():

        # ----------------------------------
        name = form.name.data
        psw1 = form.psw1.data
        # psw = form.psw.data
        # ----------------------------------

        user_item = Personal.query.filter_by(name=name).first()

        # ----------------------------------
        if user_item:
            flash("Bunday foydalanuvchi mavjud! boshqa ism yoki parol kiriting")
            return redirect(url_for('register'))
        else:
            # ----------------------------------
            password = generate_password_hash(psw1)
            if check_password_hash(password, psw1):
                print("Raaaaaaaabotaet")
                user = Personal(name = name, psw=password)

                db.session.add(user)
                db.session.commit()
               # ----------------------------------
            
                return redirect(url_for('login'))
            else:
                print("Neeeeeeee Raaaaaaaabotaet")
                return redirect(url_for('register'))
        # ----------------------------------
    
    
    return render_template("main-templates/register.html", form=form)

        
@app.route("/selection", methods=['POST', 'GET'])
@login_required
def selection():
    cheked_session()
    # --------------------------
    subject = Subject.query.all()
    select = ToifaForm()
    select.subject.choices = [
        (subjects.name, subjects.name) for subjects in Subject.query.all()
    ]
    select.type.choices = [
        ('oliy_toifa', 'Oliy toifa'),  ('1-toifa', '1-toifa'),  ('2-toifa', '2-toifa'), ('mutaxassis', 'Mutaxassis')
    ]

    if request.method == 'POST':
        # ----------------------------------
        subject = request.form.get("subject")
        toifa = request.form.get("type")
        ball = request.form.get("ball")
        # ----------------------------------

        return redirect(url_for('test', sub=subject, toifa=toifa, 
        ball=ball))

    return render_template("main-templates/select.html", subject=subject, select =select)


@app.route("/test/<sub>/<toifa>/<ball>", methods=['POST', 'GET'])
@login_required
def test(sub=None, toifa=None, ball=None):
    cheked_session()
    form_hidden_tag = UserEditForm()
    # --------------------------
    if request.method == 'POST':
        # -------------------------------
        id_ = current_user.get_id()
        ozu = Ozu.query.filter_by(user_id=id_).first()
        # -------------------------------
        if ozu:
            tests = ozu.test_id
            result_items = []
            # ----------------------------------
            result = 0
            for item in tests:
                # ----------------------------------
                test_item = Test.query.filter_by(id=int(item)).first()
                answer = request.form.get(f"{test_item.id}")
                # ----------------------------------
                if answer == test_item.true:
                    result += 2
            # ----------------------------------
            Ozu.query.filter_by(user_id=id_).delete()
            return redirect(url_for('result', toifa = toifa, ball = ball, result = result))


    # if user loginned and testing time comes
    id_ = current_user.get_id()
    ozu = Ozu.query.filter_by(user_id=id_).first()
    # -------------------------------
    if id_ and ozu:
        tests = ozu.test_id
        result_items = []
        # -------------------------------
        for item in tests:
            test_item = Test.query.filter_by(id=int(item)).all()
        # ----------------------------------
            for i in test_item:
                item = getTest(i)
                result_items.append(item)
        # --------- --------- --------- 
        time_is_up = ozu.endtime - datetime.now()
        # --------- --------- --------- 
        if time_is_up.total_seconds() >= 0:
            time = ozu.endtime
            # --------- --------- --------- 
            hour = time.hour * 1000 * 60 * 60
            minut = time.minute * 1000 * 60
            second = time.second * 1000
            # --------- --------- --------- 
            time = hour + minut + second
                                                 
        else:
            Ozu.query.filter_by(user_id=id_).delete()
            return redirect(url_for('selection'))        
        
    # =====================================================

    else:
        subject = Subject.query.filter_by(name=sub).first()
        if subject:
            # ----------------------------------
            if subject.yakka ==  True:
                test_items = Test.query.filter_by(subject_item=subject.id).all()
                
                if test_items and len(test_items) >= 40:
                    # ----------------------------------

                    result_items = sample(test_items, k=40)
                    result_test = []
                    # ----------------------------------
                    for i in result_items:
                        item = getTest(i)
                        result_test.append(item)

                    result_items = result_test

                    # ----------------------------------
                    arr_id = []
                    for a in result_items:
                        arr_id.append(int(a['id']))

                    id_of_user = current_user.get_id()
                    
                    # ----------------------------------
                    starttime = datetime.now()
                    # hour = timedelta(minutes=1) 
                    hour = timedelta(hours=1) 
                    endtime = starttime + hour 
                    # ----------------------------------

                    kesh = Ozu(user_id = id_of_user, test_id = arr_id, starttime=starttime, endtime=endtime)

                    db.session.add(kesh)
                    db.session.commit()

                    # ----------------------------------
                    ozu = Ozu.query.filter_by(user_id=current_user.get_id()).first()
                    
                    # --------- --------- ---------
                    time_is_up = ozu.endtime - datetime.now()
                    # --------- --------- --------- 
                    if time_is_up.total_seconds() >= 0:
                        time = ozu.endtime
                        # --------- --------- --------- 
                        hour = time.hour * 1000 * 60 * 60
                        minut = time.minute * 1000 * 60
                        second = time.second * 1000
                        # --------- --------- --------- 
                        time = hour + minut + second
                                                 
                    else:
                        Ozu.query.filter_by(user_id=id_).delete()
                        return redirect(url_for('selection'))
                    # ----------------------------------
                else:
                    result_items = []
                    ozu=''
                    return redirect(url_for('testerror', user_id=id_))

            elif subject.aralash == True:
                subjects = Subject.query.all()

                if subjects:
                    # ----------------------------------
                    result_items = []
                    for i in subjects:
                        #-------------------------------------------------------
                        test_item = Test.query.filter_by(subject_item=i.id).all()
                        length = len(test_item)
                        #-------------------------------------------------------
                        if not i.aralash:
                            if i.yakka == True and length >= i.count:
                                if i.id == subject.id:
                                    pass
                                else:
                                    print( i.name )
                                    # ----------------------------------
                                    result_item = sample(test_item, k=i.count)
                                    # ----------------------------------
                                    for p in result_item:
                                        result_items.append(p)
                            else:
                                return redirect(url_for('testerror', user_id=id_))
                    # ----------------------------------
                    # eslab qolishi uchun qilingan
                    arr_id = []
                    for a in result_items:
                        arr_id.append(a.id)

                    id_of_user = current_user.get_id()
                    
                    # ----------------------------------
                    starttime = datetime.now()
                    # hour = timedelta(minutes=1) 
                    hour = timedelta(hours=1) 
                    endtime = starttime + hour 
                    print(f"starttime --> {starttime}, endtime --> {endtime}")                    
                    # ----------------------------------

                    kesh = Ozu(user_id = id_of_user, test_id = arr_id, starttime=starttime, endtime=endtime)

                    db.session.add(kesh)
                    db.session.commit()

                    # ----------------------------------

                    result_test = []
                    if result_items:
                        # ----------------------------------
                        for i in result_items:
                            item = getTest(i)
                            result_test.append(item)
                        # ----------------------------------

                    result_items = result_test
                    # ----------------------------------
                    ozu = Ozu.query.filter_by(user_id=current_user.get_id()).first()
                    time = ozu.endtime
                    # --------- --------- --------- 
                    time_is_up = ozu.endtime - datetime.now()
                    # --------- --------- --------- 
                    if time_is_up.total_seconds() >= 0:
                        time = ozu.endtime
                        # --------- --------- --------- 
                        hour = time.hour * 1000 * 60 * 60
                        minut = time.minute * 1000 * 60
                        second = time.second * 1000
                        # --------- --------- --------- 
                        time = hour + minut + second
                                                 
                    else:
                        Ozu.query.filter_by(user_id=id_).delete()
                        return redirect(url_for('selection'))
                else:
                    result_items = []
                    ozu = ''
                    return redirect(url_for('testerror', user_id=id_))
                    
        # ----------------------------------
        elif not subject:
            result_items = []
            ozu = ''
            return redirect(url_for('testerror', user_id=id_))
        return render_template('main-templates/test.html',
                                result_items=result_items, time=time,
                                form_hidden_tag=form_hidden_tag)

    
    return render_template("main-templates/test.html",
                            result_items=result_items,
                            time=time, form_hidden_tag=form_hidden_tag)
    

@app.route("/testerror/<int:user_id>")
def testerror(user_id):
    Ozu.query.filter_by(user_id=user_id).delete()
    return render_template("main-templates/error.html")


@app.route("/result/<toifa>/<ball>/<result>")
def result(toifa, ball, result):
    cheked_session()
    # --------------------------
    ball = int(ball) + int(result)
    result = True

    if toifa == 'oliy_toifa' and int(ball) <= 80:
        result = True

    elif toifa == '1-toifa' and int(ball) <= 75 and int(ball) >= 65:
        result = True

    elif toifa == '2-toifa' and int(ball) <= 65 and int(ball) >= 60:
        result = True
    
    elif int(ball) <= 60 and int(ball) >=55:
        result = "Tabriklaymiz! mutaxassislikni saqlab qoldingiz"
    
    else:
        result = False


    return render_template('main-templates/result.html', result = result, ball = ball, toifa = toifa)


# ==== login ====

@app.route("/login/", methods=['POST', 'GET'])
def login():
    cheked_session()
    # --------------------------
    if current_user.get_id:
        idp = current_user.get_id()
        # ----------------- ------------------
        us = Personal.query.filter_by(id=idp).first()
        if current_user.is_authenticated and us.is_admin:
            return redirect(url_for('subjects_list'))
        # ----------------- ------------------
        if current_user.is_authenticated and us.is_user==True and us.permission==True:
            return redirect(url_for('selection'))

    # ----------------- ------------------
    form = LoginForm()
    if form.validate_on_submit():
        # ----------------- ------------------
        admin_user = Personal.query.filter_by(name=form.name.data).first()
        # ----------------- ------------------
        if admin_user:
            print(admin_user.psw)
            # ----------------- --------------------------
            if check_password_hash(admin_user.psw, form.psw.data):
                print('PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                if admin_user.is_admin == True:
                    # ----------------- ------------------
                    userlogin = UserLogin().create(admin_user)
                    rm = True if request.form.get('remember') else False
                    login_user(userlogin, remember=rm)
                    # ----------------- ------------------
                    session['admin_active'] = admin_user.id
                    # ----------------- ------------------
                    return redirect(url_for('subjects_list'))
                elif admin_user.is_admin == True and admin_user.is_user == False:
                    flash("Login yoki parol noto'g'ri!")
            
                # ----------------- ------------------
                elif admin_user.permission == True:
                    # ----------------- ------------------
                    userlogin = UserLogin().create(admin_user)
                    rm = True if request.form.get('remember') else False
                    login_user(userlogin, remember=rm)
                    # ----------------- ------------------
                    return redirect(url_for('selection'))
                elif admin_user.permission == False:
                    flash("ZT adminlaridan ruxsat berilmagan!")

            else:
                flash("Login yoki parol noto'g'ri!")
                return redirect(url_for('login'))
        
        else:
            flash("Login yoki parol noto'g'ri!")
            return redirect(url_for('login'))

    return render_template('main-templates/login.html', form=form)



@app.route('/logout')
def logout():
    cheked_session()
    if 'admin_active' in session: del session['admin_active']
    # --------------------------
    logout_user()
    return redirect(url_for('main_page'))

# end views.py
# -----------------------------------------------------------------

# ============ END OF THE FILES IN MAIN APPLICATION =============




# ############################## Main Views ################################
# ############################## Main Views ################################








if __name__ == '__main__':
    app.run(host='0.0.0.0')
