import os
import shutil
import subprocess
import sys
import random
import threading
import json
import time
import traceback
import signal

USER_HOME_DIR = '~'
HOME_DIR = '~/Docker'
APP_DIR = '~/.local/share/applications'
PULSE_COOKIE_PATH = '~/.config/pulse/cookie'
TMP_DIR = '/tmp'
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_PATH = os.path.join(ROOT_DIR, __file__)
PULSE_SERVER = 'unix:/var/run/pulse/native'



# Init
DESKTOP_ENTRY = '''
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Name=Docker - %s
Comment=Docker - %s
Exec=%s
Icon=%s
Categories=Other;
'''
USER_HOME_DIR = os.path.expanduser(USER_HOME_DIR)
HOME_DIR = os.path.expanduser(HOME_DIR)
DESKTOP_DIR = os.path.expanduser(APP_DIR)
PULSE_COOKIE_PATH = os.path.expanduser(PULSE_COOKIE_PATH)
TMP_DIR = os.path.expanduser(TMP_DIR)
CONF_DIR = os.path.join(HOME_DIR, '.config')
BASE_CONF_PATH = os.path.join(CONF_DIR, 'base.json')
interrupt = False



def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

mkdirs(CONF_DIR)

if not os.path.exists(BASE_CONF_PATH):
    shutil.copyfile(
        os.path.join(ROOT_DIR, 'apps', 'base', 'settings.json'),
        BASE_CONF_PATH,
    )

with open(BASE_CONF_PATH, 'r') as conf_file:
    conf_data = json.loads(conf_file.read())

SUDO_DOCKER = conf_data.get('sudo_docker', True)
INCREASE_SHM = conf_data.get('increase_shm', True)
SHARE_CLIPBOARD = conf_data.get('share_clipboard', True)
SHARE_FONTS = conf_data.get('share_fonts', True)
SHARE_THEMES = conf_data.get('share_themes', False)
SHARE_ICONS = conf_data.get('share_icons', False)
SHARE_USER_FONTS = conf_data.get('share_user_fonfs', True)
SHARE_USER_THEMES = conf_data.get('share_user_themes', True)
DPI = conf_data.get('dpi')
DEBUG = False

GPU = conf_data.get('gpu', 'auto')
if GPU == 'auto':
    try:
        subprocess.check_output(['which', 'nvidia-settings'],
            stderr=subprocess.PIPE)
        GPU = 'nvidia'
    except:
        GPU = 'intel'

DEFAULT_WIN_SIZE = conf_data.get('default_win_size', '1024x768')
DEFAULT_VOLUMES = conf_data.get('default_volumes', [])

def kill_process(process):
    terminated = False

    for _ in xrange(200):
        try:
            process.send_signal(signal.SIGINT)
        except OSError as error:
            if error.errno != 3:
                raise
        for _ in xrange(4):
            if process.poll() is not None:
                terminated = True
                break
            time.sleep(0.0025)
        if terminated:
            break

    if not terminated:
        for _ in xrange(10):
            if process.poll() is not None:
                break
            try:
                process.send_signal(signal.SIGKILL)
            except OSError as error:
                if error.errno != 3:
                    raise
            time.sleep(0.01)

def image_exists(image):
    image_id = subprocess.check_output([
        'docker',
        'images',
        '-q',
        image,
    ]).strip()

    return bool(image_id)

def pull():
    subprocess.check_call((['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'pull',
        'pritunl/archlinux',
    ])

def exists_pull():
    if not image_exists('pritunl/archlinux'):
        pull()

def build(app):
    app = app.split('#')[0]

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

def exists_build(app):
    if not image_exists('dockercask/' + app):
        build(app)

def build_all():
    build('base')
    for app in os.listdir(HOME_DIR):
        if not os.path.isdir(os.path.join(HOME_DIR, app)) or \
                app.startswith('.'):
            continue
        exists_build(app)

def add(app):
    app_dir = os.path.join(HOME_DIR, app)
    icon_path = os.path.join(ROOT_DIR, 'apps', app.split('#')[0], 'icon.png')
    app_conf_path = os.path.join(CONF_DIR, app + '.json')

    mkdirs(app_dir)

    if not os.path.exists(app_conf_path):
        shutil.copyfile(
            os.path.join(ROOT_DIR, 'apps', app.split('#')[0], 'settings.json'),
            app_conf_path,
        )

    if DEBUG:
        cmd = 'xfce4-terminal --command="python2 %s %s --debug"' % (
            SCRIPT_PATH, app)
    else:
        cmd = 'python2 %s %s' % (SCRIPT_PATH, app)

    formated_app_name = app.replace('#', ' ').replace('-', ' ').split()
    formated_app_name = ' '.join([x.capitalize() for x in formated_app_name])

    with open(os.path.join(DESKTOP_DIR,
            'docker-%s.desktop' % app.replace('#', '-')), 'w') as desktop_file:
        desktop_file.write(DESKTOP_ENTRY % (
            formated_app_name,
            formated_app_name,
            cmd,
            icon_path,
        ))

def run(app):
    try:
        subprocess.check_call([
            'wmctrl',
            '-F',
            '-R',
            app,
        ])
        return
    except subprocess.CalledProcessError:
        pass

    app_dir = os.path.join(HOME_DIR, app)
    app_conf_path = os.path.join(CONF_DIR, app + '.json')
    fonts_dir = os.path.join(USER_HOME_DIR, '.fonts')
    themes_dir = os.path.join(USER_HOME_DIR, '.themes')
    cmd = []
    docker_args = []
    volume_args = []

    app_conf_data = {}
    with open(app_conf_path, 'r') as app_conf_file:
        app_conf_data = json.loads(app_conf_file.read())

    host_x11 = app_conf_data.get('host_x11')
    privileged = app_conf_data.get('privileged')
    increase_shm = app_conf_data.get('increase_shm', INCREASE_SHM)
    dpi = app_conf_data.get('dpi', DPI)

    if not os.path.exists(app_dir):
        print 'App must be added before running'
        exit(1)

    if DEBUG:
        docker_args.append('-it')
        cmd.append('/bin/bash')

    if privileged:
        docker_args += ['--privileged']

    if increase_shm:
        docker_args += ['--shm-size', '1g']

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

    if host_x11:
        x_cookie = subprocess.check_output(['xauth', 'list', ':0']).split()[-1]
        x_num = '0'
    else:
        x_cookie = subprocess.check_output(['mcookie'])
        x_num = str(random.randint(1000, 32000))
        x_auth_path = os.path.join(TMP_DIR, '.X11-docker-' + x_num)

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

    x_screen_path = os.path.join(TMP_DIR, '.X11-unix', 'X' + x_num)

    x_proc = None
    docker_id = None

    def clean_up():
        global interrupt
        interrupt = True

        if docker_id:
            try:
                subprocess.check_output([
                    'docker',
                    'rm',
                    '-f',
                    docker_id,
                ], stderr=subprocess.PIPE)
            except:
                pass
        if x_proc:
            kill_process(x_proc)
        if not host_x11:
            try:
                os.remove(x_auth_path)
            except:
                pass
            try:
                subprocess.check_output([
                    'xauth',
                    'remove',
                    ':' + x_num,
                ], stderr=subprocess.PIPE)
            except:
                pass

    if not host_x11:
        args = [
            'Xephyr',
            '-auth', x_auth_path,
            '-screen', DEFAULT_WIN_SIZE,
            '-title', app,
            '-br',
            '-resizeable',
            '-no-host-grab',
            '-nolisten', 'tcp',
        ]

        if dpi:
            args += ['-dpi', dpi]

        x_proc = subprocess.Popen(args + [':' + x_num])

        def thread_func():
            try:
                x_proc.wait()
            finally:
                clean_up()

        thread = threading.Thread(target=thread_func)
        thread.start()

    args = (['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'run',
        '--rm' if DEBUG else '--detach',
    ] + docker_args + [
        '-v', '%s:%s' % (x_screen_path, x_screen_path),
        '-v', '%s:%s' % (PULSE_COOKIE_PATH, '/tmp/.pulse-cookie'),
        '-v', '%s:%s' % (BASE_CONF_PATH, '/base.json:ro'),
        '-v', '%s:%s' % (app_conf_path, '/app.json:ro'),
        '-v', '%s:%s' % (app_dir, '/home/docker/Docker'),
        '-v', '/var/run/user/%s/pulse/native:/var/run/pulse/native' % (
            os.getuid()),
    ] + volume_args + [
        '-e', 'DISPLAY=:' + x_num,
        '-e', 'XAUTHORITY=/tmp/.Xauth',
        '-e', 'XCOOKIE=' + x_cookie,
        '-e', 'PULSE_SERVER=' + PULSE_SERVER,
        'dockercask/' + app.split('#')[0],
    ] + cmd

    print ' '.join(args)

    if not host_x11 and SHARE_CLIPBOARD:
        thread = threading.Thread(target=share_clipboard, args=(x_num,))
        thread.daemon = True
        thread.start()

    if DEBUG:
        try:
            subprocess.check_call(args)
        finally:
            clean_up()
    else:
        docker_id = subprocess.check_output(args).strip()

        try:
            subprocess.check_call(['docker', 'wait', docker_id])
        finally:
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
    set_clipboard(app_num, val)
    clipboards = [val, get_clipboard(app_num)]

    while not interrupt:
        try:
            for num in ('0', app_num):
                val = get_clipboard(num)
                i = 0 if num == '0' else 1
                if val != clipboards[i]:
                    clipboards[0] = val
                    clipboards[1] = val
                    new_num = app_num if num == '0' else '0'
                    set_clipboard(new_num, val)
            time.sleep(0.2)
        except:
            if not interrupt:
                traceback.print_stack()
                time.sleep(5)


command = sys.argv[1]
if sys.argv[-1] == '--debug':
    DEBUG = True

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

else:
    app = sys.argv[1]
    run(app)
