from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from json import load,dump
from pymysql import connect
from sys import argv


# 主窗口
class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_login_window()
        self.init_main_window_widget()

    # 初始化登录窗口的基本控件
    def init_login_window(self):
        # 外观
        self.setWindowTitle('数据库登陆')
        screen_size = [QApplication.desktop().screenGeometry().width(),
                       QApplication.desktop().screenGeometry().height()]
        self.setGeometry(screen_size[0]//2 - 210, screen_size[1]//2 - 125, 420, 250)
        # 设置基础控件
        self.host_label = QLabel('IP地址', self)
        self.host_label.setFixedSize(50, 30)
        self.host_label.setFont(QFont('微软雅黑', 12, 75))
        self.host_label.setAlignment(Qt.AlignCenter)
        self.name_label = QLabel('用户名', self)
        self.name_label.setFixedSize(50, 30)
        self.name_label.setFont(QFont('微软雅黑', 12, 75))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.paw_label = QLabel('密码', self)
        self.paw_label.setFixedSize(40, 30)
        self.paw_label.setFont(QFont('微软雅黑', 12, 75))
        self.paw_label.setAlignment(Qt.AlignCenter)
        self.remember = QCheckBox('记住我', self)
        self.remember.setCheckable(True)
        self.remember.setStyleSheet("QCheckBox{color:#A020F0}")
        self.remember.setFont(QFont('微软雅黑', 13, 75))
        self.host = QLineEdit(self)
        self.name = QLineEdit(self)
        self.paw = QLineEdit(self)
        self.submit = QPushButton('提交', self)
        self.submit.clicked.connect(self.login_button)
        self.cancel = QPushButton('清空', self)
        self.cancel.clicked.connect(self.clear_text)
        self.set_login_style()
        # 添加到Layout
        self.host_label.move(80, 30)
        self.host.move(150, 30)
        self.name_label.move(80, 80)
        self.name.move(150, 80)
        self.paw_label.move(80, 130)
        self.paw.move(150, 130)
        self.submit.move(160, 200)
        self.cancel.move(290, 200)
        self.remember.move(70, 202)
        self.host.setText('127.0.0.1')
        self.name.setText('root')
        # 显示所有控件
        for child in [self.host_label, self.host, self.remember, self.name, self.name_label, self.paw, self.paw_label,
                      self.submit, self.cancel]:
            child.setVisible(True)
        # 检查是否有保存的账号密码
        f = open('user.json', encoding='utf-8')
        info = load(f)
        if info != 0:
            self.host.setText(info["host"])
            self.name.setText(info["user"])
            self.paw.setText(info["paw"])
            self.remember.setChecked(True)
        f.close()

    # 设定登陆窗口的控件style
    def set_login_style(self):
        self.host.setFixedSize(200, 30)
        self.host.setClearButtonEnabled(True)
        self.host.setToolTip('输入数据库IP地址')
        self.name.setFixedSize(200, 30)
        self.name.setClearButtonEnabled(True)
        self.name.setToolTip('输入名称')
        self.paw.setFixedSize(200, 30)
        self.paw.setClearButtonEnabled(True)
        self.paw.setEchoMode(QLineEdit.Password)
        self.paw.setToolTip('输入密码')
        self.submit.setFixedSize(58, 28)
        self.submit.setStyleSheet('QPushButton{background-color:lightgreen;border-radius:8px}')
        self.submit.setToolTip('连接数据库')
        self.cancel.setFixedSize(58, 28)
        self.cancel.setStyleSheet('QPushButton{background-color:pink;border-radius:8px}')
        self.cancel.setToolTip('清空输入')
        self.host.setFont(QFont('Microsoft YaHei', 15))
        self.name.setFont(QFont('Microsoft YaHei', 15))
        self.paw.setFont(QFont('Microsoft YaHei', 15))
        self.submit.setFont(QFont('微软雅黑', 11, 75))
        self.cancel.setFont(QFont('微软雅黑', 11, 75))

    # 初始化主窗口控件
    def init_main_window_widget(self):
        # 翻页按钮
        self.last = QPushButton('上一页', self)
        self.last.setFixedSize(58, 28)
        self.last.setStyleSheet('QPushButton{background-color:lightgreen;border-radius:8px}')
        self.last.setToolTip('上一页')
        self.last.move(800, 650)
        self.next = QPushButton('下一页', self)
        self.next.setFixedSize(58, 28)
        self.next.setStyleSheet('QPushButton{background-color:lightgreen;border-radius:8px}')
        self.next.setToolTip('下一页')
        self.next.move(950, 650)
        # 建表按钮
        self.add_butt = QPushButton('增加列', self)
        self.submit_butt = QPushButton('确定', self)
        self.add_butt.setFixedSize(58, 28)
        self.add_butt.setStyleSheet('QPushButton{background-color:lightgreen;border-radius:8px}')
        self.add_butt.setToolTip('增加列')
        self.add_butt.move(1080, 30)
        self.submit_butt.setFixedSize(58, 28)
        self.submit_butt.setStyleSheet('QPushButton{background-color:lightgreen;border-radius:8px}')
        self.submit_butt.setToolTip('提交')
        self.submit_butt.move(1080, 100)
        # 隐藏
        self.add_butt.setVisible(False)
        self.submit_butt.setVisible(False)
        self.add_butt.clicked.connect(self.add_column)
        self.submit_butt.clicked.connect(self.submit_create)
        # 页码标签
        self.page_label = QLabel('', self)
        self.page_label.setFont(QFont('微软雅黑', 10, 75))
        self.page_label.move(885, 653)
        # 事件
        self.last.clicked.connect(self.page_go_last)
        self.next.clicked.connect(self.page_go_next)
        # 数据库list
        self.db_lis = QListWidget(self)
        self.db_lis.setFont(QFont('微软雅黑', 11, 75))
        self.db_lis.setFixedSize(200, 200)
        self.db_lis.clicked.connect(self.show_table)
        self.db_lis.move(20, 30)
        # 数据表list
        self.table_lis = QListWidget(self)
        self.table_lis.setFont(QFont('微软雅黑', 10))
        self.table_lis.setFixedSize(200, 330)
        self.table_lis.clicked.connect(self.show_info)
        # 右键菜单
        self.table_lis.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_lis.customContextMenuRequested[QPoint].connect(self.show_table_menu)
        self.table_lis.move(20, 300)
        # 数据
        self.info = QTableWidget(self)
        self.info.setFixedSize(800, 600)
        self.info.move(270, 30)
        # 全部隐藏
        for child in [self.last, self.next, self.page_label, self.add_butt, self.submit_butt, self.db_lis, self.table_lis, self.info]:
            child.setVisible(False)

    # 登陆按钮
    def login_button(self):
        host = self.host.text()
        name = self.name.text()
        paw = self.paw.text()
        # 检查输入是否合法
        if name == '' or paw == '':
            QMessageBox.warning(self, '警告', '用户名或密码不能为空！', QMessageBox.Ok, QMessageBox.Ok)
        # 连接数据库
        else:
            try:
                self.connect = connect(
                    host=host,
                    user=name,
                    password=paw,
                    charset='utf8mb4'
                )
                self.cursor = self.connect.cursor()
                # 检查改变存储的用户名密码
                self.check_user()
                # 删除所有控件
                for child in [self.host_label, self.host, self.remember, self.name, self.name_label, self.paw, self.paw_label, self.submit, self.cancel]:
                    child.setVisible(False)
                self.init_main_window()
            except:
                QMessageBox.warning(self, '错误', '用户名或密码错误，请重试！', QMessageBox.Ok, QMessageBox.Ok)
                self.paw.clear()

    # 检查存储
    def check_user(self):
        f = open('user.json', 'w', encoding='utf-8')
        # 存入信息,否则存入0
        if self.remember.isChecked():
            dic = {"host": self.host.text(), "user": self.name.text(), "paw": self.paw.text()}
        else:
            dic = 0
        dump(dic, f)
        f.close()

    # 清除按钮
    def clear_text(self):
        self.name.clear()
        self.paw.clear()

    # 回车按钮
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.login_button()

    # 设置主窗口样式
    def init_main_window(self):
        # 显示控件
        for child in [self.db_lis, self.table_lis, self.info]:
            child.setVisible(True)
        # 清空信息
        self.db_lis.clear()
        self.table_lis.clear()
        self.info.clear()
        # 显示databases
        self.cursor.execute('show databases')
        db = self.cursor.fetchall()
        for i in db:
            for x in i:
                self.db_lis.addItem(x)
        # 显示菜单
        self.init_menubar()
        # 设置外观
        self.setWindowTitle('数据库管理')
        screen_size = [QApplication.desktop().screenGeometry().width(),
                       QApplication.desktop().screenGeometry().height()]
        self.setGeometry(screen_size[0]//2 - 600, screen_size[1]//2 - 350, 1200, 700)

    # 主菜单
    def init_menubar(self):
        try:
            if self.menubar:
                self.menubar.show()
        except:
            self.menubar = self.menuBar()
            set_bar = self.menubar.addMenu('选项')
            refresh_act = QAction('刷新', self)
            set_bar.addAction(refresh_act)
            logout_bar = QAction('退出', self)
            set_bar.addAction(logout_bar)
            refresh_act.triggered.connect(self.refresh_main_window)
            logout_bar.triggered.connect(self.logout)

    # 刷新界面
    def refresh_main_window(self):
        # 隐藏
        for child in [self.page_label, self.next, self.last]:
            child.setVisible(False)
        self.init_main_window()

    # 退出登陆
    def logout(self):
        # 删除主窗口控件
        for child in [self.db_lis, self.table_lis, self.menubar, self.info, self.next, self.last, self.page_label, self.add_butt, self.submit_butt]:
            child.setVisible(False)
        # 载入登陆界面
        self.init_login_window()

    # 右键表弹出菜单
    def show_table_menu(self):
        table_menu = QMenu(self.table_lis)
        clear_menu = QAction('清空', self)
        refresh_menu = QAction('刷新', self)
        delete_menu = QAction('删除', self)
        new_menu = QAction('新建表', self)
        clear_menu.triggered.connect(self.clear_table)
        refresh_menu.triggered.connect(self.refresh_table)
        delete_menu.triggered.connect(self.delete_table)
        new_menu.triggered.connect(self.new_table)
        table_menu.addActions([clear_menu, refresh_menu, delete_menu, new_menu])
        table_menu.exec_(QCursor.pos())

    # 清空表
    def clear_table(self):
        self.cursor.execute('delete from %s;' % self.table)

    # 刷新表
    def refresh_table(self):
        self.get_info()

    # 删除表
    def delete_table(self):
        self.cursor.execute('drop table %s;' % self.table)
        self.table_lis.removeItemWidget(self.table_widget)
        # 刷新
        self.show_table()

    # 新建表
    def new_table(self):
        # 隐藏标签
        self.page_label.setVisible(False)
        self.last.setVisible(False)
        self.next.setVisible(False)
        # 清空显示信息
        self.info.clear()
        # 一列四行
        self.now_create_column = 2
        self.info.setColumnCount(self.now_create_column)
        self.info.setRowCount(7)
        # 设置表头提示
        for i, s in zip(range(7), ['列名称', '类型', '大小', '自增', '默认值', '是否主键', '表名']):
            item = QTableWidgetItem(s)
            self.info.setItem(i, 0, item)
            item.setFlags(Qt.ItemIsEnabled)
        self.info.setColumnWidth(0, 70)
        # 显示一个加选项按钮一个确定按钮
        self.add_butt.setVisible(True)
        self.submit_butt.setVisible(True)

    # 增加列
    def add_column(self):
        self.now_create_column += 1
        self.info.setColumnCount(self.now_create_column)
        # 设置表名跨列
        self.info.setSpan(6, 1, 1, self.now_create_column)
        self.info.update()

    # 提交新建表
    def submit_create(self):
        # 名称，类型，大小，默认值，是否主键分别生成语句
        all_sql = 'create table if not exists '+self.info.item(6, 1).text() + '('
        primary_k = None
        for i in range(self.now_create_column):
            name = self.info.item(0, i+1)
            tp = self.info.item(1, i + 1)
            size = self.info.item(2, i + 1)
            default = self.info.item(4, i + 1)
            if default:
                default = default.text()
            is_primary = self.info.item(5, i + 1)
            if is_primary:
                if is_primary.text() != '':
                    primary_k = name.text()
            # 创造语句
            if name:
                if self.info.item(3, i + 1) and self.info.item(3, i + 1).text() != '':
                        sql = name.text() + " " + tp.text() + '(' + size.text() + ") NOT NULL AUTO_INCREMENT,"
                elif default:
                    sql = name.text() + " " + tp.text() + '(' + size.text() + ") NOT NULL DEFAULT '" + default + "',"
                else:
                    sql = name.text() + " " + tp.text() + '(' + size.text() + ") NOT NULL,"
                all_sql += sql
        if primary_k:
            all_sql += "PRIMARY KEY (" + primary_k + "),"
        all_sql = all_sql[:-1] + ');'
        print(all_sql)
        try:
            self.cursor.execute(all_sql)
        except:
            print('错误')
        self.show_table()

    # 在下边显示表
    def show_table(self):
        # 取消跨列
        self.info.setSpan(6, 1, 1, 1)
        self.table_lis.clear()
        db = self.db_lis.currentItem().text()
        self.cursor.execute('use %s;' % db)
        self.cursor.execute('show tables;')
        all_table = self.cursor.fetchall()
        for x in all_table:
            for i in x:
                self.table_lis.addItem(i)

    # 显示表中信息
    def show_info(self):
        # 取消跨列
        self.info.setSpan(6, 1, 1, 1)
        # 显示标签
        self.page_label.setVisible(True)
        self.last.setVisible(True)
        self.next.setVisible(True)
        self.submit_butt.setVisible(False)
        self.add_butt.setVisible(False)
        # 设置页数为0
        self.page = 0
        # 清空表
        self.info.clear()
        self.table_widget = self.table_lis.currentItem()
        self.table = self.table_widget.text()
        # 获取表的项目
        self.cursor.execute('describe %s' % self.table)
        field = self.cursor.fetchall()
        self.item_desc = []
        for x in field:
            self.item_desc.append(x[0])
        # 默认每页200行
        self.info.setRowCount(200)
        # 设置表列数和列宽列名
        self.info.setColumnCount(len(self.item_desc))
        self.info.setHorizontalHeaderLabels(self.item_desc)
        for i in range(len(self.item_desc)):
            if len(self.item_desc) > 8:
                self.info.setColumnWidth(i, 100)
            else:
                self.info.setColumnWidth(i, 800//len(self.item_desc))
            # 设置列名
            item = self.info.horizontalHeaderItem(i)
            item.setFont(QFont('微软雅黑', 11, 75))
        self.get_info()

    # 获取一页信息并显示
    def get_info(self):
        # 清空信息重置表头
        self.info.clear()
        # 默认每页200行
        self.info.setRowCount(200)
        # 设置表列数和列宽列名
        self.info.setColumnCount(len(self.item_desc))
        self.info.setHorizontalHeaderLabels(self.item_desc)
        for i in range(len(self.item_desc)):
            # 设置列名
            item = self.info.horizontalHeaderItem(i)
            item.setFont(QFont('微软雅黑', 11, 75))
        now = 200 * self.page
        self.cursor.execute('select COUNT(*) from %s' % self.table)
        self.all_ = self.cursor.fetchone()[0]
        if self.all_ != 0:
            if self.all_ - now >= 200:
                self.cursor.execute('select * from %s limit %d,%d;' % (self.table, now, (now+200)))
                length = 200
            else:
                self.cursor.execute('select * from %s limit %d,%d;' % (self.table, now, (self.all_ - now)))
                length = self.all_ - now
            info = self.cursor.fetchall()
            # 插入信息
            if info:
                for i in range(length):
                    for column in range(len(self.item_desc)):
                        x = info[i][column]
                        if not x:
                            x = 'None'
                        else:
                            x = str(x)
                        new_item = QTableWidgetItem(x)
                        self.info.setItem(i, column, new_item)
            # 显示上一页或者下一页
            self.show_page_button(length)
            return length
        # 显示上一页或者下一页
        self.show_page_button(0)
        return 0

    # 显示翻页按钮
    def show_page_button(self, length):
        # 显示所有页码
        self.page_label.setText('%d/%d' % (self.page+1, (self.all_//200)+1))
        self.page_label.adjustSize()
        # 显示上一页
        self.last.setVisible(False)
        self.next.setVisible(False)
        if self.page > 0:
            self.last.show()
        # 显示下一页
        if length == 200:
            self.next.show()

    # 上一页
    def page_go_last(self):
        self.page -= 1
        self.get_info()

    # 下一页
    def page_go_next(self):
        self.page += 1
        self.get_info()


app = QApplication(argv)
c = Login()
c.show()
app.exec_()
