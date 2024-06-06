# -*- coding: utf-8 -*-
import os
from tkinter import *
from tkinter import font
from PIL import Image,ImageTk
import webbrowser
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

import re
import folium
import smtplib
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET


d_url='http://openapi.tour.go.kr/openapi/service/TourismResourceService/getTourResourceDetail'
l_url="http://openapi.tour.go.kr/openapi/service/TourismResourceService/getTourResourceList"
Key='cYtnsiDywOollKA9No97lS%2B7V3H1tl2gq5F%2BJyzAxQ70dhlac0M8D84OwUrJkVVy5wC7NwpkGa05zzXUIl3BWA%3D%3D'


class TKWindow:
    def __init__(self):
        self.w = Tk()
        self.w.title("관광지")
        self.w.geometry("700x600")

        self.create_widgets()

        self.w.mainloop()

    def create_widgets(self):
        # 시도 Label 및 Listbox 생성
        Label(self.w, text="시도").place(x=380, y=45)
        tpf = font.Font(self.w, size=20, weight='bold', family='Consolas')
        self.Sido = "서울특별시"
        self.sdsc = Scrollbar(self.w, width=20)
        self.sdsc.place(x=600, y=30)
        self.sdl = Listbox(self.w, font=tpf, activestyle='none', width=10, height=1, borderwidth=10, relief='ridge',
                           yscrollcommand=self.sdsc.set)
        self.city()
        self.sdl.place(x=430, y=30)

        # 시군구 Label 및 Entry 생성
        Label(self.w, text="시군구").place(x=380, y=110)
        self.sgl = Entry(self.w, width=25, borderwidth=3)
        self.sgl.place(x=430, y=110)

        # 검색 버튼 생성
        self.sb = Button(self.w, text="검색", command=self.browse)
        self.sb.place(x=630, y=110)

        # 지역별 리스트 버튼 생성
        self.gpi = ImageTk.PhotoImage(Image.open("./Image/graph.png"))
        self.gb = Button(self.w, text="지역별 리스트", command=self.newWindow, image=self.gpi)
        self.gb.place(x=630, y=30)

        self.mads = Entry(self.w, width=25, borderwidth=3)
        self.mads.place(x=385, y=550)
        self.MailImage = ImageTk.PhotoImage(Image.open("./Image/mail.png"))
        self.mabt = Button(self.w, image=self.MailImage, command=self.SendMail)
        self.mabt.place(x=585, y=545)
        # 관광지명, 분류 Label 및 설명 Text 생성
        self.tl = Listbox(self.w, width=40, height=20)
        self.tl.place(x=380, y=200)
        self.tl.bind('<<ListboxSelect>>', self.detail)
        tpf = font.Font(self.w, size=20, weight='bold', family='Consolas')
        self.n = Label(self.w, text="관광지명", width=20, font=tpf)
        self.n.place(x=30, y=20)
        self.t = Label(self.w, text="분류", width=60)
        self.t.place(x=-25, y=70)
        self.ex = Text(self.w, width=45, height=16)
        self.ex.place(x=30, y=100)

        # 지도 이미지 및 버튼 생성
        self.ea = PhotoImage(file="./Image/Build.png")
        self.EARTH = Button(self.w, overrelief="solid", width=310, height=230, image=self.ea, command=self.OpenMap)
        self.EARTH.place(x=30, y=340)

    def bar(self):
        sds = self.sdsc.get()[1]
        if sds == 0.0625:
            self.sd = "서울특별시"
        elif sds == 0.125:
            self.sd = "부산광역시"
        elif sds == 0.1875:
            self.sd = "대구광역시"
        elif sds == 0.25:
            self.sd = "인천광역시"
        elif sds == 0.3125:
            self.sd = "광주광역시"
        elif sds == 0.375:
            self.sd = "대전광역시"
        elif sds == 0.4375:
            self.sd = "울산광역시"
        elif sds == 0.5:
            self.sd = "제주특별자치도"
        elif sds == 0.5625:
            self.sd = "경기도"
        elif sds == 0.625:
            self.sd = "강원도"
        elif sds == 0.6875:
            self.sd = "충청북도"
        elif sds == 0.75:
            self.sd = "충청남도"
        elif sds == 0.8125:
            self.sd = "전라북도"
        elif sds == 0.875:
            self.sd = "전라남도"
        elif sds == 0.9375:
            self.sd = "경상북도"
        elif sds == 1.0:
            self.sd = "경상남도"

    def browse(self):
        self.bar()
        self.Sigun=self.sgl.get()

        self.url=userURLBuilder(l_url,ServiceKey=Key, SIDO=self.Sido, GUNGU=self.Sigun)
        print(self.url)
        self.SearchList()

    def city(self):
        self.sdl.insert(1, "서울특별시")
        self.sdl.insert(2, "부산광역시")
        self.sdl.insert(3, "대구광역시")
        self.sdl.insert(4, "인천광역시")
        self.sdl.insert(5, "광주광역시")
        self.sdl.insert(6, "대전광역시")
        self.sdl.insert(7, "울산광역시")
        self.sdl.insert(8, "제주특별자치도")
        self.sdl.insert(9, "경기도")
        self.sdl.insert(10, "강원도")
        self.sdl.insert(11, "충청북도")
        self.sdl.insert(12, "충청남도")
        self.sdl.insert(13, "전라북도")
        self.sdl.insert(14, "전라남도")
        self.sdl.insert(15, "경상북도")
        self.sdl.insert(16, "경상남도")
        self.sdsc.config(command=self.sdl.yview)

    def SearchList(self):  # 관광 정보를 검색하고 결과를 표시
        self.DATALIST = []
        if self.tl.size() > 0:
            self.tl.delete(0, END)
            self.tl.update()

        response = requests.get(self.url)
        tree = ET.fromstring(response.text)

        for item in tree.iter('item'):
            data = {}
            category = item.findtext("ASctnNm")
            name = item.findtext("BResNm")
            data['tag'] = category
            data['name'] = name
            self.DATALIST.append(data)

        for i, data in enumerate(self.DATALIST):
            display_name = f"[{i + 1}] 시설명 : {data['name']}"
            self.tl.insert(i, display_name)

    def detail(self, evt=None):
        if self.tl.curselection():  # 현재 선택된 항목이 있는지 확인
            i = self.tl.curselection()[0]
            self.NM = self.DATALIST[i]['name']
            self.url_d = userURLBuilder(d_url, ServiceKey=Key, SIDO=self.Sido, GUNGU=self.Sigun, RES_NM=self.NM)
            self.GoogleImageSearch(self.NM)
            response = requests.get(self.url_d)

            if response.status_code == 200:  # 요청이 성공했는지 확인
                tree = ET.fromstring(response.text)

                name = tree.findtext(".//BResNm")
                tag = tree.findtext(".//ASctnNm")
                description = tree.findtext(".//FSimpleDesc")

                self.n.configure(text="관광지명 : " + (name if name else "정보 없음"))
                self.t.configure(text="분류 : " + (tag if tag else "정보 없음"))
                self.ex.delete(1.0, END)
                if description:
                    self.ex.insert(INSERT, description)
                else:
                    self.ex.insert(INSERT, "정보 없음")
            else:
                print("상세 정보를 가져오는 중 오류가 발생했습니다. HTTP 상태 코드:", response.status_code)
        else:
            print("선택된 항목이 없습니다.")

    def GoogleImageSearch(self, NM):
        from io import StringIO
        from lxml.html import parse
        import urllib.request
        import requests
        from PIL import Image, ImageTk

        keyword = NM  # 검색 키워드
        url = f'https://www.google.co.kr/search?q={keyword}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwic-taB9IXVAhWDHpQKHXOjC14Q_AUIBigB&biw=1842&bih=990'
        response = requests.get(url).text
        response_source = StringIO(response)
        parsed_doc = parse(response_source)

        doc_root = parsed_doc.getroot()
        images = doc_root.findall('.//img')
        image_url = images[4].get('src')
        print("Image URL:", image_url)
        urllib.request.urlretrieve(image_url, "./Image/Build.png")

        original_image = Image.open("./Image/Build.png")
        resized_image = original_image.resize((300, 230))
        resized_image.save("./Image/Build.png")

        self.ea2 = ImageTk.PhotoImage(Image.open("./Image/Build.png"))
        self.EARTH.config(image=self.ea2)

        self.GoogleMap(self.NM)

    def GoogleMap(self, NM):
        import requests
        from bs4 import BeautifulSoup
        import folium

        address = NM
        url = f"https://maps.googleapis.com/maps/api/geocode/xml?address={address}&key=AIzaSyADJYJpDDbIEKd2oN4EwCMWIFzb9wRnU3c"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "xml")
            latitude = soup.select("location > lat")
            longitude = soup.select("location > lng")

            if latitude and longitude:
                lat = latitude[0].get_text()
                lng = longitude[0].get_text()
                map = folium.Map(location=[lat, lng], zoom_start=15)
                folium.Marker(location=[lat, lng], popup=address).add_to(map)
                map.save("./Image/Map.html")
            else:
                print("주소에 대한 위치 데이터를 찾을 수 없습니다.")
        else:
            print(f"API 요청 실패: 상태 코드 {response.status_code}")

    def SendMail(self):
        import mimetypes
        import smtplib
        import spam
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

    def newWindow(self):
        self.bar()
        l = {}
        if self.sd == "서울특별시":
            l = {"강남구": 10, "강동구": 4, "강북구": 2, "강서구": 9, "관악구": 0, "광진구": 4, "구로구": 0, "금천구": 3,
                 "노원구": 2, "도봉구": 1, "동대문구": 5, "동작구": 0, "마포구": 6, "서대문구": 3, "서초구": 9, "성동구": 2,
                 "성북구": 2, "송파구": 8, "양천구": 0, "영등포구": 6, "용산구": 7, "은평구": 2, "종로구": 10, "중구": 10,
                 "중랑구": 1}
        elif self.sd == "부산광역시":
            l = {"강서구": 1, "금정구": 0, "남구": 2, "동구": 7, "동래구": 5, "부산진구": 2, "북구": 4, "사상구": 2, "사하구": 3,
                 "서구": 3, "수영구": 6, "연제구": 2, "영도구": 2, "중구": 9, "해운대구": 3, "기장군": 3}
        elif self.sd == "대구광역시":
            l = {"남구": 5, "달서구": 7, "동구": 10, "북구": 2, "서구": 1, "수성구": 9, "중구": 10, "달성군": 9}
        elif self.sd == "인천광역시":
            l = {"계양구": 4, "남동구": 4, "동구": 3, "미추홀구": 2, "부평구": 6, "서구": 5, "연수구": 6, "중구": 10,
                 "강화군": 10, "옹진군": 8}
        elif self.sd == "광주광역시":
            l = {"광산구": 3, "남구": 9, "동구": 10, "북구": 10, "서구": 6}
        elif self.sd == "대전광역시":
            l = {"대덕구": 1, "동구": 4, "서구": 4, "유성구": 10, "중구": 3}
        elif self.sd == "울산광역시":
            l = {"남구": 6, "동구": 7, "북구": 2, "중구": 6, "울주군": 10}
        elif self.sd == "제주특별자치도":
            l = {"제주시": 10, "서귀포시": 10}
        elif self.sd == "경기도":
            l = {"고양시": 10, "과천시": 6, "광명시": 8, "광주시": 6, "구리시": 2, "군포시": 0, "김포시": 10, "남양주시": 10,
                 "동두천시": 6, "부천시": 10, "성남시": 8, "수원시": 10, "시흥시": 10, "안산시": 10, "안성시": 10, "안양시": 8,
                 "양주시": 8, "여주시": 10, "오산시": 2, "용인시": 10, "의왕시": 0, "의정부시": 5, "이천시": 6, "파주시": 10,
                 "평택시": 0, "포천시": 10, "하남시": 1, "화성시": 5, "가평군": 10, "양평군": 10, "연천군": 10}
        elif self.sd == "강원도":
            l = {"강릉시": 10, "동해시": 9, "삼척시": 7, "속초시": 10, "원주시": 10, "춘천시": 10, "태백시": 10, "고성군": 9,
                 "양구군": 10, "양양군": 10, "영월군": 10, "인제군": 10, "정선군": 10, "철원군": 10, "평창군": 10, "홍천군": 5,
                 "화천군": 0, "횡성군": 8}
        elif self.sd == "충청북도":
            l = {"제천시": 10, "청주시": 10, "충주시": 10, "괴산군": 10, "단양군": 10, "보은군": 10, "영동군": 10,
                 "옥천군": 4, "음성군": 4, "증평군": 5, "진천군": 10}
        elif self.sd == "충청남도":
            l = {"계룡시": 1, "공주시": 10, "논산시": 6, "당진시": 6, "보령시": 9, "서산시": 5, "아산시": 10, "천안시": 10,
                 "금산군": 7, "부여군": 10, "서천군": 8, "예산군": 10, "청양군": 10, "태안군": 10, "홍성군": 10}
        elif self.sd == "전라북도":
            l = {"전주시": 10, "군산시": 10, "김제시": 4, "남원시": 10, "익산시": 8, "정읍시": 10, "고창군": 10, "무주군": 10,
                 "부안군": 10, "순창군": 10, "완주군": 10, "임실군": 10, "장수군": 10, "진안군": 7}
        elif self.sd == "전라남도":
            l = {"광양시": 10, "나주시": 10, "목포시": 10, "순천시": 10, "여수시": 10, "강진군": 10, "고흥군": 10, "곡성군": 10,
                 "구례군": 10, "담양군": 8, "무안군": 10, "보성군": 10, "신안군": 10, "영광군": 10, "영암군": 8, "완도군": 8,
                 "장성군": 7, "장흥군": 8, "진도군": 10, "해남군": 10, "함평군": 5, "화순군": 10}
        elif self.sd == "경상북도":
            l = {"경산시": 9, "경주시": 10, "구미시": 10, "김천시": 10, "문경시": 10, "상주시": 9, "안동시": 10, "영주시": 10,
                 "영천시": 10, "포항시": 10, "고령군": 10, "군위군": 6, "봉화군": 5, "성주군": 10, "예천군": 4, "영덕군": 10,
                 "영양군": 7, "울릉군": 7, "울진군": 10, "의성군": 7, "청도군": 10, "청송군": 10, "칠곡군": 6}
        elif self.sd == "경상남도":
            l = {"거제시": 10, "김해시": 10, "밀양시": 10, "사천시": 9, "양산시": 10, "진주시": 5, "창원시": 0, "통영시": 10,
                 "거창군": 10, "고성군": 4, "남해군": 6, "산청군": 7, "의령군": 1, "창녕군": 9, "하동군": 10, "함안군": 2,
                 "함양군": 3, "합천군": 6}
        self.gpwin = Toplevel(self.w)
        self.canvas = Canvas(self.gpwin, bg="white", width=400, height=200)
        self.canvas.config(scrollregion=(0, 0, 150, len(l) * 40))
        sbar = Scrollbar(self.gpwin)
        sbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack()
        position = 0
        for i in l.keys():
            self.canvas.create_text(20, 20 + position * 40, text=i, tags="bar")
            self.canvas.create_rectangle(60, 15 + position * 40, 60 + (l[i] / 10) * 200, 30 + position * 40, tags="bar")
            self.canvas.create_text(70 + (l[i] / 10) * 200, 22 + position * 40, text=l[i], tags="bar")
            position += 1

    def OpenMap(self):
        import webbrowser
        url = r'.\Image\Map.html'
        chrome_path = r'open -a /Applications\Google\ Chrome.app %s'
        print(url)
        map_file_path = os.path.abspath("./Image/Map.html")
        webbrowser.open(f"file://{map_file_path}")


def userURLBuilder(url, **user):
    str = url + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str


TKWindow()