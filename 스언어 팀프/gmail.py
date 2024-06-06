def SendMail(self):
    import mimetypes
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.base import MIMEBase
    import os

    # global value
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"
    hfn = r".\Image\Map.html"
    hfn2 = r".\Image\Build.png"

    senderAddr = "qoxmaos342@gmail.com"  # 보내는 사람 email 주소.
    recipientAddr = "qoxmaos342@gmail.com"  # 받는 사람 email 주소.

    msg = MIMEMultipart()
    msg['Subject'] = "Script Tour Mail"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    # 텍스트 메시지 추가
    text = MIMEText("스크립트 관광지 사진\n" +
                    "관광지 : " + self.NM + "\n" +
                    "설명 : " + self.ex.get("1.0", "end") + "\n")
    msg.attach(text)

    # HTML 파일 첨부
    with open(hfn, 'r', encoding='utf-8') as file:
        html_content = file.read()
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

    # 이미지 파일 첨부
    with open(hfn2, 'rb') as file:
        image_part = MIMEImage(file.read())
        image_part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(hfn2))
        msg.attach(image_part)

    # 메일을 발송한다.
    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login("qoxmaos342@gmail.com", "idsj uzkr uooh wanm")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()