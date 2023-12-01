# coding: latin-1
import Tkinter as Tk
import mmap
import os
import shutil
import re
import Image
from tkFileDialog   import askopenfilename      
class App:
	def callbackfile(self):
		fn=askopenfilename() 		
		self.logit("check file: "+fn+"\n")
		if not os.path.isfile(fn):
			self.logit("no file"+fn+"\n")
		else:
			f=open(fn, "r+b")
			map = mmap.mmap(f.fileno(), 0)
			hexstr=" "+" ".join(["%02X"%ord(x) for x in map])
			check=1
			self.fn=None
			self.logit("search... \n")
			for i in range(5):
				pdata=self.posdata["pos"+str(i)]
				cnt=hexstr.count(pdata[0])
				self.logit("test1."+str(i)+" =>"+str(cnt)+" "+pdata[0].replace(" ","")+" \n")
				spos=0
				if cnt!=1:
					check=0
				else:
					spos=(hexstr.index(pdata[0])/3)+(len(pdata[0])/3)
					for r in range(len(self.res)):
						self.logit("res"+str(r+2)+" "+repr([sum([256**x[0]*ord(x[1]) for x in enumerate(map[spos+pdata[1+r*2]:spos+pdata[1+r*2]+2])]) ,sum([256**x[0]*ord(x[1]) for x in enumerate(map[spos+pdata[2+r*2]:spos+pdata[2+r*2]+2])])])+"\n")
			for i in range(2):
				cnt=hexstr.count(self.posdata["more"+str(i)][0])
				if cnt!=1:check=0
				self.logit("test2."+str(i)+" =>"+str(cnt)+" "+self.posdata["more"+str(i)][0].replace(" ","")+"\n")
			self.logit("check : "+str(check)+"  [0=fail, 1=ok] \n")
			if check:
				self.fn=fn		
			map.close()
			f.close()		
	def logit(self,txt):
		self.ltext.config(state=Tk.NORMAL)
		self.ltext.insert(Tk.END ,txt)
		self.ltext.config(state=Tk.DISABLED)
	def __init__(self, master):
		self.res=[[1024,768],[1280,1024]]
		self.fn=None
		frame = Tk.Frame(master)
		frame.pack()
		#self.button = Tk.Button(frame, text="QUIT", fg="red", command=frame.quit)
		#self.button.pack(side=Tk.LEFT)
		self.fbutton = Tk.Button(frame, text='select Patrizer.exe', command=self.callbackfile)
		self.fbutton.pack()
		self.ltext = Tk.Text(frame)
		self.ltext.pack()	
		self.logit("Log\n")
		self.nfile = Tk.Frame(frame)
		self.flabel = Tk.Label(self.nfile,text="new Name:")
		self.flabel.pack(side=Tk.LEFT)
		self.fname = Tk.Entry(self.nfile)
		self.fname.pack(side=Tk.LEFT)
		self.nfile.pack()
		self.res1 = Tk.Frame(frame)
		self.lx1 = Tk.Label(self.res1, text="Res2: X-",)
		self.lx1.pack(side=Tk.LEFT)
		self.ex1 = Tk.Entry(self.res1)
		self.ex1.pack(side=Tk.LEFT)
		self.ly1 = Tk.Label(self.res1, text="Y-")
		self.ly1.pack(side=Tk.LEFT)
		self.ey1 = Tk.Entry(self.res1)
		self.ey1.pack(side=Tk.LEFT)
		self.res1.pack()
		self.res2 = Tk.Frame(frame)
		self.lx2 = Tk.Label(self.res2, text="Res3: X-",)
		self.lx2.pack(side=Tk.LEFT)
		self.ex2 = Tk.Entry(self.res2)
		self.ex2.pack(side=Tk.LEFT)
		self.ly2 = Tk.Label(self.res2, text="Y-")
		self.ly2.pack(side=Tk.LEFT)
		self.ey2 = Tk.Entry(self.res2)
		self.ey2.pack(side=Tk.LEFT)
		self.res2.pack()
		self.fname.insert(Tk.END,"newPatrizier.exe")
		self.ex1.insert(Tk.END,self.res[0][0])
		self.ey1.insert(Tk.END,self.res[0][1])
		self.ex2.insert(Tk.END,self.res[1][0])
		self.ey2.insert(Tk.END,self.res[1][1])
		self.l5 = Tk.Label(frame, text="-->")
		self.l5.pack(side=Tk.LEFT)
		self.fwrite = Tk.Button(frame, text="Go",fg="red", command=self.fwrite)
		self.fwrite.pack(side=Tk.LEFT)
		self.posdata=dict(
		pos0=[" C7 44 24 4C 20 03 00 00 C7 44 24 50 58 02 00 00 EB 2A 3C 01 75 12 C7 44 24 4C",0,8,0x16,0x1e],
		pos1=[" C7 44 24 18 20 03 00 00 C7 44 24 1C 58 02 00 00 EB 2C 83 FE 01 75 12 C7 44 24 18",0,8,0x17,0x1f],
		pos2=[" C7 44 24 3C 20 03 00 00 C7 44 24 40 58 02 00 00 EB 22 C7 44 24 3C",0x12,0x1a,0,8],
		pos3=[" C7 44 24 48 20 03 00 00 C7 44 24 4C 58 02 00 00 EB 2B 83 F8 01 75 12 C7 44 24 48",0,8,0x16,0x1e],
		pos4=[" C7 44 24 24 20 03 00 00 C7 44 24 28 58 02 00 00 EB 2C 83 F8 01 75 12 C7 44 24 24",0,8,0x17,0x1f],
		more0=[" E8 FB B0 08 00 8B 0D A4 B0 6C 00 E8 90 76 FD FF A1 80 B2 6D 00 3D 20 03 00 00 0F 84 62 01 00 00 3D",0,-1,0xb,-1],
		more1=[" 90 90 90 90 90 90 90 90 90 90 90 A1 80 B2 6D 00 83 EC 1C 3D 20 03 00 00 53 55 56 57 8B F1 74 3C 3D",0,-1,7,-1],
		)
		self.files={'accelMap.ini':"",'screenGame.ini':"",'textures.ini':""}
		for fn in self.files:
			f=open("data"+os.sep+fn,"r")
			self.files[fn]=f.readlines()
			f.close
		self.convini={
		'screenGame.ini':{
		0:[
		['[ANIM41]',-3,lambda x:"Frame0=10 0 0 0 0 "+str(x[0]-284)+" 42 0\n"],
		['[ANIM43]',-3,lambda x:"Frame0=8 0 0 0 0 284 "+str(284+(x[1]-768))+"\n"],
		['[ANIM43]',-7,lambda x:"Pos="+str(x[0]-284)+" 600\n"]
		],
		1:[
		['[ANIM42]',-3,lambda x:"Frame0=11 0 0 0 0 "+str(x[0]-284)+" 42\n"],
		['[ANIM44]',-3,lambda x:"Frame0=9 0 0 0 0 284 "+str(424+(x[1]-1024))+"\n"],
		['[ANIM44]',-7,lambda x:"Pos="+str(x[0]-284)+" 600\n"]
		]
		},
		'accelMap.ini':{
		0:[
		['[SCREEN1]',-2,lambda x:"Size="+str(x[0])+" "+str(x[1])+"\n"],
		['[ANIM1]',-3,lambda x:"Frame0=30023 0 0 0 0 "+str(x[0])+" "+str(x[1])+" 0\n"]
		],
		1:[
		['[SCREEN2]',-2,lambda x:"Size="+str(x[0])+" "+str(x[1])+"\n"],
		['[ANIM2]',-3,lambda x:"Frame0=30024 0 0 0 0 "+str(x[0])+" "+str(x[1])+" 0\n"]
		]
		},
		'textures.ini':{
		0:[['[TEX30023]',-4,lambda x:"OffsetNSize0=0 0 "+str(x[0])+" "+str(x[1])+"\n"]],
		1:[['[TEX30024]',-4,lambda x:"OffsetNSize0=0 0 "+str(x[0])+" "+str(x[1])+"\n"]]
		}
		}
	def fwrite(self):
		check=1
		if not self.fn:
			self.logit("select patrizer.exe!\n")
			check=0
		if len([x for x in [self.ex1.get(),self.ex2.get(),self.ey1.get(),self.ey2.get()] if not re.search("^[0-9][0-9]*$",x)])==0 :
			if not len([x for x in [self.ex1.get(),self.ex2.get(),self.ey1.get(),self.ey2.get()] if not 100<=int(x)<=9999])==0 :
				self.logit("100<= Res X/Y <=9999 !\n")
				check=0
		else:
			self.logit("only numbers ins Res X/Y!\n")
			check=0
		if not re.search("^[0-9a-zA-Z._-]*$",self.fname.get()):
			self.logit("new filename = alphanumeric and -._ \n")
			check=0
		if check:
			ppath=os.sep.join(os.path.realpath(self.fn).split(os.sep)[0:-1])
			nfn=ppath+os.sep+self.fname.get()
			self.res[0][0]=int(self.ex1.get())
			self.res[0][1]=int(self.ey1.get())
			self.res[1][0]=int(self.ex2.get())
			self.res[1][1]=int(self.ey2.get())
			shutil.copyfile(self.fn,nfn)
			f=open(nfn, "r+b")
			map = mmap.mmap(f.fileno(), 0)
			hexstr=" "+" ".join(["%02X"%ord(x) for x in map])			
			spos=[]
			for i in range(5):
				pdata=self.posdata["pos"+str(i)]
			#	print pdata[0]
				spos.append((hexstr.index(pdata[0])/3)+(len(pdata[0])/3))
			for i in range(5):
				pdata=self.posdata["pos"+str(i)]
			#	print "%X"%spos[i]
			#	print hexstr.count(pdata[0])
				for r in range(len(self.res)):
			#		print ["%02X"%ord(x) for x in map[spos[i]+pdata[1+r*2]:spos[i]+pdata[1+r*2]+2]] ,["%02X"%ord(x) for x in map[spos[i]+pdata[2+r*2]:spos[i]+pdata[2+r*2]+2]]
					map[spos[i]+pdata[1+r*2]  ]=chr(self.res[r][0]%256)
					map[spos[i]+pdata[1+r*2]+1]=chr(self.res[r][0]/256)
					map[spos[i]+pdata[2+r*2]  ]=chr(self.res[r][1]%256)
					map[spos[i]+pdata[2+r*2]+1]=chr(self.res[r][1]/256)
			if self.res[1][0]>=1280:
				self.logit("write data for res>=1280 \n")
				for i in range(2):
					pdata=self.posdata["more"+str(i)]
					spos=(hexstr.index(pdata[0])/3)+(len(pdata[0])/3)
					map[spos+pdata[3]  ]=chr(self.res[1][0]%256)
					map[spos+pdata[3]+1]=chr(self.res[1][0]/256)
				self.logit("resize pictures for res >=1280 \n")
				if1 = Image.open("data"+os.sep+"Vollansichtskarte.bmp")
				if1n = if1.resize((self.res[1][0], self.res[1][1]), Image.ANTIALIAS)
				if1n.save(ppath+os.sep+"images"+os.sep+"Vollansichtskarte1280.bmp")
				if2 = Image.open("data"+os.sep+"HauptscreenE.bmp")
				if2n = if2.resize((284, 424-1024+self.res[1][1]), Image.ANTIALIAS)
				if2n.save(ppath+os.sep+"images"+os.sep+"HauptscreenE1280.bmp")
			map.close()
			f.close()		
			self.logit("writing to newfile done \n")
			if not os.path.isdir(ppath+os.sep+'images'):
				os.makedirs(ppath+os.sep+'images')
				self.logit("creating images dir \n")
			if not os.path.isdir(ppath+os.sep+'scripts'):
				os.makedirs(ppath+os.sep+'scripts')
				self.logit("creating script dir \n")
			self.logit("write script files \n")
			for fn in self.convini:
				txt=""
				for li in range(len(self.files[fn])):
					found=-1
					for r in range(len(self.res)):
						for cn in self.convini[fn][r]:
							if self.files[fn][li+cn[1]].startswith(cn[0]):				
								txt+=cn[2](self.res[r])
								#print files[fn][li],files[fn][li],cn[2](nres)
								found=r
					if found==-1:
						txt+=self.files[fn][li]
				f=open(ppath+os.sep+'scripts'+os.sep+fn,"w")
				f.write(txt)
				f.close()		
			self.logit("done \n")
root = Tk.Tk()
app = App(root)
root.mainloop()