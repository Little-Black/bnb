import sys, os
from getpass import getpass
from random import randint
from re import match
from string import ascii_lowercase

configs = dict()

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
def addConfigVariable(name, message=None, inQuotes=True, valueProcessor=lambda x:x):
    global configs
    if not message:
        message = "Enter "+name+": "
    value = raw_input(message)
    if not value:
        if name not in configs:
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
Ask user for configuration values.
"""
def promptUser():
    global configs
    print
    addConfigVariable("ORG_NAME",
                      "Enter organization name: ")
    addConfigVariable("ORG_NAME_SHORT",
                      "Enter organization acronym: ")
    addConfigVariable("SITE_URL",
                      "Enter URL where this app will be hosted: ",
                      valueProcessor=lambda x: x[:-1] if x[-1] == '/' else x)
    print
    # setting up connection to email server
    print "Next we will set up a way to connect with your email server. If you use gmail, choose \"TLS\", \"587\", and \"smtp.gmail.com\" in the next 3 options."
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


if __name__ == "__main__":
    configFilePath = os.path.join(os.path.dirname(__file__), 'bnbvolunteer/vcsConfig.txt')
    # read current config
    try:
        print "\nWelcome to the installer for volunteer credit system. This script will ask you for some information to customize the site."
        firstTime = True
        if os.path.exists(configFilePath):
            print "\nA configuration file is detected. Is this the first time this script is run? (Selecting yes will generate a new secret key and invalidate existing database.)"
            firstTime = stringToBool(raw_input("Enter (Y)es/(N)o: "))
            if not firstTime:
                print "\nFor the rest of the setup, you can keep the an old setting by leaving the field blank."
                try:
                    with open(configFilePath) as f:
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
        # ask user for config values
        promptUser()
        # write user-specified config to file
        with open(configFilePath, 'w') as f:
            for name in configs:
                value = configs[name]
                f.write('%s = %s\n' % (name, value))
        print "\nInstallation complete.\n"
    except InvalidArgumentException:
        print "\nYou provided an invalid argument.\n"
        sys.exit()
