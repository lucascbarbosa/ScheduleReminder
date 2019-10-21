import smtplib
import os
from  dataframes import extractData,Nao
from datetime import datetime
import time
import pandas as pd
import socket

def getDatetime():
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%d-%m-%Y-%H-%M-%S')
    
    return (st)


def consultasToHistorico(cons,hist,nome,idx):
    row = cons.iloc[idx]
    row = dict(row)
    cons = cons.drop(nome)
    row = pd.DataFrame(row,index =  [0])
    row['Nome'] = nome
    row['Enviado']= 'Nao'
    row.set_index('Nome',inplace  = True)
    hist = hist.append(row)
    hist.to_excel('Excel/Histórico.xlsx')
    cons.to_excel('Excel/Consultas.xlsx')

def sendReminder():
    cons,hist = extractData()
    socket.getaddrinfo('localhost', 8080)

    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

        nomes = cons.index.values
        for idx in range(len(nomes)):
            data = getDatetime().split('-')[:3]
            dayCons = cons.iloc[idx]['Dia']
            monthCons = cons.iloc[idx]['Mes']
            yearCons = cons.iloc[idx]['Ano']
            tsData = datetime.strptime('-'.join(data),'%d-%m-%Y')
            tsDataCons = datetime.strptime(str(dayCons)+'-'+str(monthCons)+'-'+str(yearCons),'%d-%m-%Y')
            if tsDataCons.toordinal() - tsData.toordinal() == 1:
                hourCons = int(cons.iloc[idx]['Horario'].split(':')[0])
                minuteCons = str(cons.iloc[idx]['Horario'].split(':')[1])
                if int(minuteCons)<10:
                    minuteCons = '0'+minuteCons
                nome = nomes[idx]
                medico = cons.iloc[idx]['Medico']
                email = cons.iloc[idx]['E-mail']
                dataCons = str(dayCons) +'/'+ str(monthCons) +'/'+str(yearCons)
                horarioCons = str(hourCons)+':'+str(minuteCons)
                subject = 'Lembrete de Consulta'
                body = f'Senhor(a) {nome}, este email e para lembra-lo(a) da sua proxima consulta no dia {dataCons} as {horarioCons} com o(a) Doutor(a) {medico}'
                message = f'Subject: {subject}\n\n{body}'
                try:
                    smtp.sendmail(EMAIL_ADDRESS, email,message)
                    consultasToHistorico(cons,hist,nome,idx)
                except:
                    print("Falha no envio da mensagem")


cons,hist = extractData()

def sendInvite():
    cons,hist = extractData()
    with smtplib.SMTP('smtp.gmail.com:587') as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

        nomes = hist.index.values
        for idx in range(len(nomes)):
            data = getDatetime().split('-')[:3]
            dayHist = hist.iloc[idx]['Dia']
            monthHist = hist.iloc[idx]['Mes']
            yearHist = hist.iloc[idx]['Ano']

            if dayHist == int(data[0]) and abs(int(data[1]) - monthHist) == 6 :
                nome = nomes[idx]
                medico = hist.iloc[idx]['Medico']
                email = hist.iloc[idx]['E-mail']
                subject = 'Lembrete de Agendamento'
                body = f'Senhor(a) {nome}, este email e para lembra-lo(a) que ja se passaram 6 meses da sua ultima consulta com o(a) medico(a) {medico}, esta na hora de marcar um checkup.'
                message = f'Subject: {subject}\n\n{body}'
                try:
                    smtp.sendmail(EMAIL_ADDRESS, email,message)
                    hist.iloc[idx,-1]= 'Sim'
                    hist.to_excel('Excel/Histórico.xlsx')
                    
                except :
                    print('Envio falhou')

    


EMAIL_ADDRESS = 'koiseroverbr694@gmail.com'
EMAIL_PASSWORD = '08101999'

enviado = False 
min_test = int(getDatetime().split('-')[4])+1
if min_test<10:
    min_test = '0'+str(min_test)
else:
    min_test = str(min_test)
hour_test = int(getDatetime().split('-')[3])
if hour_test<10:
    hour_test = '0'+str(hour_test)
else:
    hour_test = str(hour_test)

while True:
    timeStamp = getDatetime().split('-')[3:]
    
    time.sleep(1)
    if timeStamp == ['00','00','00']:
        enviado = False
    
    if timeStamp == [hour_test,min_test,'00'] and not enviado: 
        sendReminder()
        sendInvite()
        enviado = True
