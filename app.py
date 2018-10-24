from flask import Flask, request, render_template, session, redirect, flash
import util.accounts
import util.posts
import base64

app = Flask(__name__)
app.secret_key = util.accounts.get_salt()


@app.route('/')
def index():
    if util.accounts.is_logged_in(session):
        return render_template(
            'index_user.html',
            user=util.accounts.get_logged_in_user(session)
        )
    else:
        return render_template('index_anon.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


#  @app.route('/search')
#  def search():
    #  return render_template('search.html')


@app.route('/edit')
def edit():
    if not util.accounts.is_logged_in(session):
        return redirect('/')
    return render_template('edit.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return redirect('/')
        else:
            return render_template('login.html')

    # Get values passed via POST
    username = request.form.get('username')
    password = request.form.get('password')

    if 'ret_path' in session:
        ret_path = session['ret_path']
        del session['ret_path']
    else:
        ret_path = '/'

    if util.accounts.auth_user(username, password):
        util.accounts.login_user(session, username)
        return redirect(ret_path)
    else:
        flash('Bad username or password')
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return redirect('/')
        else:
            return render_template('signup.html')

    # Get values passed via POST
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if util.accounts.user_exists(username):
        flash('Username already taken')
        return render_template('signup.html')
    elif password != confirm:
        flash('Passwords do not match')
        return render_template('signup.html')
    else:
        util.accounts.add_user(username, password)
        util.accounts.login_user(session, username)
        return redirect('/')


@app.route('/logout')
def logout():
    util.accounts.logout_user(session)
    return redirect('/')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return render_template('create_v1.html')
        else:
            # Set return path back here
            session['ret_path'] = '/create'
            return redirect('/login')

    # Get values passed via POST
    title = request.form.get('title')
    content = request.form.get('content')
    author = util.accounts.get_logged_in_user(session)

    post = util.posts.create_post(title, content, author)
    return redirect('/post?p={post}'.format(post=post))


@app.route('/post')
def post():
    # Get values passed via GET
    post = request.args.get('p')
    title, content, author = util.posts.get_post(post)
    content = util.posts.render_post(content)
    return render_template(
            'post.html',
            title=title,
            content=content,
            author=author
    )


@app.route('/<author>')
def author(author):
    # Get values passed via GET
    ids = util.posts.get_author_posts(author)
    def get_post(post_id):
        print(util.posts.get_post(post_id))
        return util.posts.get_post(post_id)
    return render_template(
            'post_mult.html',
            ids=ids,
            get_post = get_post
    )

@app.route('/home')
def home():
    # Get values passed via GET
    ids = util.posts.get_all_posts()
    def get_post(post_id):
        print(util.posts.get_post(post_id))
        return util.posts.get_post(post_id)
    return render_template(
            'post_mult.html',
            ids=ids,
            get_post = get_post
    )


if __name__ == '__main__':
    util.posts.create_table()
    util.accounts.create_table()
    app.debug = True  # Set to `False` before release
    app.run()

