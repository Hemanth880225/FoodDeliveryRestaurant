import os, secrets
from statistics import quantiles

from PIL import Image
from foodMenuWebsite import  app, db , bcrypt
from flask import  render_template, request,redirect, url_for, flash, abort
from foodMenuWebsite.forms import LoginForm, RegisterForm, UpdateAccountForm, PostForm, OrderForm , UpdateOrderStatusForm
from flask_login import login_user, logout_user, login_required, current_user
from foodMenuWebsite.models import User, Post, Order, Cart, MenuItem, OrderItem


@app.route("/")
@app.route('/home')
def home():
    return render_template("home.html", title="Home")

@app.route('/menu')
def menu():
    items = MenuItem.query.all()
    return render_template("menu.html", title="Menu", items=items)

@app.route('/About/Story')
def about():
    return render_template("about.html", title="About")

@app.route('/Contact')
def contact():
    return render_template("contact.html", title="Contact")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(first_name= form.first_name.data,last_name= form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user , remember=form.remember.data)
            flash("Login successful. You are now logged in", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Failed, Check email and password", 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # output_size = (125, 125)
    # im = Image.open(form_picture)
    # im.thumbnail(output_size)
    # im.save(picture_path)

    form_picture.save(picture_path)

    return picture_fn




@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name  = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file or "default.jpg")
    return render_template('account.html', title='Account', form=form, image_file=image_file)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data , content=form.content.data,details=form.details.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('all_posts'))
    return render_template('create_post.html', title='New Post', form=form , legend='Create Post')

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def all_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('all_posts.html', title='All Posts', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('single_post.html', title = post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
       post.title = form.title.data
       post.content = form.content.data
       post.author = current_user
       db.session.commit()
       flash('Your post has been updated!', 'success')
       return redirect(url_for('all_posts', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend = 'Update Post')

@app.route('/post/<int:post_id>/delete' , methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('all_posts'))


@app.route('/order/item/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_item(order_id):
     menu_item = MenuItem.query.get_or_404(order_id)
     form = OrderForm()

     if form.validate_on_submit():
         quantity = form.quantity.data
         total_price = menu_item.price * quantity

         new_order = Order(user_id=current_user.id, total_price= total_price)
         db.session.add(new_order)
         db.session.commit()

         order_item = OrderItem(order_id = new_order.id, menu_item_id = menu_item.id, quantity = quantity)
         db.session.add(order_item)
         db.session.commit()

         flash(f"Your order for {menu_item.name} has been placed successfully!", "success")
         return redirect(url_for('menu'))
     return render_template('place_order.html', form=form , menu_item=menu_item)

@app.route('/cart' , methods=['GET', 'POST'])
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).order_by(Cart.added_on.desc()).all()
    total = sum(item.menu_item.price * item.quantity for item in cart_items)

    return render_template('cart.html', title='My Cart', cart_items=cart_items, total = total)

@app.route('/cart/add/<int:menu_item_id>', methods=['POST'])
@login_required
def add_to_cart(menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)

    existing_item = Cart.query.filter_by(user_id = current_user.id, menu_item_id = menu_item.id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_cart_item = Cart(user_id = current_user.id, menu_item_id = menu_item.id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    flash(f"{menu_item.name} added to your cart!", "success")
    return redirect(url_for('view_cart'))

@app.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    new_quantity = int(request.form.get('quantity' , 1))
    if new_quantity < 1:
        db.session.delete(cart_item)
        flash(f"{cart_item.menu_item.name} removed (quantity set to 0).", "info")
    else:
        cart_item.quantity = new_quantity
        flash(f"{cart_item.menu_item.name} quantity updated to {new_quantity}.", "success")

    db.session.commit()
    return redirect(url_for('view_cart'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    db.session.delete(cart_item)
    db.session.commit()
    flash(f"{cart_item.menu_item.name} removed from your cart.", "info")
    return redirect(url_for('view_cart'))


@app.route('/owner/orders')
@login_required
def owner_orders():

    if not current_user.is_owner:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('home'))

    orders = Order.query.order_by(Order.date_ordered.desc()).all()
    return render_template('owner_orders.html', orders=orders)


@app.route('/owner/orders/<int:order_id>/update', methods = ['GET', 'POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_owner:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('home'))

    order = Order.query.get_or_404(order_id)
    form = UpdateOrderStatusForm()

    if form.validate_on_submit():
        order.status = form.status.data
        db.session.commit()
        flash(f"Order #{order.id} status updated to '{order.status}'.", "success")
        return redirect(url_for('owner_orders'))

    form.status.data = order.status
    return render_template('update_order_status.html', form=form, order = order)

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id = current_user.id).order_by(Order.date_ordered.desc()).all()
    return render_template('orders.html', title='My Orders', orders=user_orders)

@app.route('/orders/view/<int:order_id>', methods=['GET', 'POST'])
@login_required
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.customer != current_user and not current_user.is_owner:
        abort(403)
    if current_user.is_owner:
        return redirect(url_for('owner_orders'))
    order_items = OrderItem.query.filter_by(order_id=order.id).order_by(OrderItem.id.desc()).all()
    return render_template('orders.html', order=order, orders=orders)

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():

    cart_items = Cart.query.filter_by(user_id = current_user.id).all()

    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('view_cart'))

    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)

    new_order = Order(user_id = current_user.id, total_price = total_price, status='Pending')
    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(order_id = new_order.id, menu_item_id = item.menu_item_id, quantity = item.quantity)
        db.session.add(order_item)
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    flash("Order placed successfully! 🎉", "success")
    return redirect(url_for('orders'))

