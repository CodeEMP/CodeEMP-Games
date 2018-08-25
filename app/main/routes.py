from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm
from app.models import User
from app.main import bp


bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()


    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/friend/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot friend yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.friend(user)
    db.session.commit()
    flash('You are following %(username)s!', username=username)
    return redirect(url_for('main.user', username=username))


@bp.route('/unfriend/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfriend yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfriend(user)
    db.session.commit()
    flash('You unfriended %(username)s.', username=username)
    return redirect(url_for('main.user', username=username))
