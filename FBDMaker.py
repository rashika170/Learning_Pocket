import cv2                                                                               
import os                                            
import numpy as np
import re
import math
import easyocr as ey
import sys

def slope(p1,p2):
        return (p2[1] - p1[1])/(p2[0] - p1[0])
#'C:\Users\suyash\Desktop\KACHRA\laohub\Ajgar\FROST HACK\Frost Hack Video\Shape34.png'

sys.stdout.write("Please enter the final location: ")
link =  sys.stdin.readline()
img1 = cv2.imread(link[:-1])
img = cv2.resize(img1,(500,500),interpolation=cv2.INTER_AREA)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 150, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
contours, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

lianother = []
liobj = []
text = []
i= -1

#Text detection using Easy-OCR library
reader = ey.Reader(['en'])
texteasy = reader.readtext(thresh1)


file = open("recognized.txt", "a")
for i in range(len(texteasy)):
    text1 = texteasy[i][1]
    file.write(str(text1))
    text.append([int(texteasy[i][0][0][0]),int(texteasy[i][0][0][1]),int(texteasy[i][0][2][0]) - int(texteasy[i][0][0][0]),int(texteasy[i][0][2][1]) - int(texteasy[i][0][0][1]),text1])

file.close()

def locat():
    sys.stdout.write("Please enter the location where you would like to save thic file")
    loc = sys.stdin.readline()[:-1]
    if os.path.isdir(loc) is True:
        return loc
    else : 
        print("enter a correct Folder")
        locat()

blank = np.zeros(img.shape, dtype='uint8')
hgt = img1.shape[0]
wdt = img1.shape[1]

if hgt>500 & wdt>500:
    img = cv2.resize(img1, (700,700), interpolation = cv2.INTER_AREA)
else:
    img = cv2.resize(img1, (700,700), interpolation=cv2.INTER_CUBIC) 

blank = np.zeros(img.shape, dtype='uint8')          
eli = []

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
arr = np.array(gray)

_, threshold = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(
	threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(blank, contours, -1, (0,0,255), 1)

i = 0
sumt = []
liobj =[]

for contour in contours:
    sumx = 0
    sumy = 0
    minx = 1000
    miny = 1000
    maxx = 0
    maxy = 0
    minimum = []
    maximum = []
    
    Area = cv2.contourArea(contour)
    if Area > 5000:
        if i == 0:
            i = 1                #Ye part samj nahi aya
            continue

        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        liobj.append([x,y])   
        
        xc, yc, wc, hc = cv2.boundingRect(contour)
        lianother.append([xc,yc,xc+wc,yc+hc,int(0)])

        eli.append(Area)

        if len(approx) == 3:
            cv2.drawContours(img, [contour], 0, (0, 0, 255), 1)
            # cv2.putText(img, 'Triangle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif len(approx) == 4:
            cv2.drawContours(img, [contour], 0, (0,255, 255), 1)
            # cv2.putText(img, 'Quadrilateral', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255, 255), 2)           
        elif len(approx) == 5:
            cv2.drawContours(img, [contour], 0, (0, 255,0), 1)
            # cv2.putText(img, 'Pentagon', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0, 255),2)
        elif len(approx) == 6:
            cv2.drawContours(img, [contour], 0, (0, 0, 255), 1)
            # cv2.putText(img, 'Hexagon', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif len(approx) == 8:
            cv2.drawContours(img, [contour],0, (255,0,0), 1)
            # cv2.putText(img, 'Octagon', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0,0 ), 2)    
        else:
            cv2.drawContours(img, [contour], 0, ( 255, 255,0), 1)
            # cv2.putText(img, 'circle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, ( 255, 255,0), 2)

    elif 1000<Area<5000:
                app = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
                if 6<=len(app)<=10 :
                        for i in range(len(app)):

                                ex = app.ravel()[int(2*i)]
                                ey = app.ravel()[int(2*i+1)]
                                sumx = sumx + ex
                                sumy = sumy + ey
                                if minx>ex:
                                        minx =ex
                                if miny>ey:
                                        miny = ey
                                if maxx<ex:
                                        maxx = ex
                                if maxy<ey:
                                        maxy = ey  
                                side = int(len(app) - 1)
                                if i==side :
                                        
                                        cv2.circle(img,(sumx//(side+1),sumy//(side+1)) , 3, (0,255,0), thickness = -1)
                                        cv2.circle(img, ((minx+maxx)//2,(miny + maxy)//2) , 3, (0,255,0),thickness = -1) 
                                        cv2.circle(img, ((((maxx + minx)//2)+40),(miny + maxy)//2) , 3, (0,255,0),thickness = -1) 
                                        minimum.append([minx,miny])
                                        maximum.append([maxx,maxy])
                                        cv2.rectangle(img, (minx-15,miny-15), (maxx+15,maxy+15), (10,40,80), thickness = 1)
                                        cv2.line(img, ((minx+maxx)//2,(miny + maxy)//2),(sumx//(side+1),sumy//(side+1)), (255,120,30))
                                        cv2.line(img, ((minx+maxx)//2,(miny + maxy)//2),((((maxx + minx)//2)+40),(miny + maxy)//2), (255,120,30))
                                        p2 = ((minx+maxx)//2,(miny + maxy)//2)
                                        p3 = (sumx//(side+1),sumy//(side+1))
                                        p1 = ((((maxx + minx)//2)+40),(miny + maxy)//2)
                                        m1 = slope(p1,p2)
                                        m2 = slope(p3,p2)
                                        
                                        ang = (m1 - m2)/(1 + m1*m2)
                                        angle = math.atan(ang)
                                        angle = math.degrees(angle)
                                        

                                        if p2[0]>=p3[0] :
                                                if  p2[1]>=p3[1]:
                                                        cv2.putText(img, "Angle="+str(180 + angle)[:5], (minx-15,miny-20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (120,120,255))
                                                        cen = (maxx,maxy)
                                                        count = (minx, miny)
                                                        plus = (10,10)
                                                        sumt.append([sumx//(side+1),sumy//(side+1),minx,miny,maxx,maxy, float(str(180 + angle)[:6])])

                                                else: 
                                                        cv2.putText(img, "Angle="+str(180 + angle)[:6], (minx-15,miny-20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (120,120,255))
                                                        cen = (maxx, miny)
                                                        count = (minx, maxy)
                                                        plus = (10, -10)
                                                        sumt.append([sumx//(side+1),sumy//(side+1),minx,miny,maxx,maxy, float(str(180 + angle)[:6])])
                                        else :
                                                if p2[1]>=p3[1]:
                                                        cv2.putText(img,"Angle="+ str(angle)[:5], (minx-15,miny-20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (120,120,250))
                                                        cen = (minx, maxy)
                                                        count = (maxx,miny)
                                                        plus = (-10,10)
                                                        sumt.append([sumx//(side+1),sumy//(side+1),minx,miny,maxx,maxy, float(str(angle)[:5])])

                                                else: 
                                                        cv2.putText(img,"Angle="+ str(270 - angle)[:6], (minx-15,miny-20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (100,100,255))
                                                        cen = (minx,miny)
                                                        count = (maxx, maxy)
                                                        plus = (-10,-10)
                                                        sumt.append([sumx//(side+1),sumy//(side+1),minx,miny,maxx,maxy, float(str(270 -angle)[:6])])
                                        
                                        cv2.line(img, cen, (cen[0], count[1]), (255,0,255), thickness = 1)   
                                        cv2.line(img, cen, (count[0], cen[1]), (255,0,255), thickness = 1) 
                                        cv2.line(img, (count[0], cen[1]), (count[0] + plus[0], cen[1] + 10), (255,0,255), thickness = 1)
                                        cv2.line(img, (count[0], cen[1]), (count[0] + plus[0], cen[1] - 10 ), (255,0,255), thickness = 1)
                                        cv2.line(img, (cen[0], count[1]), (cen[0] - 10, count[1] + plus[1]), (255,0,255), thickness = 1)
                                        cv2.line(img, (cen[0], count[1]), (cen[0] + 10, count[1] + plus[1]), (255,0,255), thickness = 1)

                        cv2.circle(img, (minx,miny), 2, (10, 10,255),-1)                        
                        cv2.putText(img,"Arrow", (minx,miny -35), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,255))

for i in range(len(liobj)):
    w=0
    for x in range(len(liobj)-i):
        if (-10<liobj[i][0] -liobj[x+i-w][0] < 10) & (-10<liobj[i][1] - liobj[x+i-w][1]<10) & (x+i-w != i):
            liobj.remove(liobj[x+i-w])
            lianother.remove(lianother[x+i-w])
            eli.remove(eli[x+i-w])
            w= w+1

    ec = 0
    for x in range(len(liobj)):
        s = 0
        for cen in liobj:
            if (lianother[x-ec][0] < cen[0] < lianother[x-ec][0] + lianother[x-ec][2]) &  (lianother[x-ec][1] < cen[1] < lianother[x-ec][1] + lianother[x-ec][3]):
                s = s + 1
        if s >=3 :
            liobj.remove(liobj[x-ec])
            lianother.remove(lianother[x-ec])
            ec = ec +1
            eli.remove(eli[x-ec])           

w = 0
for i in range(len(text)):
    if text[i-w][4] == '\x0c' or text[i-w][4] == '\n\x0c' or text[i-w][4] == '':       #This noise removal code was fro tesseract
        text.remove(text[i-w])
        w = w+1

liobj = np.array(liobj)
liobj = liobj.reshape(int(len(liobj)),2)

lianother = np.array(lianother)
lianother = lianother.reshape(int(len(lianother)), 5)                                            #This is to find problem just before the merging of arrays
shape =  np.concatenate((liobj, lianother),axis = 1)
shape = shape.tolist()

for i in shape:
    x,y,_,_,_,ym,_ = i
    hc = ym - y
    img = cv2.line(img, (x,y), (x, y+int(hc/1.5)) , (255,0,0), 3)
    img = cv2.line(img, (x,y+int(hc/1.5)), (x-int(x/10),y+int(hc/1.8)),(255,0,0), 3)
    img = cv2.line(img, (x,y+int(hc/1.5)), (x+int(x/10),y+int(hc/1.8)) ,(255,0,0),3)
    img = cv2.putText(img, "mg", (x-20,y+int(hc/1.5)+20) ,cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,0,0), 1)
    img = cv2.line(img, (x,y), (x, y-int(hc/1.5)) , (0,0,255), 3)
    img = cv2.line(img, (x,y-int(hc/1.5)), (x+int(x/10),y-int(hc/1.8)),(0,0,255), 3)
    img = cv2.line(img, (x,y-int(hc/1.5)), (x-int(x/10),y-int(hc/1.8)) ,(0,0,255),3)
    img = cv2.putText(img, "N", (x-20,y-int(hc/1.5)-10) ,cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 1)

kilo = []
nor = []
e = 0
vari = []

for x in text:
    loc = x[4].upper().find("KG")
    locf = x[4].find("N")
    numd = x[4][:int(loc)]
    numf = x[4][:int(locf)]
    reco = re.compile('\D')
    n = reco.split(numd)
    f = reco.split(numf)    
    nkg = []
    nn = []
    for i in n:
        if i != '' and loc!= -1:
            nkg = i
    if nkg != []:       
        kilo.append([int((x[0]+ x[2]/2)*1.4), int((x[1] + x[3]/2)*1.4) ,int(nkg),"kg"]) 
    for i in f:
        if i != '' and locf!= -1:
            nn = i 
    if nn!=[]:
        nor.append([int((x[0]+ x[2]/2)*1.4), int((x[1] + x[3]/2)*1.4),int(nn),"N"])
    if nkg == [] and nn == []:
        vari.append(e)  
    e = e+1
variable = []
for i in vari:
    variable.append([int((text[i][0]+ text[i][2]/2)*1.4), int((text[i][1] + text[i][3]/2)*1.4),text[i][4],"vari"])

net = kilo + nor + variable
combo = shape + sumt

for x in combo:
    minxd = 10000
    w = -1
    s = None
    for i in net:
        xc = x[0] - i[0]
        yc = x[1] - i[1]
        dist = math.sqrt(xc*xc + yc*yc)
        w= w + 1
        if dist<minxd:
            minxd = dist
            s = w
    
    x.insert(-1,net[s][2])
    x.insert(-1,net[s][3])
        
class fbd():
    def __init__(self ,mass):
        self.mass = mass

final =[]
for i in range(len(combo)):
    if combo[i][-2] == "kg":
        final.append(combo[i])
    else:
        final.append(combo[i])

remove = []
for c,i in enumerate(final):
    if i[7] == "N" or i[7] == "vari":
        remove.append(c)
        w = 0
        num = 0
        count = 0
        for  x in final:
            count = count + 1
            if x[7] == "kg":
                xf = (x[0] - i[2])
                yf = (x[1] - i[3])
                xb = (x[0] - i[4])
                yb = (x[1] - i[5])

                distf = math.sqrt(xf*xf + yf*yf)
                distb = math.sqrt(xb*xb + yb*yb)

                if distf <= distb:
                    dist = distf
                else :
                    dist = distb
                if w!=0:
                    w = w-1
                    if mindist > dist:
                        mindist = dist
                        num  = count -1 
                else:
                    w = w-1
                    mindist = dist
                    num =0
            if count == len(final) - 1:     
                final[num].append(i[-3])
                final[num].append(i[-2])
                final[num].append(i[-1])                

for x in range(len(remove)):
    final.remove(final[remove[x] - x])

finalcom = []
unknowns = []

c=0
for x in final:
    y = int(len(x))
    if y >=10:
        eqx = 0 
        eqy = 0 
        for i in range(int((y-9)/3)):
            if x[10+(i*3)] == "N":
                xcom = (x[9+(i*3)])*(math.cos(math.radians(x[11+(i*3)])))
                ycom = (x[9+(i*3)])*(math.sin(math.radians(x[11+(i*3)])))
                eqx = eqx + xcom
                eqy = eqy + ycom
            elif x[10+(i*3)] == "vari":
                unknowns.append([c,x[9+(i*3)],x[11+(i*3)]])

        c = c+1
        finalcom.append([eqx,eqy])

normal = []
friction = []
i= 0

for up in final:
    nor = up[6]*10 - finalcom[i][1]
    j=-1
    frict = finalcom[i][0]
    for down in final:
        j = j+1
        if (up[2]<down[0]<up[4]) and (0<down[1]<up[3]) and i != j:
            nor = nor + down[6]*10 - finalcom[j][1]
            frict = frict + finalcom[j][0]
    i = i+ 1
    normal.append(float(str(nor)[:5]))
    if frict>0:
        friction.append(float(str(frict)[:5]))
    else:
        friction.append(float(str(frict)[:6]))


for c,i in enumerate(shape):
    x = i[0]
    img = cv2.putText(img, "   ="+str(i[6]*10)+" N", (i[0]-20,i[1]+int(i[5]-i[3])//2-10) ,cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,0,0), 1)
    img = cv2.putText(img, "  ="+str(normal[c])+" N", (i[0]-20,i[1]-int(i[5]-i[3])//2+20) ,cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 1)
    c=c+1

cof = []
for  i,x in enumerate(normal):
    coffof = friction[i]/x
    i = i+1
    cof.append(abs(float(str(coffof)[:5])))

for i,x in enumerate(friction):
    if x>0:
        img = cv2.line(img, (final[i][2], final[i][5]),(final[i][2] - 60, final[i][5]),(120,0,180),thickness = 2 )
        img = cv2.line(img, (final[i][2] - 60, final[i][5]), (final[i][2] - 50, final[i][5]+10),(120,0,180),thickness = 2 )
        img = cv2.line(img, (final[i][2] - 60, final[i][5]), (final[i][2] - 50, final[i][5]-10),(120,0,180),thickness = 2 )
        img = cv2.putText(img,str(x)+" N", (final[i][2]-130, final[i][5]),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,255),1)
        img = cv2.putText(img,"u="+str(cof[i]), (final[i][2]-100, final[i][1]),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)
    elif x==0:
        pass
    else:
        img = cv2.line(img, (final[i][4], final[i][5]),(final[i][4] + 100, final[i][5]),(120,0,180),thickness = 2 )
        img = cv2.line(img, (final[i][4] + 100, final[i][5]), (final[i][4]+ 90, final[i][5]+10),(120,0,180),thickness = 2 )
        img = cv2.line(img, (final[i][4] + 100, final[i][5]), (final[i][4] + 90, final[i][5]-10),(120,0,180),thickness = 2 )
        img = cv2.putText(img,str(abs(x)) + " N", (final[i][4]+110, final[i][5]),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,255),1) 
        img = cv2.putText(img,"u="+str(cof[i]), (final[i][4]+150, final[i][1]),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1) 
    i = i + 1
for c,i in enumerate(liobj):
    cv2.putText(img, str(c+1), (int(i[0]*0.7), int(i[1]*0.9)) ,cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
sys.stdout.write("Do you want to save the FBD made on your device(Y/N)")
choice = sys.stdin.readline()
choice = choice[0]
OLDDIR = os.getcwd()

if choice == "Y" or choice == 'y':
    sys.stdout.write("Please enter the folder name")
    filename = sys.stdin.readline()[:-1]
    NEWDIR = locat()
    NEWDIR = NEWDIR.replace("\\","/")

    os.chdir(NEWDIR)
    os.mkdir(filename)
    os.chdir(NEWDIR+r"/"+filename)
    cv2.imwrite("OUTPUT IMG.png", img)
    
    f = open("OUTPUT TXT.txt", 'w')

for i in range(len(finalcom)):
        INTRO = str("The analysis done on the "+str(i+1)+" figure :-\n")
        XCOMP = str("\nThe equivalent X-component is " + str(finalcom[i][0])[:5])
        YCOMP = str("\nThe equivalent Y-component is " +  str(finalcom[i][1])[:5])
        NORML = str("\nThe Normal Reaction is "+ str(normal[i]))
        FCOFF = str("\nThe minimum cofficient of friction to keep the system static: " + str(cof[i])+"\n\n")
        print(INTRO+XCOMP+YCOMP+NORML+FCOFF)    
        if choice == "Y" or choice == 'y':
            f.write(INTRO)
            f.write(XCOMP)
            f.write(YCOMP)
            f.write(NORML)
            f.write(FCOFF)

if choice == "Y" or choice == 'y':
    f.close()

os.chdir(OLDDIR)
os.remove("recognized.txt")
cv2.imshow("end", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
