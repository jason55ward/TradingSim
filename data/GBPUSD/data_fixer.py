

one_minute_file = 'bid_5_m_2020-2022.csv'
timeframe=5
data=[]
new_data=[]
with open(one_minute_file) as bid_file:
    data = bid_file.readlines()

def get_missing():
    count=0
    max_count = 10
    lasthour, lastminute = 0, 0
    for index, line in enumerate(data):
        # print(index, line)
        time = line.split(' ',2)[1].split(':')
        time.pop()
        hour, minute = map(int, time)
        #print(line)
        if minute != lastminute+timeframe and (lastminute != 59 and minute != 0):
            if lastminute==59:
                lastminute = -1
            new_data.append(line.replace(f':{minute}:', f':{str(lastminute+1).rjust(2,"0")}:'))
            #print(line.replace(f':{minute}:', f':{str(lastminute+1).rjust(2, "0")}:'))

            print(f'Error Count {count}:\n{line}')
            print(lasthour, lastminute)
            print(hour, minute)
            count+=1
            if count>max_count:
                break
        lasthour = hour
        lastminute = minute

get_missing()
data.extend(new_data)
data.sort()
print('-----------------------------------------------------')
#get_missing()
print('done')
#   02.01.2020 00:00:00.000 GMT+0200,1.32463,1.32464,1.32462,1.32463,9.75