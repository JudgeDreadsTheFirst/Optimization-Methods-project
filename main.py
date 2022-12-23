"""code for optimization methods project"""
import sys

def read_data(filename):
    """writing all data into dictionary"""
    data = dict()
    with open(filename, "r", encoding = 'UTF-8') as f:
        for line in f:
            key = line.strip()
            if key == "":
                continue
            data[key] = []
            while (current_line := f.readline().strip()) != "/":
                data[key].append(tuple(float(val) for val in current_line.split()))
    return data

def check_input(filename,logFileName,ptl_test_enable):
    """some data checking function"""
    # checking TARG block
    with open(logFileName, 'w+', encoding = 'UTF-8') as log:
        blocks_dict = read_data(filename)
        expected_keys = ['TARG','PADS', 'TUBE', 'LIMI']
        keys = list(blocks_dict)
        error_str = '[ERROR]:'
        message_str = '[MESSAGE]:'
        warning_str = '[WARNING]:'
        if ptl_test_enable:
            expected_keys.append('PTL')
        if keys != expected_keys:
            log.write(' '.join([error_str,'not all data blocks presented in this file,','this blocks are missing',str(set(expected_keys).difference(set(keys))),'\n']))
            log.write(' '.join([message_str,'check process is executed','\n']))
            raise ValueError('[Error]:blocks missing')

        mass_t = blocks_dict.get('TARG')
        if len(mass_t) == 0:
            log.write(' '.join([error_str,str(keys[0]),'block, is empty','\n']))
            raise ValueError('[Error]:empty block')

        for i in range(len(mass_t)):
            if len(mass_t[i]) < 4:
                log.write('[ERROR]:')
                log.write('not enough params in ' + keys[0] + ' block, line[' + str(i+2) + ']' + ' line value:' + str(mass_t[i])+ '\n')
            elif mass_t[i][3] <= 0:
                log.write('[ERROR]:')
                log.write('price is not a positive number in ' + keys[0] + ' block, line[' + str(i+2) + ']' + ' line value:' + str(mass_t[i]) + '\n') 
          
            if len(mass_t[i]) >=3 and (mass_t[i][0] <0 or mass_t[i][1] < 0 or mass_t[i][2] < 0) :
                log.write('[ERROR]:')
                log.write('coordinate values or rad value are below zero in ' + keys[0] + ' block, line[' + str(i+2) + ']' + ' line value:' + str(mass_t[i]) + '\n') 
        
        pads = blocks_dict.get('PADS')
        if len(pads) == 0:
            log.write(' '.join([error_str,keys[1],'block, is empty','\n']))
            raise ValueError('[Error]:empty block')
        elif len(pads) > 1:
            log.write(' '.join([warning_str,keys[1],'block, has to many strings, using only one. It may cause an error','\n']))
        
        print('pads=',pads)
        for i in range(len(pads)):
            if len(pads[0]) < 2:
                log.write(' '.join([error_str,'missing price or number of pads in',keys[1],'block,line','['+str(len(mass_t)+2+i)+']',' line value:',str(pads[i]),'\n']))
            if len(pads[0]) > 2:
                log.write(' '.join([warning_str,'too much args in',keys[1],'block,line','['+str(len(mass_t)+2+i)+']',' line value:',str(pads[i]),'\n']))    
            if pads[0][0] <= 0 or pads[0][1] <= 0:
                log.write(' '.join([error_str,'price or number of pads are not a positive number',keys[1],'block,line','['+str(len(mass_t)+2+i)+']',' line value:',str(pads[i]),'\n']))   

        tube = blocks_dict.get('TUBE')
        if len(tube) == 0:
            log.write(' '.join([error_str,str(keys[2]),'block, is empty','\n']))
            raise ValueError('[Error]:empty block')
        elif len(tube) > 1:
            log.write(' '.join([warning_str,str(keys[2]),'block, has to many strings, using only one. It may cause an error','\n']))

        for i in range(len(tube)):
            if len(tube[0]) < 1:
                log.write(' '.join([error_str,'no values in',keys[2],'block,however line','['+str(len(mass_t)+2+i+len(pads)+2)+']','does not follow this rule',' line value:',str(tube[i]),'\n']))
            if len(tube[0]) > 1:
                log.write(' '.join([warning_str,'too many arguments in',keys[1],'block,line','['+str(len(mass_t)+2+i+len(pads)+2)+']',' line value:',str(pads[i]),'\n']))           
            if tube[0][0]<=0:
                log.write(' '.join([error_str,'price or number of tube are not a positive number',keys[2],'block,line','['+str(len(mass_t)+2+i+len(pads)+2)+']',' line value:',str(tube[i]),'\n']))   
   
        limi = blocks_dict.get('LIMI')
        if len(limi) == 0:
            log.write(' '.join([error_str,keys[3],'block, is empty','\n']))
            raise ValueError('[Error]:empty block')
        elif len(limi) <= 3:
            log.write(' '.join([error_str,keys[3],'not enough lines','\n']))
            raise ValueError('[Error]:not enough lines')

        dx = 0
        dy = 0
        map_lim = []
        countx = 0
        county = 0
        price_lim = 0
        for i in range(len(limi)):
            if len(limi[i]) < 3:
                log.write(' '.join([error_str,'not enough params in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))
            if i == 0:
                price_lim = limi[i][2]
                countx = int(limi[i][0])
                county = int(limi[i][1]) 
                k=1
                while True:
                    if limi[k+1][0] != limi[k][0]:
                        dx = limi[k+1][0] - limi[k][0]
                        break
                    k+=1
                dy = limi[2][1] - limi[1][1]   
                map_lim = [limi[1][0],limi[1][1],countx*dx+limi[1][0],county*dy+limi[1][1]]
                print('dx=',dx)
                print('dy=',dy)
                print('countx=',countx,' ','county=', county)
                if len(limi) < countx*county:
                    log.write(' '.join([error_str,'not enough cells in map in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))
                if price_lim <= 0:
                    log.write(' '.join([error_str,'price is not a positive number in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))
            elif i == 1:
                if limi[i][2] > price_lim:
                    log.write(' '.join([error_str,'price is bigger than value set in params in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))        
            else:        
                if limi[i][0] != limi[i-1][0] and limi[i][0]-limi[i-1][0] != dx:
                    log.write(' '.join([error_str,'grid by x is broken in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))  
                if limi[i][0] == limi[i-1][0] and limi[i][1]-limi[i-1][1] != dy:       
                    log.write(' '.join([error_str,'grid by y is broken in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))  
                if limi[i][0] == limi[i-1][0] and limi[i-1][1] == limi[i][1]:
                    log.write(' '.join([error_str,'value of the cell didnt change in next cell in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))
                if limi[i][2] > price_lim:
                    log.write(' '.join([error_str,'price is bigger than value set in params in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))    
                if limi[i][2] <=0:
                    log.write(' '.join([error_str,'price is not a positive number in',keys[3], 'block, line', '['+str(len(mass_t)+2+i+len(pads)+len(tube)+6)+']','line value:',str(limi[i]),'\n']))     
        for i in range(len(mass_t)):
            if mass_t[i][0] < map_lim[0] or mass_t[i][0] > map_lim[2] or mass_t[i][1] < map_lim[1] or mass_t[i][1] > map_lim[3]:  
                log.write(' '.join([error_str,'coordinates exceeded in',keys[0], 'block, line', '['+str(i+2)+']','line value:',str(mass_t[i]),'map limits:','['+str(map_lim)+']','\n']))
        
        if ptl_test_enable:
            log.write(' '.join([message_str,'programm started with cross test enabled\n']))
            log.write(' '.join([message_str,'executing "PTL" block test\n']))
        else:
            log.write(' '.join([message_str,'programm started without cross test\n']))
        for
        
#print(read_data('test_file'))
test_files = ['NET_0','NET_1','NET_2','NET_3','NET_4','NET_5','NET_6']
print('start testing')
for i in range(len(test_files)):
    print('starting:', test_files[i])
    print('------------------------')
    try:
        check_input(test_files[i],test_files[i]+'_log',False)
    except ValueError as err:
        print(err)    
