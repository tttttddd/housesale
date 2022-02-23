# encoding:utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import Deal, House, NormalUser, Reserve, User, Agent, HouseOwner, VipUser
from exts import db
from decorators import login_required
from datetime import datetime
from snowflake import get_random_id
from time import strftime, localtime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/user_index', methods=['GET'])
@login_required
def user_index():
    dict = {"name": session.get("name")}
    return render_template('user_index.html', dict=dict)


@app.route('/house_owner_index', methods=['GET'])
@login_required
def house_owner_index():
    dict = {"name": session.get("name")}
    return render_template('index_of_house_owner.html', dict=dict)


@app.route('/agent_index', methods=['GET'])
@login_required
def agent_index():
    dict = {"name": session.get("name")}
    return render_template('index_of_agent.html', dict=dict)


@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/login_user', methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        return render_template('login_user.html')
    else:
        account = request.form['account']  # 界面传值
        password = request.form['password']  # 界面传值
        if (len(account) == 0 | len(password) == 0):
            return render_template('login_user.html')

        exist = User.query.filter(User.account == account, User.user_password == password).first()

        if exist:
            session['name'] = exist.name
            session['id'] = str(exist.id)
            session['user_id'] = str(exist.user_id)
            session['account'] = account
            return redirect(url_for('user_index'))
        else:
            return u'账号或者密码错误，请确认后再登录！'


@app.route('/login_agent', methods=['POST', 'GET'])
def login_agent():
    if request.method == 'GET':
        return render_template('login_agent.html')
    else:
        account = request.form['account']  # 界面传值
        password = request.form['password']  # 界面传值
        if (len(account) == 0 | len(password) == 0):
            return render_template('login_agent.html')

        exist = Agent.query.filter(Agent.agent_account == account, Agent.agent_password == password).first()

        if exist:
            session['name'] = exist.agent_name
            session['agent_id'] = str(exist.agent_id)
            session['account'] = account
            return redirect(url_for('agent_index'))
        else:
            return u'账号或者密码错误，请确认后再登录！'


@app.route('/login_house_owner', methods=['POST', 'GET'])
def login_house_owner():
    if request.method == 'GET':
        return render_template('login_house_owner.html')
    else:
        account = request.form['account']  # 界面传值
        password = request.form['password']  # 界面传值
        if (len(account) == 0 | len(password) == 0):
            return render_template('login_house_owner.html')

        exist = HouseOwner.query.filter(HouseOwner.house_owner_account == account,
                                        HouseOwner.house_owner_password == password).first()

        if exist:
            session['name'] = exist.house_owner_name
            session['house_owner_id'] = str(exist.house_owner_id)
            session['account'] = account
            return redirect(url_for('house_owner_index'))
        else:
            return u'账号或者密码错误，请确认后再登录！'


@app.route('/regist', methods=['GET'])  # 表单提交
def regist():
    if request.method == 'GET':
        return render_template('regist.html')


@app.route('/regist_user', methods=['GET', 'POST'])
def regist_user():
    if request.method == 'GET':
        return render_template('regist_user.html')
    else:
        username = request.form.get('name')
        account = request.form.get('account')
        password = request.form.get('password')
        age = request.form.get('age')
        exist = User.query.filter(User.account == account).first()
        if exist:
            return u'此账号已被注册'
        else:
            # 可以进行注册
            id = get_random_id()
            user_id = get_random_id()
            user = User(
                name=username,
                id=id,
                user_id=user_id,
                account=account,
                regist_date=strftime("%Y-%m-%d %H:%M:%S", localtime()),
                user_password=password,
                property_level=1,
                sex='F',
                age=age
            )
            normal_user = NormalUser(
                id=id,
                user_id=user_id,
            )
            # 添加到数据库中
            db.session.add(user)
            db.session.add(normal_user)
            # 进行事务提交
            db.session.commit()
            # 如果注册成功，页面跳转到登录界面
            return redirect(url_for('login_user'))


@app.route('/regist_agent', methods=['GET', 'POST'])
def regist_agent():
    if request.method == 'GET':
        return render_template('regist_agent.html')
    else:
        username = request.form.get('name')
        account = request.form.get('account')
        password = request.form.get('password')

        exist = Agent.query.filter(Agent.agent_account == account).first()
        if exist:
            return u'此账号已被注册'
        else:
            # 可以进行注册
            agent_id = get_random_id()
            agent = Agent(
                agent_name=username,
                agent_id=agent_id,
                agent_account=account,
                agent_password=password,
            )
            # 添加到数据库中
            db.session.add(agent)
            # 进行事务提交
            db.session.commit()
            # 如果注册成功，页面跳转到登录界面
            return redirect(url_for('login_agent'))


@app.route('/regist_house_owner', methods=['GET', 'POST'])
def regist_house_owner():
    if request.method == 'GET':
        return render_template('regist_house_owner.html')
    else:
        username = request.form.get('name')
        account = request.form.get('account')
        password = request.form.get('password')

        exist = HouseOwner.query.filter(HouseOwner.house_owner_account == account).first()
        if exist:
            return u'此账号已被注册'
        else:
            # 可以进行注册
            house_owner_id = get_random_id()
            house_owner = HouseOwner(
                house_owner_name=username,
                house_owner_id=house_owner_id,
                house_owner_account=account,
                house_owner_password=password,
            )
            # 添加到数据库中
            db.session.add(house_owner)
            # 进行事务提交
            db.session.commit()
            # 如果注册成功，页面跳转到登录界面
            return redirect(url_for('login_house_owner'))


@app.route('/reserve', methods=['POST', 'GET'])
@login_required
def reserve():
    if request.method == 'GET':
        return render_template('reserve.html')
    else:
        reserve_user_name = request.form.get('reserve_user')
        house_name = request.form.get('house_name')
        date = request.form.get('date')
        reserve_id = get_random_id()
        agent_id = session['agent_id']

        reserve_user_id = User.query.filter(User.name == reserve_user_name).first().id
        house_id = House.query.filter(House.house_name == house_name).first().house_id

        reserve = Reserve(
            resever_id=reserve_id,
            house_id=house_id,
            agent_id=agent_id,
            id=reserve_user_id,
            watch_time=date,
        )

        db.session.add(reserve)
        db.session.commit()

        return redirect(url_for('agent_index'))


@app.route('/deal', methods=['POST', 'GET'])
@login_required
def deal():
    if request.method == 'GET':
        return render_template('deal.html')
    else:
        buy_user_name = request.form.get('buy_user')
        house_name = request.form.get('house_name')
        prices = request.form.get('prices')
        deal_id = get_random_id()
        agent_id = session['agent_id']

        buy_user_id = User.query.filter(User.name == buy_user_name).first().id
        house_id = House.query.filter(House.house_name == house_name).first().house_id
        print("house_id: ", house_id)
        exist = Deal.query.filter(Deal.house_id == house_id).first()
        print("exist: ", exist)
        if exist:
            return u'该房子已被交易'
        else:
            deal = Deal(
                deal_id=deal_id,
                house_id=house_id,
                id=buy_user_id,
                agent_id=agent_id,
                deal_prices=prices
            )

            # house = House.query.filter(House.house_id == house_id).first()
            # db.session.delete(house)
            # house.sold_date = strftime("%Y-%m-%d %H:%M:%S", localtime())
            # db.session.add(house)
            db.session.add(deal)
            db.session.commit()
            return redirect(url_for('agent_index'))


@app.route('/add_house', methods=['GET', 'POST'])
@login_required
def add_house():
    if request.method == 'GET':
        return render_template('insert_house.html')
    else:
        house_name = request.form.get('name')
        house_id = get_random_id()
        house_owner_id = session['house_owner_id']
        add_date = strftime("%Y-%m-%d %H:%M:%S", localtime())
        province = request.form.get('province')
        city = request.form.get('city')
        area = request.form.get('area')
        address = request.form.get('address')
        acreage = request.form.get('acreage')
        prices = request.form.get('prices')
        prices_per_square = int(prices) / float(acreage)

        house = House(
            house_name=house_name,
            house_id=house_id,
            house_owner_id=house_owner_id,
            add_date=add_date,
            province=province,
            city=city,
            area=area,
            address=address,
            acreage=acreage,
            prices=prices,
            price_per_square=prices_per_square,
        )

        db.session.add(house)
        db.session.commit()
        return redirect(url_for('house_owner_index'))


@app.route('/show_my_house', methods=['GET'])
@login_required
def show_my_hosue():
    houses = House.query.filter_by(house_owner_id=session['house_owner_id'])
    dict = {'houses': houses}
    return render_template("Myhouse.html", dict=dict)


@app.route('/look_for_house', methods=['GET', 'POST'])
@login_required
def look_for_house():
    if request.method == 'GET':
        return render_template('look_for_house.html')
    else:
        filter = House.query
        province = request.form.get('province')
        if province != "":
            filter = filter.filter_by(province=province)
        city = request.form.get('city')
        if city != "":
            filter = filter.filter_by(city=city)
        area = request.form.get('area')
        if area != "":
            filter = filter.filter_by(area=area)
        acreage_min = request.form.get('acreage_min')
        acreage_max = request.form.get('acreage_max')
        if acreage_min != "" and acreage_max != "":
            min = int(acreage_min)
            max = int(acreage_max)
            if min <= max:
                filter = filter.filter(House.acreage > min)
                filter = filter.filter(House.acreage < max)

        prices_min = request.form.get('prices_min')
        prices_max = request.form.get('prices_max')
        if prices_min != "" and prices_max != "":
            min = int(prices_min)
            max = int(prices_max)
            if min <= max:
                filter = filter.filter(House.prices > min)
                filter = filter.filter(House.prices < max)

        houses = filter.all()
        dict = {'houses': houses}
        return render_template('result_house_search.html', dict=dict)


@app.route('/look_for_agent', methods=['GET', 'POST'])
@login_required
def look_for_agent():
    if request.method == 'GET':
        return render_template('look_for_agent.html')
    else:
        agent_name = request.form.get('name')
        agents = Agent.query.filter(Agent.agent_name.contains(agent_name)).all()
        dict = {'agents': agents}
        return render_template('result_agent_search.html', dict=dict)


@app.route('/show_all_deal', methods=['GET'])
@login_required
def show_all_deal():
    deals = Deal.query.filter(Deal.agent_id == session['agent_id']).all()
    deals_list = []
    for deal in deals:
        d = {}
        house = House.query.filter(House.house_id == deal.house_id).first()
        d['house_name'] = house.house_name
        d['acreage'] = house.acreage
        d['prices'] = deal.deal_prices
        d['province'] = house.province
        d['city'] = house.city
        d['area'] = house.area
        d['address'] = house.address
        deals_list.append(d)

    dict = {"deals": deals_list}

    return render_template('show_all_deal.html', dict=dict)


@app.route('/show_all_reserve', methods=['GET'])
@login_required
def show_all_reserve():
    reserves = Reserve.query.filter(Reserve.agent_id == session['agent_id']).all()
    reserve_list = []
    for reserve in reserves:
        r = {}
        house = House.query.filter(House.house_id == reserve.house_id).first()
        user = User.query.filter(User.id == reserve.id).first()
        r['house_name'] = house.house_name
        r['acreage'] = house.acreage
        r['province'] = house.province
        r['city'] = house.city
        r['area'] = house.area
        r['address'] = house.address
        r['name'] = user.name
        reserve_list.append(r)

    dict = {'reserves': reserve_list}
    return render_template('show_all_reserve.html', dict=dict)


@app.route('/logout', methods=['GET'])
def logout():
    try:
        del session['account']
        del session['name']
        del session['user_id']
        del session['id']
        del session['agent_id']
        del session['house_owner_id']
    except:
        pass
    return redirect(url_for('login'))


@app.route('/pay', methods=['GET', 'POST'])
@login_required
def pay():
    if request.method == 'GET':
        return render_template('pay.html')
    else:
        money_num = request.form.get('prices')
        id = session['id']
        vip_id = get_random_id()

        vip_user = VipUser(money_num)

        return redirect(url_for('user_index'))


if __name__ == "__main__":
    app.run(debug=True)
