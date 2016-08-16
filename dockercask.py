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
LOCALTIME_PATH = '/etc/localtime'
TMP_DIR = '/tmp'
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_PATH = os.path.join(ROOT_DIR, os.path.basename( __file__))
PULSE_SERVER = 'unix:/var/run/pulse/native'



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
DEFAULT_WIN_SIZE = conf_data.get('default_win_size', '1024x768')
DEFAULT_VOLUMES = conf_data.get('default_volumes', [])
DPI = conf_data.get('dpi', '96')
DEBUG = False

GPU = conf_data.get('gpu', 'auto')
if GPU == 'auto':
    try:
        subprocess.check_output(['which', 'nvidia-settings'],
            stderr=subprocess.PIPE)
        GPU = 'nvidia'
    except:
        GPU = 'intel'



def kill_process(process):
    # Attempt to interrupt process then kill
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
    image_id = subprocess.check_output((['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'images',
        '-q',
        image,'docker
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
    app = app.split('#')[0]

    if not image_exists('dockercask/base'):
        build('base')

    if not image_exists('dockercask/' + app):
        build(app)

def build_all():
    build('base')
    for app in os.listdir(HOME_DIR):
        if not os.path.isdir(os.path.join(HOME_DIR, app)) or \
                app.startswith('.'):
            continue
        build(app)

def add(app):
    app_dir = os.path.join(HOME_DIR, app)
    icon_path = os.path.join(ROOT_DIR, 'apps', app.split('#')[0], 'icon.png')
    app_conf_path = os.path.join(CONF_DIR, app + '.json')
    desktop_entry_path = os.path.join(DESKTOP_DIR,
        'docker-%s.desktop' % app.replace('#', '-'))

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

    with open(desktop_entry_path, 'w') as desktop_file:
        desktop_file.write(DESKTOP_ENTRY % (
            formated_app_name,
            formated_app_name,
            cmd,
            icon_path,
        ))

def remove(app):
    app_dir = os.path.join(HOME_DIR, app)
    app_conf_path = os.path.join(CONF_DIR, app + '.json')
    desktop_entry_path = os.path.join(DESKTOP_DIR,
        'docker-%s.desktop' % app.replace('#', '-'))

    for path in (app_dir, app_conf_path, desktop_entry_path):
        subprocess.check_call([
            'rm',
            '-rf',
            path,
        ])

def app_exists(app):
    if os.path.exists(os.path.join(HOME_DIR, app)):
        return True
    return False

def focus_app(app):
    try:
        subprocess.check_call([
            'wmctrl',
            '-F',
            '-R',
            app,
        ])
        return True
    except subprocess.CalledProcessError:
        pass
    return False

def run(app):
    app_dir = os.path.join(HOME_DIR, app)
    app_conf_path = os.path.join(CONF_DIR, app + '.json')
    fonts_dir = os.path.join(USER_HOME_DIR, '.fonts')
    themes_dir = os.path.join(USER_HOME_DIR, '.themes')
    cmd = []
    docker_args = []
    volume_args = []

    with open(app_conf_path, 'r') as app_conf_file:
        app_conf_data = json.loads(app_conf_file.read())

    host_x11 = app_conf_data.get('host_x11')
    increase_shm = app_conf_data.get('increase_shm', INCREASE_SHM)
    dpi = app_conf_data.get('dpi', DPI)

    if DEBUG:
        docker_args.append('-it')
        cmd.append('/bin/bash')

    if host_x11:
        volume_args += ['-v', '/etc/machine-id:/etc/machine-id:ro']
        docker_args += ['--device', '/dev/dri:/dev/dri']
        docker_args += ['--device', '/dev/nvidia0:/dev/nvidia0']
        docker_args += ['--device', '/dev/nvidiactl:/dev/nvidiactl']
        docker_args += ['--device', '/dev/nvidia-modeset:/dev/nvidia-modeset']

    if increase_shm:
        if isinstance(increase_shm, basestring):
            shm_size = increase_shm
        else:
            shm_size = '4g'
        docker_args += ['--shm-size', shm_size]

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
        # Get the cookie for the host display
        x_cookie = subprocess.check_output(['xauth', 'list', ':0']).split()[-1]
        x_num = '0'
    else:
        # Create a cookie for the new Xephyr window
        x_cookie = subprocess.check_output(['mcookie'])
        x_num = str(random.randint(1000, 32000))
        x_auth_path = os.path.join(TMP_DIR, '.X11-docker-' + x_num)

        with open(x_auth_path, 'w') as _:
            pass

        # Store the cookie in a file for Xephyr to read
        subprocess.check_call([
            'xauth',
            '-f', x_auth_path,
            'add',
            ':' + x_num,
            'MIT-MAGIC-COOKIE-1',
            x_cookie,
        ])

        # Add the cookie to the hosts xauth to allow xsel and pulseaudio to
        # access the Xephyr window
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
    clean_lock = threading.Lock()

    def clean_up():
        if not clean_lock.acquire(False):
            return

        global interrupt
        interrupt = True

        if docker_id:
            try:
                subprocess.check_output((['sudo'] if SUDO_DOCKER else []) + [
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
                # Remove the Xephyr display from xauth
                subprocess.check_output([
                    'xauth',
                    'remove',
                    ':' + x_num,
                ], stderr=subprocess.PIPE)
            except:
                pass
            try:
                os.remove(x_auth_path)
            except:
                pass
            try:
                os.remove(x_screen_path)
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

        # Create Xephyr window secured with cookie
        x_proc = subprocess.Popen(args + [':' + x_num])

        def x_thread_func():
            try:
                x_proc.wait()
            finally:
                clean_up()

        thread = threading.Thread(target=x_thread_func)
        thread.start()

        # The module-x11-publish for the Xephyr display does not appear to be
        # needed and will crash the pulseaudio server if the Xephyr window is
        # closed while the module is loaded. Module is loaded by xfce4-sesion
        def pacmd_thread_func():
            if DEBUG:
                while True:
                    time.sleep(1)
                    unload_pulseaudio(x_num)
            else:
                for _ in xrange(20):
                    time.sleep(0.5)
                    unload_pulseaudio(x_num)

        thread = threading.Thread(target=pacmd_thread_func)
        thread.daemon = True
        thread.start()

    args = (['sudo'] if SUDO_DOCKER else []) + [
        'docker',
        'run',
        '--rm' if DEBUG else '--detach',
    ] + docker_args + [
        '-v', '%s:%s:ro' % (LOCALTIME_PATH, LOCALTIME_PATH),
        '-v', '%s:%s:ro' % (x_screen_path, x_screen_path),
        '-v', '%s:%s:ro' % (PULSE_COOKIE_PATH, '/tmp/.pulse-cookie'),
        '-v', '%s:%s:ro' % (BASE_CONF_PATH, '/base.json'),
        '-v', '%s:%s:ro' % (app_conf_path, '/app.json'),
        '-v', '%s:%s' % (app_dir, '/home/docker/Docker'),
        '-v', '/var/run/user/%s/pulse/native:/var/run/pulse/native' % (
            os.getuid()),
    ] + volume_args + [
        '-u', 'docker',
        '-e', 'HOME=/home/docker',
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
            subprocess.check_call((['sudo'] if SUDO_DOCKER else []) +
                ['docker', 'wait', docker_id])
        finally:
            clean_up()

def set_clipboard(num, val):
    if not val:
        return

    process = subprocess.Popen(
        ['xsel', '--display', ':' + num, '-b', '-i', '-t', '250'],
        stdin=subprocess.PIPE,
    )
    process.stdin.write(val)
    process.stdin.close()

    for _ in xrange(75):
        time.sleep(0.005)
        exit_code = process.poll()
        if exit_code is not None:
            if exit_code != 0:
                raise Exception('Error from xsel process')
            return

    process.kill()
    raise Exception('Timeout setting clipboard')

def get_clipboard(num):
    process = subprocess.Popen(
        ['xsel', '--display', ':' + num, '-b', '-o', '-t', '250'],
        stdout=subprocess.PIPE,
    )

    for _ in xrange(75):
        time.sleep(0.005)
        exit_code = process.poll()
        if exit_code is not None:
            if exit_code != 0:
                raise Exception('Error from xsel process')
            output, _ = process.communicate()
            return output[:3072]

    process.kill()
    raise Exception('Timeout getting clipboard')

def share_clipboard(app_num):
    time.sleep(1)

    try:
        val = get_clipboard('0')
        set_clipboard(app_num, val)
        clipboards = [val, get_clipboard(app_num)]
    except:
        traceback.print_exc()
        time.sleep(3)
        share_clipboard(app_num)
        return

    while not interrupt:
        try:
            for num in ('0', app_num):
                val = get_clipboard(num)
                i = 0 if num == '0' else 1
                if val != clipboards[i]:
                    set_num = app_num if num == '0' else '0'
                    set_i = 1 if num == '0' else 0
                    set_clipboard(app_num if num == '0' else '0', val)
                    clipboards[i] = val
                    clipboards[set_i] = get_clipboard(set_num)
            time.sleep(0.2)
        except:
            if not interrupt:
                traceback.print_exc()
                time.sleep(3)

def unload_pulseaudio(x_num, count=0):
    # Unload the pulse audio module specific to the Xephyr window. Pacmd will
    # sometimes return an error when busy.
    if count > 2:
        return

    try:
        modules = subprocess.check_output(['pacmd', 'list-modules'])
    except:
        traceback.print_exc()
        time.sleep(0.1)
        unload_pulseaudio(x_num, count + 1)
        return
    index = None

    for line in modules.splitlines():
        line = line.strip()
        if line.startswith('index:'):
            index = line.split()[-1]

        if 'display=:' + x_num in line and index:
            for _ in xrange(3):
                try:
                    subprocess.check_call(['pacmd', 'unload-module', index])
                    break
                except:
                    traceback.print_exc()
                    time.sleep(0.1)

def kill_pulseaudio(x_num, count=0):
    # Kill the pulse audio client specific to the Xephyr window. Pacmd will
    # sometimes return an error when busy.
    if count > 2:
        return

    try:
        clients = subprocess.check_output(['pacmd', 'list-clients'])
    except:
        traceback.print_exc()
        time.sleep(0.1)
        kill_pulseaudio(x_num, count + 1)
        return
    index = None

    for line in clients.splitlines():
        line = line.strip()
        if line.startswith('index:'):
            index = line.split()[-1]

        if 'window.x11.display' in line and ':' + x_num in line and index:
            for _ in xrange(3):
                try:
                    subprocess.check_call(['pacmd', 'kill-client', index])
                    break
                except:
                    traceback.print_exc()
                    time.sleep(0.1)



command = sys.argv[1]
if sys.argv[-1] == '--debug':
    DEBUG = True

if command == 'build':
    app = sys.argv[2]

    exists_pull()
    build(app)

elif command == 'build-all':
    build_all()

elif command == 'update':
    if len(sys.argv) > 2:
        app = sys.argv[2]
    else:
        app = None

    pull()
    if app:
        build('base')
        build(app)
    else:
        build_all()

elif command == 'add':
    app = sys.argv[2]

    exists_pull()
    exists_build(app)
    add(app)

elif command == 'remove':
    app = sys.argv[2]

    remove(app)

else:
    if command == 'run':
        app = sys.argv[2]
    else:
        app = sys.argv[1]

    if not app_exists(app):
        print 'App must be added before running'
        exit(1)

    if focus_app(app):
        exit(0)
    exists_pull()
    exists_build(app)
    run(app)
