import sys
import os
import subprocess


def runCommand(command):
    """Run commands in the terminal."""
    return subprocess.check_output(command, shell=True).decode().strip()


def createGithubRepo(project_name):
    return [
        f"curl -u '{os.environ.get('githubUser')}' "
        "https://api.github.com/user/repos -d '"
        "{\"name\":\"" + f"{project_name}" + "\"}'",
        "git remote add origin https://github.com/"
        f"{os.environ.get('githubUser')}/"
        f"{project_name}.git",
        "git push -u origin master"
    ]


if __name__ == "__main__":
    try:
        project_name = sys.argv[1]
        runCommand(createGithubRepo(f"{project_name}"))
    except:
        print("Something went wrong!")
