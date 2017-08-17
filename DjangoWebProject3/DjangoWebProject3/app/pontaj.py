import datetime, calendar, csv
from datetime import  date, timedelta

def pontaj(first_name,last_name, marca,cnp,location,team,team_leader_email,concediu,oohrequest):

        transport=80

        monthDays = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)
        days = int(monthDays)
        workingDays, satAndSun = 0, 0

        for i in range(1, days + 1, 1):
            if ((calendar.weekday(datetime.datetime.now().year, datetime.datetime.now().month, i) == 0) or (
                        calendar.weekday(datetime.datetime.now().year, datetime.datetime.now().month, i) == 6)):
                satAndSun += 1
            else:
                workingDays += 1
        workingHours=workingDays*8
        number_tickets=workingDays
        hours_worked=workingHours
        hours_paid=0
        with open('pontaj.csv','wb') as csvfile:
            fieldnames=['Prenume','Nume','Marca','CNP','Locatia','Echipa','Email TL']
            writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Prenume' : first_name,'Nume': last_name,'Marca':marca,'CNP':cnp,'Locatia':location,'Echipa':team,'Email TL':team_leader_email})

            fieldnames1 = ['Concediu']
            writer1=csv.DictWriter(csvfile,fieldnames=fieldnames1)
            if concediu==True:
                start_date=raw_input("Start date (YYYY-MM-DD):")
                end_date=raw_input("End_date (YYYY-MM-DD):")
                fieldnames1.insert(len(fieldnames1)+1,'Start')
                fieldnames1.append('End')
                fieldnames1.insert(len(fieldnames1)+1,'Zile libere')
                writer1.writeheader()

                start_date1 = start_date.split('-')
                end_date1 = end_date.split('-')

                start_year, start_month, start_day = int(start_date1[0]), int(start_date1[1]), int(start_date1[2])
                end_year, end_month, end_day = int(end_date1[0]), int(end_date1[1]), int(end_date1[2])
                fromdate = date(start_year, start_month, start_day - 1)
                todate = date(end_year, end_month, end_day)

                if(start_month==end_month):
                    fromdate = fromdate
                    todate = todate
                elif ((start_month<end_month and start_year==end_year) or (start_month>end_month and start_year<end_year)):
                    fromdate=date(start_year,start_month,start_day-1)
                    last=calendar.monthrange(start_year,start_month)
                    todate=date(start_year,start_month,last)


                daygenerator = (fromdate + timedelta(x + 1) for x in xrange((todate - fromdate).days))
                week_days = sum(1 for day in daygenerator if day.weekday() < 5)


                writer1.writerow({'Concediu':concediu,'Start':start_date,'End':end_date,'Zile libere':week_days})
                hours_worked=hours_worked-week_days*8
                hours_paid=hours_worked+week_days*8
                number_tickets=workingDays-week_days
                transport=float(transport/workingDays)*(workingDays-week_days)


            else:
                writer1.writeheader()
                writer1.writerow({'Concediu': concediu})
                hours_paid=workingHours

            fieldnames2 = ['OOH']
            writer2=csv.DictWriter(csvfile, fieldnames=fieldnames2)
            if oohrequest==True:
                days_called=raw_input("Days called:")
                count_days=""
                incident=""
                hours=0
                i=0
                while i<int(days_called):
                    i=i+1
                    day=raw_input("Day called:")
                    incident_number=raw_input("Incident number:")
                    hours_spent=raw_input("Hours spent:")

                    count_days=count_days+" "+ str(day)
                    incident=incident+" "+incident_number
                    hours=hours+int(hours_spent)

                fieldnames2.insert(len(fieldnames2)+1,'Day called')
                fieldnames2.append('Incident number')
                fieldnames2.append('Hours spent')
                writer2.writeheader()
                writer2.writerow({'OOH':oohrequest,'Day called':count_days,'Incident number':incident,'Hours spent':hours})

                hours_worked+=hours
                hours_paid+=2*hours
            else:
                writer2.writeheader()
                writer2.writerow({'OOH':oohrequest})
                hours_paid=workingHours
            fieldnames3=['Ore lucratoare','Ore lucrate','Ore platite','Transport','Tichete']
            writer3=csv.DictWriter(csvfile,fieldnames=fieldnames3)
            writer3.writeheader()
            writer3.writerow({'Ore lucratoare':workingHours,'Ore lucrate':hours_worked,'Ore platite':hours_paid,'Transport':transport,'Tichete':number_tickets})