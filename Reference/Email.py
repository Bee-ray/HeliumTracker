import smtplib


def send_email(sender, password, receivers, subject, text):
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(sender,password)
        message = 'Subject:{}\n\n{}'.format(subject, text)
        for receiver in receivers:
            s.sendmail(sender,receiver,message)

send_email('deanlab.notification@gmail.com','ekgvglpjzmaonrcf',['by2298@columbia.edu','ybr123111@gmail.com'],'TEST','Liquefiers on fire!!')