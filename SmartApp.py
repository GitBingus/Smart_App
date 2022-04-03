import os, glob, sys, json, time, traceback, logging, platform
from datetime import datetime
from cryptography.fernet import Fernet

try:
    if sys.platform == 'win32' : #windows
        dir = os.getenv('appdata')+'\\SmartApp'
    elif sys.platform == 'darwin':
        dir = "~/Library/Application Support/SmartApp/" #macos
    elif sys.platform.startswith('linux'):
        dir = "/usr/local/home/SmartApp" #linux
    else:
        print('Your OS "{} {}" is incompatible. This version supports Windows Vista and above, MacOS Catalina and above and/or Ubuntu 20.04LTS / similar and above.'.format(platform.system(),platform.release()))
        sys.exit()

    shouldSignIn = False
    if not os.path.exists(dir):
        os.makedirs(dir)

    def tryLog(log):
        if log == True:
            logging.basicConfig(filename=dir+'\\log_{}.log'.format(datetime.strftime('%x_%X')))
        else:
            pass

    try:
        with open(dir+'\\settings.json', 'r') as logEnable:
            jsonLog = json.load(logEnable)
            if jsonLog['log'] == False or jsonLog['log'] == "false":
                log = False
            else:
                tryLog(True)
    except:
        pass

    try:
        with open(dir+'\\settings.json','r') as term:
            ifTerminalError = json.loads(term.read())
            if ifTerminalError['useCmdIfTerminalError'] == False:
                useCmdIfTerminalError = False
            else:
                useCmdIfTerminalError = True
    except:
        pass

    def fileMaker(username, password):
        try:    
            key = Fernet.generate_key()
            fernet = Fernet(key)
            with open(dir+'\\1Df0tcw59R.enc', 'wb+') as key_:
                key_.write(key)
                key_.close()
            if username == None and password == None:
                setup()
                
            elif password == None:
                with open(dir+'\\encU.enc' ,'wb+') as encU:
                    encUsername = fernet.encrypt(username.encode())
                    encU.write(encUsername)
                    encU.close()
            else:
                with open(dir+'\\encU.enc' ,'wb+') as encU:
                    encUsername = fernet.encrypt(username.encode())
                    encU.write(encUsername)
                    encU.close()

                with open(dir+'\\encP.enc' ,'wb+') as encU:
                    encPassword = fernet.encrypt(password.encode())
                    encU.write(encPassword)
                    encU.close()
        except Exception as fileMakerError:
            print('Failed to make file. Reason: %s' % fileMakerError)

    def tryClear():
        try:
            os.system('cls')
        except:
            os.system('clear')

    def terminal(command):
        tryClear()
        command = command.lower()
        with open(dir+'\\settings.json','r') as term:
            ifTerminalError = json.loads(term.read())
            if ifTerminalError['useCmdIfTerminalError'] == False:
                useCmdIfTerminalError = False

            else:
                useCmdIfTerminalError = True

        availableCommands = [
            'GENERAL COMMANDS:\r\n'
            'Exit: Exits the terminal and returns you back to the main app\r\n'
            'Help: Displays this section'
            '\r\nHELPFUL COMMANDS:\r\n'
            'Exec [parameter]: Executes an app that you specified. E.G: exec c:\\Program Files\\Google\\Chrome\\Application\\chrome.exe |or| exec Chrome\r\n'
            'Del [parameter]: Deletes files that you specify. E.G: del %homedrive%\\SmartApp'
            '\r\nMORE COMING SOON\r\n'
        ]

        if 'exit' in command:
            mainApp()

        elif 'help' in command:
            for i in availableCommands:
                print(i)
                terminal(input('Enter command: '))

        elif 'exec' in command:
            try:
                cmd, param, options = command.split()

                if '/' in options:
                    os.system('start {} {}'.format(param - ' ', options))
                elif '/?' in options: 
                    os.system('start {} /?'.format(param - ' '))

                else:
                    os.system('start {}'.format(param - ' '))
                    terminal(input('Enter command: '))
            except:
                try:
                    cmd, param = command.split()
                    os.startfile(param)
                    terminal(input('Enter command: '))
                except Exception as error:
                    print(error)
                    terminal(input('Enter command: '))

        elif 'del' in command:
            try:
                temp, path_ = command.split()
                path = glob.glob(path_)
                for f in path:
                    os.remove(f)

                terminal(input('Deleting successful. Enter command: '))
            
            except Exception as delError:
                if Exception == IndexError:
                    print('Deleting failed. Please make sure you have entered a valid parameter.')
                    terminal(input('Enter command: '))
                else:
                    print(delError)
                    terminal(input('Deleting failed. Enter command: '))

        else:
            if useCmdIfTerminalError == True:
                try:
                    os.system(command)
                except:
                    terminal(input('Invalid command. Please enter another command: '))
            else:
                terminal(input('Invalid command. Please enter another command: '))
    
    def reset():
        tryClear()
        confirm = input('Are you sure you would like to reset this app. This will remove all preferences and credentials. This is unchangeable. Continue? (y/n)').lower()
        if confirm == 'y':
            pass
        else:
            print('Okay. No changes will be made. ')

        print('Okay. Resetting...')
        try:
            try:
                fileHandles = [open(dir+'\\1Df0tcw59R.enc'),open(dir+'\\encU.enc'),open(dir+'\\encP.enc'), open(dir+'\\settings.json')]
                for file in fileHandles:
                    try:
                        file.close()
                    except Exception:
                        pass

            except:
                fileHandles = [open(dir+'\\1Df0tcw59R.enc'),open(dir+'\\encU.enc'), open(dir+'\\settings.json')]
                for file in fileHandles:
                    try:
                        file.close()
                    except Exception:
                        pass

            os.system('rmdir /s /q "%appdata%/SmartApp"')
            print('Reset successfully. You can restart the app manually from where it is downloaded. Thanks for using my app!')
            sys.exit()
        except Exception as resetErr:
            print('Failed to reset. No changes have been made. Reason: {}.'.format(resetErr))
            sys.exit()

    def changeSettings():
        tryClear()
        try:
            jsonFile = open(dir+'\\settings.json','r')
            data = json.load(jsonFile)
            jsonFile.close()
            changeSetting = input('Your settings are currently {}. Which setting would you like to change?'.format(json.dumps(data, sort_keys=False, indent=4))).lower()
            updateSetting = input('What would you like to change the setting too: ').lower()
            if updateSetting == 'true':
                data[changeSetting] = updateSetting
                updateSetting = bool(True)
                jsonFile = open(dir+'\\settings.json','w+')
                jsonFile.write(json.dumps(data, indent=4, sort_keys=False))
                jsonFile.close()
                print('Successfully changed the setting!')
                mainApp()
            elif updateSetting == 'false':
                data[changeSetting] = updateSetting
                updateSetting = bool(False)
                jsonFile = open(dir+'\\settings.json','w+')
                jsonFile.write(json.dumps(data, indent=4, sort_keys=False))
                jsonFile.close()
                print('Successfully changed the setting!')
                mainApp()
            else:
                jsonFile = open(dir+'\\settings.json','w+')
                jsonFile.write(json.dumps(data, indent=4, sort_keys=False))
                jsonFile.close()
                print('Successfully changed the setting!')
                mainApp()
        except Exception as cSError:
            print('Error:', cSError)

    def mainApp():
        tryClear()

        if not os.path.exists(dir+'\\settings.json'):
            settings = {'ver':'1.0.1', 'useCmdIfTerminalError':False, 'log':False}
            with open(dir+'\\settings.json','w+') as jWrite:
                jWrite.write(json.dumps(settings, indent=4, sort_keys=False))
                jWrite.close()

        else:
            with open(dir+'\\settings.json','r') as jRead:
                jRead.read()

        choice = input('To use a simple calculator, enter "1".\r\nTo execute any installed Windows app from here, enter "2".\r\nTo use my custom-made terminal, enter "3" *Pre-Alpha*.\r\nTo play music, enter "4".\r\nTo change settings, enter "5".\r\nTo reset this app, enter "reset": ')
        if choice == '1':
            calc = input('Enter calculation. ')
            print('The answer to {} is {}. '.format(calc, eval(calc)))
            os.system('pause')
            mainApp()

        elif choice == '2':
            try:
                import winapps
                appToRun = input('Enter app you want too start. ')
                print('Thanks. Trying to execute now... ')
                for app in winapps.search_installed(appToRun):
                    try:
                       os.system('start %s' % appToRun)
                       mainApp()
                    except:
                        try:
                            os.system('start %s' % app.name)
                            mainApp()
                        except:
                            try:
                                os.system('start ''%s''' % app.install_location)
                                mainApp()
                            except Exception as execError:
                                print('Failed to execute program. Reason: %s' % execError)
                mainApp()
            except Exception as num2Err:
                print('Error: {}. '.format(num2Err))
                mainApp()

        elif choice == '3':
            try:
                tryClear()
                terminal(input('Enter command: '))
            except Exception as termError:
                print('Error: %s' % termError)
                mainApp()

        elif choice == '4':
            tryClear()
            import music
            music.youtube()

        elif choice == '5':
            tryClear()
            changeSettings()
        
        elif choice.lower() == 'reset':
            tryClear()
            reset()

        elif choice.lower() == 'exit':
            tryClear()
            print("Thanks for using my app.\r\nExiting...")
            quit()

        else:
            print('Invalid choice. ')
            time.sleep(1)
            mainApp()

    def signIn():
        tryClear()
        key = open(dir+'\\1Df0tcw59R.enc')
        fernet = Fernet(key.read())
        key.close()
        if not os.path.exists(dir+'\\encP.enc'):
            userEnteredUsername = input('Enter username. ')
            u_ = open(dir+'\\encU.enc','rb')
            u = u_.read()
            uDec = fernet.decrypt(u).decode()
            if userEnteredUsername == uDec:
                n_ = open(dir+'\\encU.enc','rb')
                n = n_.read()
                name = fernet.decrypt(n).decode()
                print('Welcome, {}!'.format(name))

                u_.close()
                n_.close()

                mainApp()
            else:
                print(u, uDec)
        else:
            pass
        
        u_ = open(dir+'\\encU.enc','rb')
        u = u_.read()
        p_ = open(dir+'\\encP.enc','rb')
        p = p_.read()

        un = input('Enter username. ')
        pswd= input('Enter password. ')

        uDec = fernet.decrypt(u).decode()
        pDec = fernet.decrypt(p).decode()

        if uDec == un:
            if pDec == pswd:
                fernet_ = open(dir+'\\1Df0tcw59R.enc')
                fernet = Fernet(fernet_.read())
                n_ = open(dir+'\\encU.enc','rb')
                n = n_.read()
                name = fernet.decrypt(n).decode()
                fernet_.close()
                print('Welcome, {}!'.format(name))

                u_.close()
                p_.close()
                n_.close()

                mainApp()
            else:
                print('Invalid credentials.')
                signIn()
        else:
            print('Invalid credentials.')
            signIn()

    def setup():
        tryClear()
        username = input('Welcome to the setup! First, enter username. ')
        if len(username) == 0:
            print('Please enter a username. ')
            setup()
        else:
            pass

        password = input('Thanks. Next, enter a secure password. ')
        
        if len(password) == 0:
            choicePswd = input('You did not enter a password. This is not recommended as this is less secure. Do you wish too proceed? Y/N. ')
            if choicePswd.lower() == 'n':
                print('Okay. ')
                setup()
            else:
                print('Okay. You will not have a password for your user. ')
                fileMaker(username, password=None)
                    
                signIn()
                pass

        fileMaker(username, password)

        if os.path.exists(dir+'\\encU.enc'):
            if os.path.exists(dir+'\\encP.enc'):
                print('Success! Please sign-in.')
                signIn()
            else:
                print('Something went wrong. Please try again.')
                setup()
        else:
            print('Something went wrong. Please try again.')
            setup()

    if shouldSignIn == False:
        mainApp()
    else:
        pass

    while True:
            if __name__ == '__main__':
                if not os.path.exists(dir):
                    os.makedirs(dir)
                    setup()
                else:
                    try:
                        with open(dir+'\\1Df0tcw59R.enc', 'rb') as testKey:
                            testKey.read()
                            testKey.close()
                            if os.path.exists(dir+'\\encU.enc'):
                                signIn()
                            else:
                                setup()

                    except:
                        fileMaker(None, None)
                        if os.path.exists(dir+'\\encU.enc'):
                            signIn()
                        else:
                            setup()


except Exception as gen:
    print('An error has occured. Here are the details: {} %s'.format(gen) % traceback.format_exc())