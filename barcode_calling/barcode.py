import sys,string
print sys.argv
input=sys.argv[1]
#print sys.argv
output=sys.argv[2]
#print sys.argv
option=sys.argv[3]
#print sys.argv
stuffoption=sys.argv[4]
#print sys.argv
sup=output+'info'
useless=output+'nobarcode'

uless=open(useless,'w')
yu=open(output,'w')
f=open(input)
gh=open(sup,'w')

i=0
i+=1
count=0
print 'stuffoption:', stuffoption
if stuffoption=='r2':
	import seqanaly as aseq
	firstbound='ATG'
	secondbound='CTGCAG'
elif stuffoption=='r1':
	import revseqanaly as aseq
	firstbound='CTGCAG'
	secondbound='CAT'
total=0
addstuff=len(firstbound)
secondaddstuff=len(secondbound)
eleven=0
twelve=0
thirteen=0
twelveplus=0
bases=['A','C','T','G','N']
count=0
for line in f:
	count+=1
	if (count % 100,000)==0:
		print count
	id=line
	seq=f.next()
	plussign=f.next()
	qscore=f.next()
	k=str(seq.rstrip().upper())
	s=0
	total+=1
	first1=[]
	last1=[]
	while firstbound in k[s:]:
		b1=string.find(k,firstbound,s)
		first1.append(b1)
		s=b1+addstuff
	s2=0
	while secondbound in k[s2:]: 
		b1=string.find(k,secondbound,s2)
		last1.append(b1)
		s2=b1+secondaddstuff
	numbercount=0
	lob=[]
	plob=[]
	for thing1 in first1:
		for thing2 in last1:
			sb=thing1+addstuff
			eb=thing2
			length1=eb-sb
			if length1 <=13 and length1 >=11:
				bcode=k[sb:eb]
				if aseq.boseqin(bcode):
					numbercount+=1
					lob.append(bcode)
					plob.append(sb+1)
	if numbercount==1:
		count+=1
		r=lob[0]
		barcodel=len(r)
		if barcodel==11:
			eleven+=1
		elif barcodel==12:
			if r in aseq.seqlist:
				twelve+=1
			else:
				twelveplus+=1
		elif barcodel==13:
			thirteen+=1
		else:
			raise IOError
		r1=firstbound+r+secondbound
		result=str(total)+','+k+','+r1+','+str(barcodel)+','+aseq.matchid(r)
		predist=plob[0]
		if stuffoption.lower()=='r2':
			truedist=int(predist)-3
		elif stuffoption.lower()=='r1':
			prelength=len(k)
			prestuff=prelength+1
			enddist=prestuff-int(predist)
			truedist=enddist-barcodel+1-3
		result+=','+str(truedist)
		result+='\n'
		yu.write(result)
	else:
		leftover=str(total)+','+k+'\n'
		uless.write(leftover)
			
print count

yu.close()
uless.close()
f.close()

uncount=total-count
inforesult='No Barcode: '+str(uncount)+'\n'
inforesult+='11mer barcode: '+str(eleven)+'\n'+'12mer perfect barcode: '+str(twelve)+'\n'+'12mer mutated barcode: '+str(twelveplus)+'\n'+'13mer barcode: '+str(thirteen)+'\n'+'Total: '+str(total)
try:
	
	gh.write(inforesult)
finally:
	gh.close()