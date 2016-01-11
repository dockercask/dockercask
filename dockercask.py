import os
import shutil
import subprocess
import sys
import random
import threading
import json
import time

# sudo sh -c 'echo "load-module module-native-protocol-tcp" >> /etc/pulse/default.pa'
# pulseaudio -k
# pulseaudio --start

USER_HOME_DIR = '~'
HOME_DIR = '~/Docker'
PULSE_COOKIE_PATH = '~/.config/pulse/cookie'
TMP_DIR = '/tmp'
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
PULSE_SERVER = 'tcp:172.17.0.1:4713'



# Init
USER_HOME_DIR = os.path.expanduser(USER_HOME_DIR)
HOME_DIR = os.path.expanduser(HOME_DIR)
PULSE_COOKIE_PATH = os.path.expanduser(PULSE_COOKIE_PATH)
TMP_DIR = os.path.expanduser(TMP_DIR)
CONF_DIR = os.path.join(HOME_DIR, '.config')
BASE_CONF_PATH = os.path.join(CONF_DIR, 'base.json')



def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

mkdirs(CONF_DIR)

if not os.path.exists(BASE_CONF_PATH):
    shutil.copyfile(
        os.path.join(ROOT_DIR, 'apps', 'base', 'settings.json'),
        BASE_CONF_PATH
    )

conf_data = {}
with open(BASE_CONF_PATH, 'r') as conf_file:
    conf_data = json.loads(conf_file.read())

SUDO_DOCKER = conf_data.get('sudo_docker', False)
SHARE_CLIPBOARD = conf_data.get('share_clipboard', False)
SHARE_FONTS = conf_data.get('share_fonts', False)
SHARE_THEMES = conf_data.get('share_themes', False)
SHARE_ICONS = conf_data.get('share_icons', False)
SHARE_USER_FONTS = conf_data.get('share_user_fonfs', False)
SHARE_USER_THEMES = conf_data.get('share_user_themes', False)
DEBUG = conf_data.get('debug', False)

GPU = conf_data.get('gpu', 'auto')
if GPU == 'auto':
    try:
        subprocess.check_output(['which', 'nvidia-settings'])
        GPU = 'nvidia'
    except:
        GPU = 'intel'

DEFAULT_WIN_SIZE = conf_data.get('default_win_size', '1024x768')
DEFAULT_VOLUMES = conf_data.get('default_volumes', [])

def pull():
    subprocess.check_call((['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'pull',
        'pritunl/archlinux',
    ])

def build(app):
    if app == 'base-intel' or app == 'base-nvidia':
        image_name = 'base-xorg'
    else:
        image_name = app

    app_dir = os.path.join(ROOT_DIR, 'apps', app)

    subprocess.check_call((['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'build',
        '--rm',
        '-t', 'dockercask/' + image_name,
        '.',
    ], cwd=app_dir)

    if app == 'base':
        build('base-' + GPU)

def build_all():
    build('base')
    for app in os.listdir(HOME_DIR):
        if not os.path.isdir(os.path.join(HOME_DIR, app)) or \
                app.startswith('.'):
            continue
        build(app)

def add(app):
    app_dir = os.path.join(HOME_DIR, app)
    app_conf_path = os.path.join(CONF_DIR, app + '.json')

    mkdirs(app_dir)

    if not os.path.exists(app_conf_path):
        shutil.copyfile(
            os.path.join(ROOT_DIR, 'apps', app, 'settings.json'),
            app_conf_path
        )

def run(app):
    app_dir = os.path.join(HOME_DIR, app)
    app_conf_path = os.path.join(CONF_DIR, app + '.json')
    fonts_dir = os.path.join(USER_HOME_DIR, '.fonts')
    themes_dir = os.path.join(USER_HOME_DIR, '.themes')
    cmd = []
    args = []
    volume_args = []

    if DEBUG:
        args.append('-it')
        cmd.append('/bin/bash')

    downloads_dir = os.path.join(USER_HOME_DIR, 'Downloads')

    for src, dest in DEFAULT_VOLUMES:
        volume_args += [
            '-v', '%s:%s' % (os.path.expanduser(src), dest),
        ]

    if SHARE_FONTS:
        volume_args += [
            '-v', '%s:%s' % ('/usr/share/fonts', '/usr/share/fonts:ro'),
        ]

    if SHARE_ICONS:
        volume_args += [
            '-v', '%s:%s' % ('/usr/share/icons', '/usr/share/icons:ro'),
        ]

    if SHARE_THEMES:
        volume_args += [
            '-v', '%s:%s' % ('/usr/share/themes', '/usr/share/themes:ro'),
        ]

    if SHARE_USER_FONTS:
        volume_args += [
            '-v', '%s:%s' % (fonts_dir, '/home/docker/.fonts:ro'),
        ]

    if SHARE_USER_THEMES:
        volume_args += [
            '-v', '%s:%s' % (themes_dir, '/home/docker/.themes:ro'),
        ]

    mkdirs(fonts_dir)
    mkdirs(themes_dir)

    x_cookie = subprocess.check_output(['mcookie'])
    x_num = str(random.randint(1000, 32000))
    x_auth_path = os.path.join(TMP_DIR, '.X11-docker-' + x_num)
    x_screen_path = os.path.join(TMP_DIR, '.X11-unix', 'X' + x_num)

    with open(x_auth_path, 'w') as _:
        pass

    subprocess.check_call([
        'xauth',
        '-f', x_auth_path,
        'add',
        ':' + x_num,
        'MIT-MAGIC-COOKIE-1',
        x_cookie,
    ])

    subprocess.check_call([
        'xauth',
        'add',
        ':' + x_num,
        'MIT-MAGIC-COOKIE-1',
        x_cookie,
    ])

    x_proc = None
    docker_proc = None

    def clean_up():
        try:
            if docker_proc:
                docker_proc.kill()
        except:
            pass
        try:
            if x_proc:
                x_proc.kill()
        except:
            pass
        try:
            os.remove(x_auth_path)
        except:
            pass
        try:
            subprocess.check_output([
                'xauth',
                'remove',
                ':' + x_num,
            ])
        except:
            pass

    x_proc = subprocess.Popen([
        'Xephyr',
        '-auth', x_auth_path,
        '-screen', DEFAULT_WIN_SIZE,
        '-title', app,
        '-br',
        '-resizeable',
        '-nolisten', 'tcp',
        ':' + x_num,
    ])

    def thread_func():
        x_proc.wait()
        clean_up()

    thread = threading.Thread(target=thread_func)
    thread.daemon = True
    thread.start()

    docker_proc = subprocess.Popen((['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'run',
        '--rm',
    ] + args + [
        '-v', '%s:%s' % (x_screen_path, x_screen_path),
        '-v', '%s:%s' % (PULSE_COOKIE_PATH, '/tmp/.pulse-cookie'),
        '-v', '%s:%s' % (BASE_CONF_PATH, '/base.json:ro'),
        '-v', '%s:%s' % (app_conf_path, '/app.json:ro'),
        '-v', '%s:%s' % (app_dir, '/home/docker/Docker'),
    ] + volume_args + [
        '-e', 'DISPLAY=:' + x_num,
        '-e', 'XAUTHORITY=/tmp/.Xauth',
        '-e', 'XCOOKIE=' + x_cookie,
        '-e', 'PULSE_SERVER=' + PULSE_SERVER,
        'dockercask/' + app,
    ] + cmd)

    if SHARE_CLIPBOARD:
        thread = threading.Thread(target=share_clipboard, args=(x_num,))
        thread.daemon = True
        thread.start()

    docker_proc.wait()
    clean_up()

def set_clipboard(num, val):
    proc = subprocess.Popen(
        ['xsel', '--display', ':' + num, '-b', '-i'],
        stdin=subprocess.PIPE,
    )
    proc.communicate(input=val)
    proc.wait()

def get_clipboard(num):
    return subprocess.check_output(
        ['xsel', '--display', ':' + num, '-b', '-o'],
    )

def share_clipboard(app_num):
    time.sleep(1)

    val = get_clipboard('0')
    set_clipboard(app_num,val )
    clipboards = [val, get_clipboard(app_num)]
    clipboard = None

    while True:
        for num in ('0', app_num):
            val = get_clipboard(num)
            i = 0 if num == '0' else 1
            if val != clipboards[i] and val != clipboard:
                clipboard = val
                clipboards[i] = val
                new_num = app_num if num == '0' else '0'
                set_clipboard(new_num, val)
        time.sleep(0.1)


command = sys.argv[1]

if command == 'build':
    app = sys.argv[2]
    build(app)

elif command == 'build-all':
    build_all()

elif command == 'update':
    pull()
    build_all()

elif command == 'add':
    app = sys.argv[2]
    add(app)

elif command == 'run':
    app = sys.argv[2]
    run(app)
