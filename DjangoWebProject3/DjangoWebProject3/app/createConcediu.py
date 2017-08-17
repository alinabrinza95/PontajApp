from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

def concediu(name, teamleader, daysOff, start_date, end_date):
    mycanvas = canvas.Canvas("concediu.pdf", pagesize=letter)
    mycanvas.setLineWidth(.3)
    mycanvas.setFont('Helvetica', 12)

    sendTime=str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)

    mycanvas.drawString(30, 750, 'CONCEDIU')
    mycanvas.drawString(500, 750, sendTime)
    mycanvas.line(420, 747, 580, 747)

    mycanvas.drawString(30, 725, 'TEAM LEADER:')
    mycanvas.drawString(500, 725, str(teamleader))
    mycanvas.line(420, 723, 580, 723)

    mycanvas.drawString(30, 700, 'RECEIVED BY:')
    mycanvas.line(265, 700, 580, 700)
    mycanvas.drawString(265, 703, str(name))

    mycanvas.drawString(30,525,'NUMBER OF DAYS OFF: ')
    mycanvas.drawString(265,525,str(daysOff))
    mycanvas.line(265,523,580,523)

    mycanvas.drawString(30,500,'START DATE: ')
    mycanvas.drawString(265,500,str(start_date))
    mycanvas.line(265,497,580,497)

    mycanvas.drawString(30,475,'END DATE: ')
    mycanvas.drawString(265,475,str(end_date))
    mycanvas.line(265,472,580,472)

    mycanvas.drawString(30,450,'VALIDATION: ')
    mycanvas.line(265,447,580,447)


    mycanvas.save()
    return mycanvas


