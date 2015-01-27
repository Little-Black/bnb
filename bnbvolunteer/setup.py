import os, sys
from getpass import getpass
from random import randint
from re import match
from string import ascii_lowercase

configs = dict()
BASE_PATH = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.join(BASE_PATH, "bnbvolunteer/vcsConfig.txt")
MANAGE_PY_PATH = os.path.join(BASE_PATH, "manage.py")

class InvalidArgumentException(Exception):
    @classmethod
    def raiseException(cls):
        raise InvalidArgumentException()

"""
Ask for a configuration value and process it.
"""
def processConfig(message, processFunc):
    value = raw_input(message)
    processFunc(value)

"""
Add a configuration value.
"""
def addConfigVariable(name, message=None, inQuotes=True, valueProcessor=lambda x:x, default=None):
    global configs
    if not message:
        message = "Enter "+name+": "
    value = raw_input(message)
    if not value:
        if name not in configs:
            if default != None:
                configs[name] = default
            else:
                raise InvalidArgumentException()
    else:
        quotingProcessor = lambda x: '\"%s\"' % x if inQuotes else x
        try:
            configs[name] = quotingProcessor(valueProcessor(value))
        except:
            raise InvalidArgumentException()

"""
Ask user for a password.
"""
def addConfigPasswordVariable(name, message="Enter password (will not show on screen): "):
    global configs
    while True:
        pw = getpass(message)
        pwConfirm = getpass("Confirm password (will not show on screen): ")
        if pw != pwConfirm:
            print "The passwords do not match. Please enter them again."
        elif not pw:
            if name in configs:
                break
            else:
                raise InvalidArgumentException()
        else:
            configs[name] = "\"%s\"" % pw
            break

def stringToBool(s):
    if s.lower() in ("true", "t", "yes", "y", "si", "oui", "shi", "hai"):
        return True
    elif s.lower() in ("false", "f", "no", "n", "non", "fou", "shinai"):
        return False
    else:
        raise InvalidArgumentException()


"""
Read existing configuration values and reset fields if needed.
"""
def promptUserFirstTime():
    global configs, CONFIG_FILE_PATH, MANAGE_PY_PATH
    print
    print "Welcome to the installer for volunteer credit system. This script will ask you for some information to customize the site."
    firstTime = True
    if os.path.exists(CONFIG_FILE_PATH):
        print
        print "A configuration file is detected. Is this the first time this script is run?"
        print "(Selecting yes will generate a new secret key and flush existing database.)"
        firstTime = stringToBool(raw_input("Enter (Y)es/(N)o: "))
        if not firstTime:
            # read old config file and load constants
            print
            print "For the rest of the setup, you can keep an old setting by leaving the field blank."
            try:
                with open(CONFIG_FILE_PATH) as f:
                    configRegex = r'(?P<name>[a-zA-Z_]\w*)\s*=\s*(?P<value>.+)\n'
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        else:
                            mo = match(configRegex, line)
                            if mo:
                                configs[mo.group("name")] = mo.group("value")
            except IOError:
                print "Cannot read configuration file."
    if firstTime:
        # generate secret key
        charList = list(ascii_lowercase + "1234567890_=!@#$%^&*()_+")
        generateChar = lambda : charList[randint(0,len(charList)-1)]
        gString = ""
        for i in xrange(50):
            gString += generateChar()
        configs["SECRET_KEY"] = "\"%s\"" % gString
        # flush database
        print
        print "Flushing database..."
        os.system("python %(path)s sqlflush | python %(path)s dbshell" % {"path": MANAGE_PY_PATH})
    # create superuser (optional if not running setup for first time)
    if firstTime:
        createSuperuser = True
    else:
        print
        print "Do you want to create a superuser?"
        createSuperuser = stringToBool(raw_input("Enter (Y)es/(N)o: "))
    if createSuperuser:
        print
        csuExitCode = os.system("python %s createsuperuser" % MANAGE_PY_PATH)
        if not csuExitCode:
            print "\nInstallation cancelled.\n"
            sys.exit()


"""
Ask user for configuration values.
"""
def promptUserGeneral():
    global configs, MANAGE_PY_PATH
    print
    addConfigVariable("ORG_NAME",
                      "Enter organization name: ")
    addConfigVariable("ORG_NAME_SHORT",
                      "Enter organization acronym: ")
    addConfigVariable("SUBHEADER",
                      "Enter website subheader (optional): ",
                      default="\"\"")
    addConfigVariable("SITE_URL",
                      "Enter URL where this app will be hosted: ",
                      valueProcessor=lambda x: x[:-1] if x[-1] == '/' else x)
    print
    # setting up connection to email server
    print "Setting up connection to an email server..."
    print "If you use gmail, choose \"TLS\", \"587\", and \"smtp.gmail.com\" in the next 3 options."
    print
    processConfig("Email server encryption (TLS, SSL, None): ",
                  lambda s: configs.update({"EMAIL_USE_TLS": True, "EMAIL_USE_SSL": False}) if s.upper() == "TLS" \
                            else configs.update({"EMAIL_USE_TLS": False, "EMAIL_USE_SSL": True}) if s.upper() == "SSL" \
                            else configs.update({"EMAIL_USE_TLS": False, "EMAIL_USE_SSL": False}) if s.upper() == "NONE" \
                            else None if not s and "EMAIL_USE_TLS" in configs and "EMAIL_USE_SSL" in configs \
                            else InvalidArgumentException.raiseException())
    addConfigVariable("EMAIL_PORT",
                      "Email server port: ",
                      inQuotes=False,
                      valueProcessor=lambda x: int(x))
    addConfigVariable("EMAIL_HOST",
                      "Email server host: ")
    addConfigVariable("EMAIL_HOST_USER",
                      "User (email): ")
    addConfigPasswordVariable("EMAIL_HOST_PASSWORD")


def saveConfigs():
    global configs, CONFIG_FILE_PATH
    with open(CONFIG_FILE_PATH, 'w') as f:
        for name in configs:
            value = configs[name]
            f.write('%s = %s\n' % (name, value))
    print
    print "Installation complete."
    print


if __name__ == "__main__":
    try:
        promptUserFirstTime()
        promptUserGeneral()
        saveConfigs()
    except InvalidArgumentException:
        print "\nYou provided an invalid argument.\n"
        sys.exit()