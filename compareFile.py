
tmpBuffer1 =""
tmpBuffer2 = ""

tmpBuffer1 += open("/tmp/inf3200/asv009/test.zip" , 'r').read()
tmpBuffer2 += open("/tmp/inf3200/asv009/worm.zip", 'r').read()

i = 0
for line1 in tmpBuffer1:
	line2 = tmpBuffer2[i]
	if line1 != line2:
		print "Got an different file: " + str(i)
		print line1
		print line2
	i += 1

new_file = open("/tmp/inf3200/asv009/test2.zip", 'w')
new_file.write(tmpBuffer2)
new_file.close()
