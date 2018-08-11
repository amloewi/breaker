#!/anaconda3/bin/python

# import rumps
import os
import minigame

# https://stackoverflow.com/questions/1724693/find-a-file-in-python
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



if __name__ == "__main__":

    # 1) find the application
    # app_path = find('Breaker.app', '/') # right?
    # https://stackoverflow.com/questions/595305/how-do-i-get-the-path-of-a-the-python-script-i-am-running-in
    # app_path = os.path.realpath(__file__) # or os.path.abspath? Many options.
    # dir_path = os.path.dirname(app_path)
    # minigame_path = os.path.join(dir_path, 'minigame.py') # NO, because the files are NOT INSIDE.

    # ... WRONG WAY AROUND? do a sudo execution of JUST the hotkey,
    # RUN THE REST HERE. Course -- how do I ... INDICATE THAT FILE, IF
    # IT'S NOT FUCKING INCLUDED?
    # Could actually -- define the python file in a STRING, and pass THAT?
    script = """from minigame import minigame; import keyboard; keyboard.add_hotkey("windows+shift+y", minigame)"""
    # => do shell script "<above>" ... ? YES, with 'python -c <string>';
    # but would that DO ANYTHING I WANTED.

    # 2) run with the VERSION OF PYTHON THAT'S INSIDE ... (does that make sense?)
    right_python = '/anaconda3/bin/python' #os.path.join(app_path, '/usr/bin/python3') # or whatever; what IS it?
    # OR JUST: (which python3) ? So you need it, but -- THAT'S ok? WHERE does this need to be executed?
    # MAYBE need to evaluate 'which python'
    shell_call = "{} {}".format("python3 -c", script) # redundant? Just $(which python3)?
    # OR, do I do "sudo open Breaker.app"; how does that conflict with it having
    # ALREADY --BEEN-- called by 'open'?
    # https://stackoverflow.com/questions/3170771/mac-os-x-python-gui-administrator-prompt
    print(shell_call)
    # apparently, there's a more accepted way to do this now; subsystem.Popen;
    # or subprocess? Jesus, christ
    # script = 'tell "some application" to do something'
    # p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # stdout, stderr = p.communicate(script)
    # os.system("""osascript -e 'do shell script "{}" with administrator privileges'""".format(shell_call))
    # os.system("""osascript -e 'do shell script "<commands go here>" ' with administrator privileges'""")
    import subprocess
    # subprocess.call(['gksudo', """python -c '{}'""".format(script)])
    # ... 'cept there IS no 'gksudo' on mac. FUUUUUUUUUUUCK.

    # OR (idiot) I ... run the PARENT process with sudo, and ... import stuff to THAT?
    # But then it's the

    # Piping password into sudo:
    # [SPACE?] $echo <password> | sudo -S <command>
    #https://superuser.com/questions/67765/sudo-with-password-in-one-command-line

    from tkinter import simpledialog # One of the ones where you can't tk.f
    simpledialog.askstring("Breaker needs your password to run!", "Enter password:", show='*')
    # but what is this RUNNING?


    # RUN THIS IFF THE ABOVE LINE WORKS? (How do I SEE that?)
    import minigame
    minigame.start() # something like that -- but I need to, uh, RE-re-factor/move
