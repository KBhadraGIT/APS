from setuptools import setup, find_packages


HYPHEN_E_DOT = "-e ."
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements():
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)

    return requirement_list


REPO_NAME = "APS"
AUTHOR_USER_NAME = "KBhadraGIT"
AUTHOR_EMAIL = "kushal.bhadra.git@gmail.com"

setup(
    name=REPO_NAME,
    version= "0.0.1",
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    packages = find_packages(),
    install_requires=get_requirements(),
    whr = "\src",
)