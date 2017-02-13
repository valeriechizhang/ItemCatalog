from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import session as login_session
import random, string

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')


#API endpoints
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    return jsonify(MenuItem=item.serialize)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['restaurant_name'])
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant [%s] Created' % newRestaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['restaurant_name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant [%s] Successfully Edited" % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant [%s] Successfully Deleted" % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['item_name'],
                            price = request.form['item_price'],
                            description = request.form['item_description'],
                            restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('Menu Item [%s] Created' % newItem.name)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    if request.method == 'POST':
        item.name = request.form['item_name']
        item.price = request.form['item_price']
        item.description = request.form['item_description']
        session.add(item)
        session.commit()
        flash('Menu Item [%s] Edited' % item.name)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu Item [%s] Deleted' % item.name)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, item = item)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

















