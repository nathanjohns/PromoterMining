def nseqcompare(x,y):
	x=x.upper()
	y=y.upper()
	if len(x)!=len(y):
		return False
	else:
		for stuff in range(len(x)):
			if x[stuff]!=y[stuff]:
				if x[stuff]=='N' or y[stuff]=='N':
					pass
				else:
					return False
		return True

def seqcompare(x,y):
	x=x.upper()
	y=y.upper()
	if x==y:
		return True
	else:
		return False
		
def seqin(x,d):
	count=0
	b=0
	for thing in d:
		if seqcompare(x,thing):
			count+=1
			b=1
	if b==1:
		return True, count
	elif b==0:
		return False, count

def seqone(x):
	count=0
	for thing in x:
		if thing==1:
			count+=1
	if count==1:
		return True
	else:
		return False
		
