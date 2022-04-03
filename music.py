import urllib.request, re, webbrowser

while True:
    try:
        search_keyword = input('Enter a song. Enter "exit" to exit the program: ').replace(" ", "+")
        if search_keyword.lower() == 'exit':
            import SmartApp
            SmartApp.signIn()
            quit()
        else:
            url = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", url.read().decode())
            result = 'https:\\www.youtube.com/watch?v=' + video_ids[0]
            webbrowser.open_new(result)
    except Exception as exceptionMusic:
        print('Error: %s' % exceptionMusic)
        break