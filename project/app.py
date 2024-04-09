from flask import Flask, flash, render_template, request, redirect, url_for
from config import Config
from Database.database_setup import Message, db, User, Channel, UserChannel
from channel_management import create_channel, delete_channel
from utils import get_current_user_id, is_user_channel_admin
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms import ChannelForm, MessageForm, RegisterForm, LoginForm

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    # user can be accessed anywhere with current_user
    # for example the username can be accessed with {{ current_user.username }}
    # {% if current_user.is_authenticated %} ... {% endif %} can be used to run only if logged in
    return db.get_or_404(User, user_id)

@app.route("/")
def root():
    return redirect("/home")

@app.route("/index")
def index():
    return redirect("/home")

@app.route("/friendspage")
def Friendspage():
    return render_template("Friendspage.html")

@app.route("/channels", methods=["GET"])
@login_required
def channels():
    channelForm = ChannelForm()
    channel_id = request.args.get("channel_id")
    channels_query = db.session.query(Channel).order_by(Channel.id)
    if channel_id is None:
        channel_id = 0
    elif(not channel_id.isnumeric()):
        channel_id = 0
        flash("Invalid Channel ID")
    else:
        channel = channels_query.filter_by(id=channel_id).first()
        if not channel:
            flash("No channel with that ID")
            channel_id = 0
        return redirect(url_for("message") + "?channel_id=" + str(channel_id))

    return render_template("Channels-Page.html", channelform=channelForm, channel_id=channel_id, channels_query=channels_query)

@app.route("/message", methods=["GET"])
@login_required
def message():
    messageForm = MessageForm()
    channel_id = request.args.get("channel_id")
    channels_query = db.session.query(Channel).order_by(Channel.id)
    if channel_id is None or not channel_id.isnumeric():
        return redirect(url_for("channels"))
    else:
        channel = channels_query.filter_by(id=channel_id).first()
        messages = db.session.query(Message).filter_by(channel=channel).all()
        if not channel:
            flash("No channel with that ID")
            return redirect(url_for("channels"))

    return render_template("message.html", channel=channel, messages=messages, messageform=messageForm)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    regForm = RegisterForm()
    logForm = LoginForm()

    if request.method == "POST" and logForm.validate_on_submit():
        # flash(logForm.validate_on_submit().__repr__())
        # flash(logForm.validate_on_submit.__repr__())
        # user = db.session.execute(db.select(User).filter_by(username=logForm.username.data).first())
        username=logForm.username.data
        user = db.session.query(User).filter_by(username=username).first()
        if user and user.check_password(logForm.password.data):
            login_user(user)
            flash("Logged In!")
            # next = request.args.get('next')
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # See Django's url_has_allowed_host_and_scheme for an example.
            # TODO: Implement this to validate the URL
            # if not url_has_allowed_host_and_scheme(next, request.host):
            #     return abort(400)

            return redirect(url_for("home", username=username))
        else:
            # Redirect back to login page with an error message
            flash("Incorrect username or password")
            return render_template("login.html", title="Login/Register", regform=regForm, logform=logForm, error="Invalid username or password")

    # For GET requests, just render the login page
    return render_template("login.html", title="Login/Register", regform=regForm, logform=logForm)

@app.route("/register", methods=["GET", "POST"])
def register():
    logForm = LoginForm()
    regForm = RegisterForm()
    if request.method == "POST" and regForm.validate_on_submit():
        # flash(regForm.validate_on_submit().__repr__())
        username = regForm.username.data
        user = User(username=username)
        user.set_password(regForm.password.data)
        if not db.session.query(User).filter_by(username=username).first():
            db.session.add(user)
            db.session.commit()
            flash("Registered Successfully!")
            return redirect(url_for("login"))
        else:
            flash("Username already in use")
            return render_template("login.html", title="Login/Register", regform=regForm, logform=logForm)

    # For GET requests, redirect to login page
    # return redirect(url_for("login"))
    return render_template("login.html", title="Login/Register", regform=regForm, logform=logForm)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.")
    return redirect(url_for("index"))

@app.route("/user")
# @login_required
def user():
    return render_template("user.html")

# ******************************************************
# PLACEHOLDER CODE /create_channel IS NOT CREATED YET
# TODO: Create Channel page and/or directory
# ******************************************************
@app.route("/create_channel", methods=["POST"])
@login_required
def create_channel_route():
    channelForm = ChannelForm()
    # flash(str(channelForm.validate_on_submit()))
    if request.method == "POST" and channelForm.validate_on_submit():
        channel_name = request.form["channel_name"]
        # user_id = get_current_user_id()  # Implement this to get current user ID
        user_id = current_user.get_id()
        # flash(user_id)

        # Create the channel
        channel = create_channel(user_id, channel_name)
        
        # Redirect to channel page or wherever appropriate
        return redirect(url_for("channels", channel_id=channel.id))

    # Handle GET requests or other cases
    return redirect(url_for("index"))

# ****************************************************
# PLACEHOLDER CODE /delete_channel IS NOT CREATED YET
# TODO: Delete Channel page and/or directory
# ****************************************************
@app.route("/delete_channel/", methods=["POST"])
def delete_channel_route():
    if request.method == "POST":
        channel_id = request.form["del_channel_id"]
        channel = db.session.query(Channel).filter_by(id=channel_id).first();
        if channel:
            # Ensure the current user is an admin of the channel or handle permissions as needed
            user_channel = db.session.query(UserChannel).filter_by(user_id=current_user.get_id()).first(); 
            if is_user_channel_admin(current_user.get_id(), channel_id, user_channel):
                # Delete the channel
                if delete_channel(channel_id):
                    flash("\"" + channel.channel_name + "\" channel successfully deleted.")
                    return redirect(url_for("channels"))  # Redirect after successful deletion
                else:
                    flash("Deletion error.")
                    return redirect(url_for("channels"))  # Redirect after successful deletion
            else:
                flash("Permision Denied.")
                return redirect(url_for("channels") + "?channel_id=" + channel_id)  # Redirect after successful deletion
        else:
            flash("Channel not found.")
            return redirect(url_for("channels"))  # Redirect after successful deletion

    # Handle other HTTP methods if needed
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
