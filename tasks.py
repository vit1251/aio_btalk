
from invoke import task

@task
def uninstall(c):
    c.run('python3 -B -u -m pip uninstall -y aio_btalk', pty=True)

@task(default=True, pre=[ uninstall ])
def install(c):
    c.run('python3 -B -u setup.py install', pty=True)

