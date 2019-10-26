#python web main
#版本：测试1.0

from flask import *
import mysql.connector
import os
import time

# 初始化内容
app = Flask(__name__, template_folder='templates')
def start_server():
    global app
    app.config.from_object('config')

    #数据库配置部分
    app.config['DATA_BASE'] = 'test'
    app.config['USER'] = 'root'
    app.config['PASSWORD']='**************'

    #路径及ip配置
    app.config['WEB_URL']='http://127.0.0.1:5000/'    #这是测试的目标机ip
    app.config['AIM_DIR']='static/things_inf_pic'#存储文件名
    app.config['BASE_DIR']=os.path.abspath(os.path.dirname(__file__)) #当前项目绝对位置
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['FILE_DIR'] = os.path.join(app.config['BASE_DIR'], app.config['AIM_DIR'])  # 图片存储文件夹地址
    global user_log_number  #累计用户登录次数（服务器开机算起）
    user_log_number=0
    global server_start_time
    server_start_time = time.time() #开机时间  秒形
    global data_being
    data_being = Data() #生成常驻数据模型 data_being
    data_being.start()    #初始化填充数据

#辅助函数部分
    #..时间转化函数 返回列表 年月日时分秒 length=6
    #..传入str或者int类型
def time_list(t):
    t=int(t)
    t_c=time.localtime(t)
    return [t_c[0],t_c[1],t_c[2],t_c[3],t_c[4],t_c[5]]

    #..主界面的填充函数  带入目标list元组与recommend列表  查数据库并返回字典数据
        #...带入字典结构 ： ｛’list‘：列表，‘recommend’：目标页元组｝
        #...返回的字典结构：
            #   {'list':{"1":[picture_url,direct_url,
            # type,title,simplefy_description,log_name
            # ,release_time,write_number,see_number,place,type_class],"2":[list_2]}
            #, 'recommend':{'1':[picture_url,title,direct_url]}
            #  }
def session_get(name):     #必须是个字符串带入
    try:
        if session.get(name)==None:
            return ''
        else:
            return session.get(name)
    except:
        return ""


def insert_for_main(dict):
    dbc=SQLconnector()
    result_dict={'list':{},'recommend':{}}
    list=dict['list']    #这是一个10位列表
    list_for_recommend=dict['recommend']   #这是一个七位列表
    #..循环装载list

    for k in ['1','2','3','4','5','6','7','8','9','10']:
        id=list[int(k)-1]   #id是个int 型
        picturename=dbc.run('select picture_name from things_inf where id='+"'"+str(id)+"'")[0][0]
        picture_url='/static/things_inf_pic/'+picturename
        direct_url=app.config['WEB_URL']+'things/'+str(id)
        data_list=dbc.run('select title,type,description,user_name,see_number,release_time,place from things_inf where id='+"'"+str(id)+"'")[0]
        title=data_list[0]
        if data_list[1]=='lost':
            type='失物'
            type_class="danger"
        else:
            type='招领'
            type_class = "dark"
        description=data_list[2]
        user_name=data_list[3]
        see_number=data_list[4]

        a_time=time_list(data_list[5])
        b_time=[]
        for i in a_time:
            b_time.append(str(i))
        release_time=b_time[0]+'/'+b_time[1]+'/'+b_time[2]+' '+b_time[3]+':'+b_time[4]+':'+b_time[5]

        place=data_list[6]
        write_number=0         #未加入评论功能    先设置为0
        log_name=dbc.run('select log_name from user_inf where user_name='+"'"+user_name+"'")[0][0]
        #...简化长度的description
        if len(description)>100:
            simplefy_description=description[0:101]
        else:
            simplefy_description=description

            result_dict['list'][k]=[picture_url,direct_url, type,title,simplefy_description,log_name,release_time,write_number,see_number,place,type_class]

    #..for循环装载recommend
    for m in ['1', '2', '3', '4', '5', '6', '7']:
        r_id=str(list_for_recommend[int(m)-1])

        n=dbc.run('select picture_name,title from things_inf where id='+"'"+r_id+"'")
        print(n)
        r_picture_url='/static/things_inf_pic/'+n[0][0]
        r_title=n[0][1]
        r_direct_url=app.config['WEB_URL']+'things/'+r_id
        result_dict['recommend'][m]=[r_picture_url,r_title,r_direct_url]
    return result_dict

def returener_for_start(page):    #输入一个int型的值
    page = str(page)
    max_page=int(data_being.max/10)# 可能出现空白页
    # 需要填充：  开始界面推荐图    最后的最近的公告图（常驻数据图，时时更新）
    if int(page) < 5:
        recommend = data_being.main_recommend  # 私有化取数据
        list = data_being.main_list[int(page)-1]
        print({"recommend": recommend, "list": list})
        dict = insert_for_main({"recommend": recommend, "list": list})  # 这里是利用私有化数据 在数据库取数据 放入dict
        return render_template('main.html', dict=dict, page=page, max_page=max_page)
    else:
        if (int(page))*10>data_being.max:
            return 'error-out-range' #测试使用
        max=int(data_being.max-(int(page)-1)*10)
        list=[]
        list_before=[max,max-1,max-2,max-3,max-4,max-5,max-6,max-7,max-8,max-9]
        for m in list_before:
            list.append(str(m))
        recommend=data_being.main_recommend
        dict=insert_for_main({'recommend':recommend,'list':list})
        return render_template('main.html',dict=dict,page=page,max_page=max_page)

def get(str):
    m=request.form.get(str)
    try:
        if m==None:
            return ""
        else:
            return m
    except:
        return ''

@app.route('/login/<traceback_url>',methods=['GET','POST'])  #traceback用于在导航登录以后回到原来
def login(traceback_url):
    #功能：1验证登录 post方法 2.导航栏：登录/用户  get

    global user_log_number  #记录历史登录
    if request.method=='POST':
        dbc = SQLconnector()
        user_name=get('user_name')
        password=get('password')
        sqlstr = 'select password from user_inf where user_name=' + user_name
        #测试 当没有此username的情况
        if dbc.run(sqlstr)[0][0]==password:
            if request.form.get('remember')=='on':
                session.permanent=True
            session['user_state'] = True
            print(request.form.get('remember'))
            user_log_number+=1    #用户记录
            session['user_name']=user_name
            #return redirect(url_for(traceback_url))
            return render_template('login.html',dict={"traceback_url":traceback_url,"state":"success"})
        else:
            return "登录失败"    #此处为测试  以后使用闪现优化 返回错误
    else:
        #get 方法
        dict={}
        dict['state']='no'
        dict['traceback_url']=traceback_url
        print("url是"+traceback_url)
        if session.get('user_state')==None:
            return render_template('login.html',dict=dict)  #回溯机制写在log.html模版中 post到log/traceback
        else:
            return redirect('/user')

@app.route('/for_login/<traceback_url>',methods=['POST','GET'])
def for_login(traceback_url):
    global user_log_number  # 记录历史登录
    if request.method == 'POST':
        dbc = SQLconnector()
        user_name = get('user_name')
        password = get('password')
        sqlstr = 'select password from user_inf where user_name=' + user_name
        # 测试 当没有此username的情况
        if dbc.run(sqlstr)[0][0] == password:
            if request.form.get('remember') == 'on':
                session.permanent = True
            session['user_state'] = True
            print(request.form.get('remember'))
            user_log_number += 1  # 用户记录
            session['user_name'] = user_name
            return render_template('login.html',dict={"traceback_url":traceback_url,"state":"success"})
        #验证针对多层url things/2的回溯
        else:
            return render_template('login.html',dict={'state':'fail','traceback_url':traceback_url})




@app.route('/<int:page>')
def start_more(page):
    return returener_for_start(page)

@app.route('/')
def start():
    return returener_for_start('1')


#验证是否是本人url

@app.route('/user/<user_name>')
def user(user_name):
    #自己的界面
    if user_name==session.get['user_name']:
        dict={}
        pass
    #别人的界面
    else:
        dict={}
        #dict的装载部分




        return render_template("user.html",dict=dict)

@app.route("/release_after_login")
def release_after_login():
    dbc=SQLconnector()
    session['dict']['log_name']=dbc.run('select log_name from user_inf where user_name='+"'"+session.get('user_name')+"'")[0][0]
    session['dict']['user_url']='/user/'+session.get('user_name')
    session['dict']['login_state']='yes'
    return render_template('fabu_after_login.html',dict=session['dict'])

#request对象的一些特点：
#取form一定要用form.get（）才会返回字符串  不存在返回None  无值返回空串
@app.route('/release',methods=['POST','GET'])
def release():
    dbc=SQLconnector()
    if request.method=='GET':
        if session.get("user_state")!=True:
            dict={'login_state':'no','log_name':'未登录','user_url':'/login/release'}
            return render_template('fabu.html',dict=dict)
        else:
            user_name = session.get('user_name')
            log_name=dbc.run('select log_name from user_inf where user_name='+"'"+user_name+"'")[0][0]
            dict = {'login_state':'yes','log_name':log_name,'user_url':'/user/'+user_name}
            return render_template('fabu.html',dict=dict)
    else:
        if session.get("user_state")!=True:
            list=['form_title','type','place','object_name','connect_way','phone_number','month','day','description']
            session['dict']={}
            for i in list:
                session['dict'][i] = get(i)
            return render_template('login.html',dict={'state':'release_after_login','traceback_url':'release_after_login'})    #测试使用 一般情况不会跳转到此处
        else:
            #数据库存储部分
            user_name=session.get('user_name')

            # ..提交限制 一天只能提交一次
            lastest_time = dbc.run("select max(release_time) from things_inf where user_name=" + "'" + user_name + "'")
            if int(lastest_time[0][0]) - int(time.time()) < 86400:
                write_time = 86400 - int(lastest_time[0][0]) + time.time()
                return "发布失败 还需要等待" + str(write_time)[0:5] + 's'




            release_time=str(int(time.time()))#此处需要修改
            form_type=get("type")
                #..合法性验证
            try:
                file_dir=app.config['FILE_DIR']
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                f = request.files.get('picture')
                print(f)
                if f and ('.' in f.filename and f.filename.split('.', 1)[1] in set(['jpeg','JPEG','png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])):
                    fname = f.filename
                    ext = fname.split('.', 1)[1]  # 获取文件后缀
                    unix_time = int(time.time())
                    new_filename = str(unix_time)+ user_name + '.' + ext  # 修改文件名
                    f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
                    picture_name = new_filename
                else:
                    raise ValueError

            except :
                picture_name = 'no_pic.png'


            time_m=str(time_list(int(time.time()))[0])+'-'+get('month')+'-'+get('day')
            sqlstr="insert into things_inf (release_time,title,name,user_name,contact_way,description,phone_number,place,picture_name,type,time) values (" \
                   +"'"+release_time+"'"\
                   +","+"'"+get("form_title")+"'"\
                   +","+"'"+get("object_name")+"'"\
                   +","+"'"+user_name+"'"\
                   +","+"'"+get("connect_way")+"'"\
                   +","+"'"+get("description")+"'"\
                   +","+"'"+get("phone_number")+"'"\
                   +","+"'"+get("place")+"'"\
                   +","+"'"+picture_name+"'"\
                   +","+"'"+form_type+"'" \
                   +","+"'"+time_m+"'" \
                   +")"

                #..插入数据测试 sql语句
            print(sqlstr)

                #..执行插入数据
            dbc.insert(sqlstr)


            #常驻数据更新部分
            data_being.update_list()


            #重定向部分
            return redirect('/things/'+str(data_being.max))    #此html  显示 提交成功   返回主页功能
#某物界面


@app.route('/things/<id>')    #带入的id是个str
def things(id):
    #..初始化
    id=str(id)
    dbc=SQLconnector()
    dict={}
    #..浏览次数增加函数
    the_last_see_number=int(dbc.run("select see_number from things_inf where id="+"'"+id+"'")[0][0])
    dbc.insert("update things_inf set see_number="+"'"+str(the_last_see_number+1)+"'"+"where id="+"'"+id+"'" )
    data_list=dbc.run('select * from things_inf where id='+"'"+id+"'")[0]
    if data_list[0]=='':
        return "找不到这条信息，返回原界面"

    else:
        # ..字典数据准备
            # ...结构    {head_picture_url,log_name,picture_url ,list for the main information}
            #...一下的结果全为字符串
        time_a=time_list(data_list[1])
        time_b=[]
        for m in time_a:
            time_b.append(str(m))
            #str 型
        release_time=time_b[0]+"-"+time_b[1]+"-"+time_b[2]+' '+time_b[3]+":"+time_b[4]+":"+time_b[5]
        title=data_list[2]
        name=data_list[3]
        user_name=data_list[4]
        contact_way=data_list[5]
        description=data_list[6]
        place=data_list[8]
        picture_name=data_list[9]
        type=data_list[10]
        see_number=str(the_last_see_number+1)

        # 注意：评论 默认是个字符串型的空字典
        write_dict=eval(data_list[13])
        write_number=len(write_dict)
        time=data_list[14]
        log_name=dbc.run("select log_name from user_inf where user_name="+"'"+user_name+"'")[0][0]
        picture_url='/static/things_inf_pic/'+picture_name
        #!!!!!扩展部分:操作write——dict 查询评论数据 并装入新的字典  最后放入主字典   1.0bate版本不支持

        #...字典装载
        dict["release_time"]=release_time
        dict["title"]=title
        dict["name"]=name
        dict["contact_way"]=contact_way
        dict["description"]=description
        dict["place"]=place
        dict["picture_url"]=picture_url
        dict["type"]=type
        dict["see_number"]=see_number
        dict["log_name"]=log_name
        dict["write_dict"]=write_dict
        dict["write_number"]=write_number
        dict["time"]=time
        dict['user_url']="/user/"+dbc.run('select user_name from things_inf where id='+"'"+id+"'")[0][0]
        if session.get('user_state')!=True:
            dict['login_state']='no'
        else:
            dict['login_state']='yes'#广告表暂时未加
    print(dict)
    #..模版传入 字典返回
    return render_template("things.html",dict=dict)

@app.route('/change_password/<traceback_html_name>',methods=['POST','GET'])
def change_password():
    #转向change_password.html
    if request.method=='GET':
        #对change_password.html    使用的提交form地址为此路由的post   地址的最后一个填充时输入
        return template_rendered('change_password.html',traceback_html_name=traceback_html_name)
    else:
        dbc=SQLconnector()
        new_password=request.form.password       #???

        #此处有一句update语句!!!

@app.route('/claim/<id>',methods=['POST,GET']) #这是事件的id
def claim(id):
    dbc=SQLconnector()
    if request.method=='post':
        user_name=dbc.run('select user_name from things_inf where id='+"'"+id+"'")
        insert_str=str(get('massage'))
        dbc.insert('insert into massage_inf (user_name,massage,id) values')

@app.route('/search_for_pc')
def search_for_pc():
    return render_template('search_for_pc.html')
@app.route('/search_for_phone')
def search_for_phone():
    return render_template('search_for_phone.html')
@app.route('/search/<str_input>',methods=['GET','POST'])
def search(str_input):
#对于search_result.html的分析：
    #具有两个传入参数：
        #state：no 或者 yes  no表示未搜索到结果  此时可以省略inf参数————这是一个双层嵌套列表类型
    #list_inner 结构：
        #id,see_number,time--一共有年月日 时分秒 六个参数  ,picture_url,user_url(用户跳转url),title
#post方法  获取request的搜索语句
    if request.method=='POST':
        search_str=request.form.get('search_str')
    else:
        search_str=str_input
    if search_str==None:
        search_str=request.form.get('search_str1')
    if search_str==None:
        search_str=request.form.get('search_str2')
    if search_str==None:
        return '找不到搜索语句'
    elif search_str=='':
        return redirect('/')   #否则返回主页
    else:
        session['search_obj']=SearchHelper(search_str)   #生成搜索对象

    if session['search_obj'].state=='no':
        return redirect('/')
    else:
        id_list=session['search_obj'].list
        dbc=SQLconnector()
        inf=[]
        print(id_list)
        for i in range(0,len(id_list)):
            id=id_list[i]
            #dgl----dbc_get_list
            dgl=dbc.run("select see_number,picture_name,release_time,user_name,title from things_inf where id="+str(id))[0]
            list_inner=[id,dgl[0],time_list(dgl[2]),'/static/things_inf_pic/'+dgl[1],'/user/'+dgl[3],dgl[4]]
            inf.append(list_inner)
        print(inf)
        print(len(inf))
        return 'w'

@app.route('/test_search',methods=['POST'])
def test_search():
    return render_template('search_result.html')

#Model_1:数据库连接器
#先实例化   然后使用run 传入sqlstr
#注意事项：
    #..用run查询不到就会返回空列表  一定要注意此时的的二阶索引会返回错误
@app.route('/test_user')
def test_user():
    return render_template('user.html')

class SQLconnector():
    def __init__(self):
        self._init_list={
            'mul_select_num':5
        }
        self.DataBaseConfig = {
            'host': '127.0.0.1',
            'user': app.config['USER'],
            'password': app.config['PASSWORD'],
            'port': 3306,
            'database':app.config['DATA_BASE'],
            'charset': 'utf8'
        }
    def _new_connector(self):#生成连接器
        try:
            self.connector = mysql.connector.connect(**self.DataBaseConfig)
            self.connector_cursor = self.connector.cursor()
        except Exception as e:
            print('erro:connect fails!:'+str(e)) #for test
    def run(self,sqlstr):#执行sql语句 并且关闭数据库  返回结果
        self.sqlstr=sqlstr
        if self.sqlstr=='':
            print("run stop because of string is not input")
            return [['']]   #嵌套空串 支持二阶索引
        else:
            self._new_connector()
            try:
                self.connector_cursor.execute(self.sqlstr)
                result = self.connector_cursor.fetchall()
            except mysql.connector.Error as e:
                print('connect fails!{}'.format(e))
                result = [['']]
            finally:
                self.connector.commit()
                self._close()
            if result == []:
                return [['']]
            else:
                return result
    def insert(self,sqlstr):#插入数据函数
        self.sqlstr=sqlstr
        if self.sqlstr=='':
            print("run stop because of string is not input")
            return []
        else:
            self._new_connector()
            try:
                self.connector_cursor.execute(self.sqlstr)
            except mysql.connector.Error as e:
                print('connect fails!{}'.format(e))
            finally:
                self.connector.commit()
                self._close()
    def _close(self):
        self.connector_cursor.close()
        self.connector.close()
# Model_2:动态响应性常驻数据结构
class Data():
    def __init__(self):     # all of the date must be a url and not a id in database
        self.main_recommend=[]      #length:7 放置七个id
        self.main_list=[]    #放置5组 每组10个数据  跳转更高页 便使用查数据库法
        self.fabu_forPC_guanggao={}            #picture url and the gonging to href
        self.thing_forPC_guanggao={}
        self.release_inf = {}
        self.dbc = SQLconnector()   #Date_Being 类的私有化查询器
        self.max = int(self.dbc.run("SELECT MAX(id) FROM things_inf")[0][0])
    def start(self):   #初始化填充数据   比如广告等等   这些数据从文件当中寻找（便于修改）
        self._max_to_list()
        with open('main_recommend.txt', 'r') as f:
            self.main_recommend=eval(f.readlines()[0])

        #此处要求由新配置文件（非config）文件配置写入推荐表

    def _max_to_list(self): #内部调用二级函数
        self.main_list = [(self.max, self.max - 1, self.max - 2, self.max - 3, self.max - 4, self.max - 5, self.max - 6,
                           self.max - 7, self.max - 8, self.max - 9),
                          (self.max - 10, self.max - 11, self.max - 12, self.max - 13, self.max - 14, self.max - 15,
                           self.max - 16, self.max - 17, self.max - 18, self.max - 19),
                          (self.max - 20, self.max - 21, self.max - 22, self.max - 23, self.max - 24, self.max - 25,
                           self.max - 26, self.max - 27, self.max - 28, self.max - 29),
                          (self.max - 30, self.max - 31, self.max - 32, self.max - 33, self.max - 34, self.max - 35,
                           self.max - 36, self.max - 37, self.max - 38, self.max - 39),
                          (self.max - 40, self.max - 41, self.max - 42, self.max - 43, self.max - 44, self.max - 45,
                           self.max - 46, self.max - 47, self.max - 48, self.max - 49),
                          ]
    def update_list(self):   #主要用于提交后更新main页最新列表数据
        self.max+=1
        self._max_to_list()
    def update_recommend(self):   #更新最新推荐
        with open('main_recommend.txt', 'r') as f:
            self.main_recommend = eval(f.readlines()[0])   #修改七个id  管理员界面调用 要在更新配置文件的前提下

#Model_3:语句拼接 sql注入防护
class MulStr():
    def __init__(self):
        self.checkwords_list = [
            'select',
            'from',
            'delete',
            'update'
        ]
    def cheak(self,word):
        pass


#Model_5:短信发送模块
class Massage():
    def __init__(self,massage_id):
        self.massage_id=massage_id
        self.list=dbc.run('select * from massage_inf where massage_id='+"'"+self.massage_id+"'")[0]


#Model_6:搜索类
# 函数简介：
# ..传入str类型的 返回一个带指针双链表

class SearchHelper():
    def __init__(self,str):
        self.str=str
        self.dbc=SQLconnector()
        self.list_sql_get=self.dbc.run("select id from things_inf where description like '%"+self.str+"%' or title like '%"+self.str+"%'")
        self.state='yes'
        if self.list_sql_get==[] or self.list_sql_get==[''] or self.list_sql_get==[['']]:
            self.state='no'
        else:
            self.list=[]
            for i in range(0,len(self.list_sql_get)):
                self.list.append(self.list_sql_get[i][0])
#Model_7:链表类（双）辅助数据结构（model6的辅助模块 瀑布流的数据储存结构部分）
class Node_new_double():
    def __init__(self,data,next,before):
        self.data=data
        self.next=next
        self.before=before
class Double_link():
    def __init__(self,list=[]):
        if list==[]:
            self.head=Node_new_double(None,None,None)
        else:
            self.position=-1
            self.head=Node_new_double(list[self.position],None,None)
            self.position-=1
            self.end=self.head
            self.store=self.end #用于储存前一个节点对象
            self.probe_helper=self.end   #用于调用指针
            while True:
                try:
                    self.head = Node_new_double(list[self.position], self.head, None)
                    self.probe_helper = self.head
                    self.store.before = self.probe_helper
                    self.store = self.head
                    self.position -= 1
                except:
                    break
    def throught(self):
        self.list = []
        self.probe = self.head  # 初始化指针
        while self.probe != None:
            self.list.append(self.probe.data)
            self.probe = self.probe.next
        return self.list
    def __len__(self):
        self.i=0
        self.probe=self.head
        while self.probe!=None:
            self.i+=1
            self.probe=self.probe.next
        return self.i
    def delete(self,delete_data):
        self.probe = self.head
        if self.probe.data==delete_data:
            self.head=self.head.next
            self.head.before=None
            self.delete(delete_data)
        else:
            while self.probe.next != None:  #如果不是最后一个元素的话
                if self.probe.next.data==delete_data:  #如果下一个元素为目标
                    if self.probe.next.next==None:    #如果下一个元素为最后一个
                        self.probe.next=None
                        self.end=self.probe
                    else:
                        self.probe.next=self.probe.next.next
                        self.probe.next.next.before=self.probe
                else:
                    self.probe=self.probe.next
    def change_by_value(self,data_changeby,*args):
        self.probe = self.head
        while self.probe!=None:
            if self.probe.data in args:
                self.probe.data=data_changeby
            self.probe=self.probe.next
    def change_by_position(self,data_changeby,position):
        if position>len(self) or position<1:
            raise ValueError
        self.probe = self.head
        position-=1
        while position!=0:
            self.probe=self.probe.next
        self.probe.data=data_changeby
    def append(self,append_data):
        self.probe=self.end   #初始化指针
        self.end=Node_new_double(append_data,None,self.probe)
        self.probe.next=self.end
    def head_append(self,append_data):
        self.probe=self.head #初始化指针
        self.head=Node_new_double(append_data,self.head,None)
        self.probe.before=self.head
    def __repr__(self):
        return 'length:' + str(len(self)) + '\nlink_dataList: ' + str(self.throught())
if __name__=="__main__":
    start_server()
    app.run(debug=True,host='0.0.0.0')
