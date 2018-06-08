from flask_migrate import MigrateCommand
from flask_script import Manager
from mainapp import create_app


app = create_app()

manager = Manager(app)
#添加迁移命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
