import seqcompare 
su='revbarcodeid.csv'
_={}
with open(su) as d:
	next(d)
	for line in d:
		stuff=line.rstrip().split(',')
		id=stuff[0]
		seq=stuff[1]
		_[seq]=id
d.close()

seqlist=_

def oseqin(x,op=0):
	if x in seqlist:
		r=True
		r1=seqlist[x]
	else:
		r=False
		r1='None'
	if op==1:
		return r1
	return r
bases=['A','C','T','G']

def oseqin2(barcode,op=0):
	barcode=barcode.upper()
	count157=0
	genedict=[]
	glist=[]
	while count157 <= 11:
		basec=0
		basedict=[]
		while basec <=3:
			__o=list(barcode)
			__o[count157]=bases[basec]
			tbarcode=''.join(__o)
			basec+=1
			if tbarcode not in seqlist:
				glist.append(0)
				pass
			else:
				wo=seqcompare.seqin(tbarcode,seqlist)[1]
				basedict.append(wo)
				glist.append(wo)
		count157+=1
	if seqcompare.seqone(glist):
		pos8=glist.index(1)
		pos8+=1
		n1=pos8 / 4
		r1=pos8 % 4
		if r1!=0:
			n1+=1
		r1-=1
		p12=n1-1
		b12=bases[r1]
		_r=list(barcode)
		_r[p12]=b12
		barcode="".join(_r)
	if op==1:
		if barcode in seqlist:
			return seqlist[barcode]
		elif barcode not in seqlist:
			return 'None'
		else:
			return IOError('something was wrong')
	if barcode not in seqlist:
		return False
	elif barcode in seqlist:
		return True
	else:
		return IOError('something was wrong')

def lseqin(x,op=0):
	if len(x)!=11:
		raise IOError('Wrong Usauge 11nt long only')
	x=x.upper()
	barcode=x
	count157=0
	genedict=[]
	glist=[]
	tarlist=[]
	while count157 <= 11:
		basec=0
		basedict=[]
		while basec <=3:
			__o=list(barcode)
			__o.insert(count157,bases[basec])
			tbarcode=''.join(__o)
			basec+=1
			
			if tbarcode not in seqlist:
				glist.append(0)
				pass
			elif tbarcode in tarlist:
				glist.append(0)
			else:
				wo=seqcompare.seqin(tbarcode,seqlist)[1]
				basedict.append(wo)
				glist.append(wo)
			tarlist.append(tbarcode)
		count157+=1
	if seqcompare.seqone(glist):
		pos8=glist.index(1)
		pos8+=1
		n1=pos8 / 4
		r1=pos8 % 4
		if r1!=0:
			n1+=1
		r1-=1
		p12=n1-1
		b12=bases[r1]
		_r=list(barcode)
		_r.insert(p12,b12)
		barcode="".join(_r)
	if op==1:
		if barcode in seqlist:
			return seqlist[barcode]
		elif barcode not in seqlist:
			return 'None'
		else:
			return IOError('something was wrong')
	if barcode not in seqlist:
		return False
	elif barcode in seqlist:
		return True
	else:
		return IOError('something was wrong')
		
def dseqin(x,op=0):
	if len(x)!=13:
		raise IOError('Wrong Usauge 13nt long only')
	x=x.upper()
	barcode=x
	count157=0
	genedict=[]
	glist=[]
	tarlist=[]
	while count157 <= 12:
		basedict=[]
		__o=list(barcode)
		del __o[count157]
		tbarcode=''.join(__o)
		if tbarcode not in seqlist:
			glist.append(0)
			pass
		elif tbarcode in tarlist:
			glist.append(0)
		else:
			wo=seqcompare.seqin(tbarcode,seqlist)[1]
			basedict.append(wo)
			glist.append(wo)
		tarlist.append(tbarcode)
		count157+=1
	if seqcompare.seqone(glist):
		pos8=glist.index(1)
		pos8+=1
		n1=pos8
		p12=n1-1
		_r=list(barcode)
		del _r[p12]
		barcode="".join(_r)
	if op==1:
		if barcode in seqlist:
			return seqlist[barcode]
		elif barcode not in seqlist:
			return 'None'
		else:
			return IOError('something was wrong')
	if barcode not in seqlist:
		return False
	elif barcode in seqlist:
		return True
	else:
		return IOError('something was wrong')
		
def boseqin(x): #test if 11,12,13 barcode match or not
	if len(x)==12:
		r=oseqin(x)
		if r:
			return True
		elif not r:
			w=oseqin2(x)
			return w
		else:
			return False
	elif len(x)==11:
		r=lseqin(x)
		return r
	elif len(x)==13:
		r=dseqin(x)
		return r
	else:
		raise IOError('Something bad happened')
		
def matchid(x):
	if len(x)==12:
		r=oseqin(x,1)
		if r!='None':
			return r
		else:
			w=oseqin2(x,1)
			return w
	elif len(x)==11:
		r=lseqin(x,1)
		return r
	elif len(x)==13:
		r=dseqin(x,1)
		return r
	else:
		raise IOError