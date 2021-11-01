
import os
import subprocess


def __init__():
    python = "#!/home/egor/projects/slackk_bot/slack_bot/bin/python3"
    print(subprocess.Popen('python3 -m venv slack_bot;'
                     '. ~/projects/slackk_bot/slack_bot/bin/activate;'
                     'pip install --upgrade pip;'
                     'pip install -r requirements.txt;'
                     'chmod +x ~/projects/slackk_bot/main.py', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode('utf-8'))
    edited_file = "main.py.bak"
    main_file = "main.py"
    with open(main_file, 'r') as read_object, open(edited_file, 'w') as write_object:
        write_object.write(f"{python}\n")
        for line in read_object:
            write_object.write(line)

        os.remove(main_file)
        os.rename(edited_file, main_file)


if __name__ == '__main__':
    __init__()
