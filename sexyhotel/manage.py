from flask_script import Manager
from App import create_app
from flask_migrate import MigrateCommand

app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand) # 添加迁移命令

if __name__ == '__main__':
    manager.run()