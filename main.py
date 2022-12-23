"""code for optimization methods project"""
import sys

def read_data(filename):
    """writing all data into dictionary"""
    data = dict()
    with open(filename, "r", encoding = 'UTF-8') as f:
        for line in f:
            key = line.strip()
            data[key] = []
            while (current_line := f.readline().strip()) != "/":
                data[key].append(tuple(int(val) for val in current_line.split()))
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
            if len(mass_t[i]) != 4:
                log.write('[ERROR]:')
                log.write('not enough/too many params in ' + keys[0] + ' block, line[' + str(i+2) + ']' + ' line value:' + str(mass_t[i])+ '\n')
            elif mass_t[i][3] <= 0:
                log.write('[ERROR]:')
                log.write('price is not a positive number in ' + keys[0] + ' block, line[' + str(i+2) + ']' + ' line value:' + str(mass_t[i]) + '\n') 

            if mass_t[i][0] <0 or mass_t[i][1] < 0 or mass_t[i][2] < 0 :
                log.write('[ERROR]:')
                log.write('coordinate values or rad value are below zero in ' + keys[0] + ' block, line[' + str(i+2) + ']' + ' line value:' + str(mass_t[i]) + '\n') 
        
        pads = blocks_dict.get('PADS')
        if len(pads) == 0:
            log.write(' '.join([error_str,keys[1],'block, is empty','\n']))
            raise ValueError('[Error]:empty block')
        elif len(pads) > 1:
            log.write(' '.join([warning_str,keys[1],'block, has to many strings, using only one. It may cause an error','\n']))
            pads=pads[0]

        for i in range(len(pads)):
            if len(pads) != 2:
                log.write(' '.join([error_str,'missing price or number of pads in',keys[1],'block,line',str(len(mass_t)+2+i),' line value:',str(pads[i]),'\n']))
            if pads[0]<=0 or pads[1]<=0:
                log.write(' '.join([error_str,'price or number of pads are not a positive number',keys[1],'block,line',str(len(mass_t)+2+i),' line value:',str(pads[i]),'\n']))   

        tube = blocks_dict.get('TUBE')
        if len(tube) == 0:
            log.write(' '.join([error_str,str(keys[2]),'block, is empty','\n']))
            raise ValueError('[Error]:empty block')
        elif len(pads) > 1:
            log.write(' '.join([warning_str,str(keys[2]),'block, has to many strings, using only one. It may cause an error','\n']))
            tube=tube[0]

        for i in range(len(tube)):
            if len(tube) != 1:
                log.write(' '.join([error_str,'there must be only one value in',keys[1],'block,however line','['+str(len(mass_t)+2+i)+']','does not follow this rule',' line value:',str(tube[i]),'\n']))
            if pads[0]<=0 or pads[1]<=0:
                log.write(' '.join([error_str,'price or number of pads are not a positive number',keys[1],'block,line',str(len(mass_t)+2+i),' line value:',str(tube[i]),'\n']))   
   
        limi = blocks_dict.get('LIMI')
        if len(limi) == 0:
            log.write(' '.join([error_str,keys[3],'block, is empty','\n']))
            raise ValueError('[Error]:empty block')

        for i in range(len(limi)):
            print()
        if ptl_test_enable:
            log.write(' '.join([message_str,'programm started with cross test enabled\n']))
            log.write(' '.join([message_str,'executing "PTL" block test\n']))
        else:
            log.write(' '.join([message_str,'programm started without cross test\n']))
print(read_data('test_file'))
try:
    check_input('test_file','test_log',False)
except ValueError as err:
    print(err)    
