#Message router

import requests
import datetime

class HBMR:
    def __init__(self):
        self.NHLAPI = "http://statsapi.web.nhl.com/api/v1"
        self.SCHEDULE = "/schedule"

    def route(self, msg):

        msgarr = msg.split()

        msgarr.pop(0)

        if not msgarr:
            return None

        if msgarr[0].lower() == 'schedule':
            if len(msgarr) > 1:
                return self.getScheduleByDate(msgarr[1])
            else:
                return self.getDailySchedule()

    def getDailySchedule(self):

        result = requests.get(self.NHLAPI+self.SCHEDULE)

        data = result.json()

        # need to convert to if statement
        try:
            test = data['dates'][0]['games']
            return self.formatSchedule(data)
        except:
            return self.getScheduleByDate('tomorrow')

        return "Whoops"

        

    def getScheduleByDate(self, date):
        print("getScheduleByDate entered")
        if date.lower() == 'tomorrow':
            x = datetime.datetime.now()
            print(x)
            print(x.hour)
            if int(x.hour) < 9:
                date = str(x).split()[0]
            else:
                date = str(x + datetime.timedelta(days=1)).split()[0]
                
        else:
            return "Future lookup currently only supports 'tomorrow'"

        print("Searching date:"+date)
        req = self.NHLAPI + self.SCHEDULE + '?date=' + date
        
        print(req)

        result = requests.get(req)

        data = result.json()

        return self.formatSchedule(data)

    def formatSchedule(self, data):

        thegoods = f"```js\nSchedule for {data['dates'][0]['date']}"

        for x in data['dates'][0]['games']:
            thegoods += '\n'
            thegoods += "Status: " #+ x['status']['abstractGameState']

            gamestatus = x['status']['abstractGameState']

            if gamestatus == 'Preview':
                thegoods += self.formatDate(x['gameDate'])
            elif gamestatus == 'Live':
                thegoods += 'Live '
            elif gamestatus == 'Final':
                thegoods += 'Final'
            else:
                thegoods += "Date/Status error"

            thegoods += "\tTeams: " + x['teams']['home']['team']['name'] + " vs " + x['teams']['away']['team']['name']
            if gamestatus != 'Preview':
                thegoods += "\tScore:\t" + str(x['teams']['home']['score']) + " : " + str(x['teams']['away']['score'])

        thegoods += "```"
        return thegoods

    def formatDate(self, date):

        date = date.split('T')[1]
        date = date.split(':')

        if int(date[0]) < 12:
            date[0] = str(int(date[0])+24)
        date[0] = str(int(date[0])-16)

        print(date)

        final = ''

        for x in date:
            if x == '0':
                x = '12'
            final += x + ':'

        final = final[0:len(final)-5]

        final = final + " ET"

        return final
