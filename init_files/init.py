import os
import subprocess
import sys
import traceback


def __init__():
    path = sys.argv[1]
    try:
        if path.startswith('/') and path.endswith('/'):
            with open(f"{path}projects/slack_bot/init_files/slack_bot.service", 'r') as service_file:
                lines = service_file.read()
                service_file.close()
            with open(f"{path}projects/slack_bot/init_files/slack_bot.service", "w") as service_file:
                service_file.truncate()
                service_file.writelines(lines.replace('{HOME_PATH}', f'{path}'))
                service_file.close()

            python = f"#!{path}projects/slack_bot/slack_bot/bin/python3"
            print(subprocess.Popen((f'cat {path}projects/slack_bot/init_files/slack_bot.service; '
                                    'python3 -m venv slack_bot && '
                                    f'. {path}projects/slack_bot/slack_bot/bin/activate && '
                                    'pip install --upgrade pip && '
                                    'pip install -r requirements.txt;'
                                    f'cp {path}projects/slack_bot/init_files/slack_bot.service /etc/systemd/system/ && '
                                    'systemctl enable slack_bot.service && '
                                    'systemctl start slack_bot.service; '
                                    'systemctl status slack_bot.service'), shell=True,
                                   stdout=subprocess.PIPE, env=os.environ).stdout.read().decode('utf-8'))
            edited_file = f"{path}projects/slack_bot/main.py.bak"
            main_file = f"{path}projects/slack_bot/main.py"
            with open(main_file, 'r') as read_object, open(edited_file, 'w') as write_object:
                write_object.write(f"{python}\n")
                for line in read_object:
                    write_object.write(line)

            os.rename(edited_file, main_file)
            os.remove(main_file)
            os.chmod(f'{path}projects/slack_bot/main.py', 0o755)
        else:
            print(f'You need to print /home/path/ with "/" at end and beginning, I need full home path')

    except IndexError:
        print(f'You need to print -- ./init_files/init.py /home/path/')
    except Exception as error:
        print(f'An error occurred: {traceback.format_exc(error)}')


if __name__ == '__main__':
    __init__()
