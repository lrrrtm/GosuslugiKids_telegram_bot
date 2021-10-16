import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from func.config import from_email, password
from platform import python_version
from jinja2 import Template


def mail_out(to_email, parent_name, patronymic, child_second_name, child_name, club_name, club_cost, geolocation):
    msg = MIMEMultipart('alternative')
    with open('func/main.html', 'r', encoding="utf-8") as f:
        html = f.read()
        f.close()
    html = Template(html).render(parent_name=parent_name, patronymic=patronymic, child_second_name=child_second_name, child_name=child_name,
                    club_name=club_name, club_cost= club_cost, geolocation=geolocation)
    message = 'Сообщение сделано при помощи python'
    msg['To'] = to_email
    msg['Subject'] = 'Запрос ребёнка на посещение внеурочной деятельности'
    msg['From'] = f'GosuslugiDeti <{from_email}>'
    msg['Reply-To'] = from_email
    msg['Return-Path'] = from_email
    msg['X-Mailer'] = 'Python/' + (python_version())


    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(html, 'html'))


    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print('Письмо отправленно')


if __name__ == "__main__":

    mail_out('l0tus0rb@yandex.ru', 'Татьяна', 'Викторовна', 'Сулейманов', 'Артур', 'Яндекс.Лицей', '0', 'Ул. Пушкина')
