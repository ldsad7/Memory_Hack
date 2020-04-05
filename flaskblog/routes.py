import paramiko
import json
import os
import secrets
import imageio
import random
import numpy as np

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, send_file, make_response
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf.file import FileField, FileAllowed
from PIL import ImageEnhance, Image
from moviepy.editor import *

RANDOM_TRANSITIONS = ['crossfadein', 'crossfadeout', 'slide_in', 'slide_out', 'make_loopable']
TRANSITION_SIDES = ['left', 'right']
# COLORS = TextClip.list('color')
# FONTS = TextClip.list('font')

# @app.route('/')
# @app.route("/register", methods=['GET', 'POST'])
# def register():
# 	if current_user.is_authenticated:
# 	 return redirect(url_for('account'))
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 	 hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
# 	 user = User(username = form.username.data, email = form.email.data, password = hashed_password)
# 	 db.session.add(user)
# 	 db.session.commit()
# 	 flash('Your account has been created and you can log in', 'success')
# 	 return redirect(url_for('login'))
# 	return render_template('register.html', title='Регистрация', form=form)

# @app.route('/home')
# def home():
#  posts = Post.query.all()
#  return render_template('home.html', posts = posts)

# @app.route('/search', methods=['GET', 'POST'])
# def search():
# 	import time
# 	from flaskblog.sear import compare as srv
# 	from flaskblog.forms import Search
# 	form = Search()
# 	res = []
# 	name_1 = 'Ничего не найдено'
# 	# name_2 = 'Default'
# 	content_1 = ""
# 	# content_1 = "Lorem ipsum dolor ipisicing elit. Temporibus delectus, iste, optio quos cum minima ipsa quis provident aspernatur impedit qui nostrum quibusdam labore doloribus laudantium accusantium quia. Quisquam, necessitatibus.</p>"
# 	count = User.query.count()
# 	if form.submit:
# 		for te in Post.query.order_by(Post.title):
# 			if srv(str(te.title), str(form.info.data)):
# 				name_1 = te.title
# 				content_1 = te.content
# 			elif srv(str(te.content), str(form.info.data)):
# 				name_1 = te.title
# 				content_1 = te.content
# 		form.info.data = ""
# 	return render_template('search.html', title='Поиск', form=form, name_1=name_1, content_1=content_1)

# @app.route('/add_project')
# def add_project():
#     return render_template('add_project.html', title='Добавить проект')


# @app.route("/login", methods=['GET', 'POST'])
# def login():
# 	if current_user.is_authenticated:
# 	 return redirect(url_for('home'))
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(email=form.email.data).first()
# 		if user and bcrypt.check_password_hash(user.password, form.password.data):
# 			login_user(user, remember = form.remember.data)
# 			next_page = request.args.get('next')
# 			return redirect(next_page) if next_page else redirect(url_for('account'))
# 		else:
# 			flash('Login unsuccessful, please check email and password', 'danger')
# 	return render_template('login.html', title='Войти', form=form)

# @app.route("/logout")
# def logout():
# 	logout_user()
# 	return redirect(url_for('register'))


def append_video_url(video_id, video_url):
    with open('url_data.json', 'r') as fd:
        data = json.loads(fd.read())
    data[video_id] = video_url
    with open('url_data.json', 'w') as fd:
        fd.write(json.dumps(data))

def get_video_url(video_id):
    with open('url_data.json', 'r') as fd:
        data = json.loads(fd.read())
    video_url = data.get(video_id, False)
    return video_url

@app.route('/video/<video_id>')
def video_player(video_id):
    video_url = get_video_url(video_id)
    if video_url is False:
        return redirect(url_for('/'))
    return render_template('video_player.html', video_url=video_url)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

class Picture:
	picture = FileField('Загрузить фото', validators=[FileAllowed(['jpg', 'png'])])


# def save_picture(form_picture):
# 	random_hex = secrets.token_hex(8)
# 	_, f_ext = os.path.splitext(form_picture.filename)
# 	picture_fn = random_hex + f_ext
# 	picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
# 	process_picture(picture_path)
# 	video_file = make_video(picture_path, 'output.jpg', seconds=2, fps=50)
# 	i = Image.open(form_picture)
# 	# i.thumbnail(output_size)

# 	i.save(picture_path)
# 	return picture_fn


def process_picture(picture_path):
    ####### SSH
    print('1')
    with paramiko.SSHClient() as ssh:
        print('2')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('3')
        ssh.connect('0.tcp.ngrok.io', username='root', password='Ip4ndwBW8ivnT6b1Qjm7DJ8uRcuujW', port=19197)
        print('4')

        ssh.exec_command("python3 -m pip install -r /content/DeOldify/colab_requirements.txt")
        print('5')
        with ssh.open_sftp() as ftp:
            #######
            print('start first ftp')
            ftp.put(picture_path, '/content/DeOldify/result_images/tmp.png')
            print('stop first ftp')
            print('start exec scrypt')
            _, stdout, _ = ssh.exec_command("python3 /content/DeOldify/our_scrypt.py")
            print('stop exec scrypt')
            image_path = stdout.read().decode('utf-8').strip()
            print('image_path:', image_path)
            print('start second ftp')
            ftp.get('/content/DeOldify/result_images/image.png', picture_path + '.processed')
            print('stop second ftp')


###### Making video out of a picture

def open_and_resize_image(input_):
    img = Image.open(input_)

    max_height = 1344
    max_width = 1080

    if img.height > max_height and img.height > img.width:
        # vertical image
        percentage_decrease = (max_height * 100) / img.height / 100
        new_height = round(img.height * percentage_decrease)
        new_width = round(img.width * percentage_decrease)
        img = img.resize((new_width, new_height))

    if (img.width > max_width and img.width > img.height) or (img.width == img.height and img.width > max_width):
        # Horizontal image
        percentage_decrease = (max_width * 100) / img.width / 100
        new_height = round(img.height * percentage_decrease)
        new_width = round(img.width * percentage_decrease)
        img = img.resize((new_width, new_height))

    return img


def make_video(input, output, seconds=5, fps=4):
    extra_duration = 5 * fps

    total_frames = seconds * fps
    color_percentage_for_each_frame = (100 / total_frames) / 100  # for the 0. mark

    im = open_and_resize_image(input)
    write_to = os.path.join(app.root_path, 'static', 'video', '{}.mp4'.format(output))

    with imageio.get_writer(write_to, format='mp4', mode='I', fps=fps) as writer:
        for i in range(total_frames + extra_duration):
            if i < total_frames:
                processed = ImageEnhance.Color(im).enhance(
                    color_percentage_for_each_frame * i)
                writer.append_data(np.asarray(processed))
            else:
                writer.append_data(np.asarray(im))
    append_video_url(secrets.token_hex(4), write_to)
    return write_to


######

@app.route("/upload_photo", methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		print(f'request.files: {request.files}')
		file = request.files['file0']
		# if file.filename == '':
		# 	flash('No selected file')
		if file:
		    filename = file.filename
		    picture_path = os.path.join(app.root_path, 'static', 'pictures', filename)
		    file.save(picture_path)
		    print('START PROCESSING')
		    process_picture(picture_path)
		    print('STOP PROCESSING')
		    print('START MAKING VIDEO')
		    video_file = make_video(picture_path + '.processed', '.'.join(filename.split('.')[:-1]), seconds=2, fps=50)
		    print("STOP MAKING VIDEO")
		    print('START CONCATING VIDEO')
		    concat_videos([VideoFileClip(video_file)], ['some text here'])
		    print('STOP CONCATING VIDEO')
	return make_response({})

###### Adding text and audio to a picture

def get_lines(text, N):
    lines = []

    cur_sum = 0
    cur_line = []
    for word in text.split():
        word_len = len(word)
        if cur_sum + word_len < N:
            cur_line.append(word)
            cur_sum += word_len
        else:
            lines.append(' '.join(cur_line))
            cur_line = [word]
            cur_sum = word_len
    lines.append(' '.join(cur_line))
    return lines


def concat_videos(videos, texts):
    width = max([video.w for video in videos])
    height = max([video.h for video in videos])
    N = width // 35  # max number of symbols in a line
    processed_videos = []
    duration = 0
    for i, (video, text) in enumerate(zip(videos, texts)):
        duration = video.duration
        lines = get_lines(text, N)

        transition = random.choice(RANDOM_TRANSITIONS)
        transition_duration = random.random() * 2
        if transition in ['crossfadein', 'crossfadeout', 'make_loopable']:
            arr = [
                video.fx(getattr(transfx, transition), transition_duration).resize(height=height)
            ]
        else:  # transition in ['slide_in', 'slide_out']
            transition_side = random.choice(TRANSITION_SIDES)
            arr = [
                video.fx(getattr(transfx, transition), duration=transition_duration, side=transition_side).resize(height=height)
            ]

        # color = random.choice(COLORS).decode('utf-8')
        color = 'white'
        # font = random.choice(FONTS).decode('utf-8')
        font = 'DejaVu-Sans'
        for j, line in enumerate(lines):
            txt_clip = TextClip(
                line, fontsize=60, font=font, color=color
            ).set_position(('center', height - (len(lines) - j) * 100)).set_duration(duration)
            arr.append(txt_clip)

        processed_videos.append(CompositeVideoClip(arr))

    result = concatenate_videoclips(processed_videos, padding=0, method='compose')
    result = result.set_audio(AudioFileClip(os.path.join(app.root_path, 'static', 'audio', 'audio.mp3')).subclip(1, len(videos) * duration + 1))
    result.write_videofile(os.path.join(app.root_path, 'static', 'video', 'result.mp4'), fps=25)

#####

@app.route("/editor", methods=['GET', 'POST'])
def editor():
    if request.method == 'POST':
        try:
            file = request.files['file']
        except KeyError:
            return render_template('editor.html')
        if file.filename == '':
            flash('No selected file')
        if file:
            filename = file.filename
            picture_path = os.path.join(app.root_path, 'static', 'pictures', filename)
            file.save(picture_path)
            print('START PROCESSING')
            # process_picture(picture_path)
            print('STOP PROCESSING')
            print('START MAKING VIDEO')
            video_file = make_video(picture_path + '.processed', '.'.join(filename.split('.')[:-1]), seconds=2, fps=50)
            print('STOP MAKING VIDEO')
            print('START CONCATING VIDEO')
            concat_videos([VideoFileClip(video_file)], ['some text here'])
            print('STOP CONCATING VIDEO')
        # block button and tell that video will be soon...
        return render_template('editor.html', video={
            'video': os.path.join(app.root_path, 'static', 'video', filename),
            'poster': os.path.join(app.root_path, 'static', 'pictures', filename + '.processed')
        })
    return render_template('editor.html')


@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template('index.html')

			# return redirect(url_for('uploaded_file', filename=filename))
	# form = UpdateAccountForm()
	# if form.validate_on_submit():
	# 	# if form.picture.data:
	# 	picture_file = save_picture(form.picture.data)
	# 	current_user.image_file = picture_file
		# current_user.username = form.username.data
		# current_user.email = form.email.data
		# db.session.commit()
		# flash('Your account has been updated', 'success')
		# return redirect(url_for('account'))
	# elif request.method == 'GET':
	# 	form.username.data = current_user.username
	# 	form.email.data = current_user.email
	# image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
	# return render_template('account.html', title='Профиль', image_file = image_file, form = form)

# @app.route("/post/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
# 	form = PostForm()
# 	if form.validate_on_submit():
# 		post = Post(title=str(form.title.data), content=str(form.content.data), user_id = current_user.username)
# 		db.session.add(post)
# 		db.session.commit()
# 		flash('Post has been created', 'success')
# 		return redirect(url_for('home'))
# 	return render_template('create_post.html', title='Добавить микросервис',
# 						form  = form, legend = 'Добавить микросервис')


# @app.route("/post/<int:post_id>")
# def post(post_id):
# 	post = Post.query.get_or_404(post_id)
# 	return render_template('post.html', title=post.title, post=post)


# @app.route("/post1")
# def post1():
# 	return render_template('post.html')

# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
# 	post = Post.query.get_or_404(post_id)
# 	if post.author != current_user:
# 		abort(403)
# 	form = PostForm()
# 	if form.validate_on_submit():
# 		post.title = form.title.data
# 		post.content = form.content.data
# 		db.session.commit()
# 		flash('Your post has been updated!', 'success')
# 		return redirect(url_for('post', post_id = post.id))
# 	elif request.method == 'GET':
# 		form.title.data = post.title
# 		form.content.data = post.content
# 	return render_template('create_post.html', title='Update Post',
# 							form  = form, legend = 'Update Post')

# @app.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
# 	post = Post.query.get_or_404(post_id)
# 	if post.author != current_user:
# 		abort(403)
# 	db.session.delete(post)
# 	db.session.commit()
# 	flash('Your post has been deleted!', 'success')
# 	return redirect(url_for('home'))
