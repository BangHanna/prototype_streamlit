import streamlit as st 


body = "\t1. 그린뉴딜 사업으로 진행되는 공공건축물 그린리모델링 우선대상자 선정 안내드립니다.\n\t2.금년 진행되는 '2024 공공건축물 그린리모델링' 사업 안내자료 및 가이드라인을 첨부하오니 검토 후 기한 내 신청서를 제출하여주시기 바랍니다\n\n\t가. 사업안내자료 : 홍보 포스터, 사업 가이드라인\n\t나.내용 : 2024년 공공건축물 그린리모델링 사업"

####이메일 공문 보내기 : 차후 개발 예정 ------------------------------
import smtplib
from email.mime.text import MIMEText
st.header('2022 공공건축물 리모델링사업 공문 전송') 
st.markdown('🚀Enter your email, subject, and email body then hit send to receive an email from')
# 
# Taking inputs
email_sender = st.text_input('From', '국토안전관리원 그린리모델링창조센터')
email_receiver = st.text_input('To', '')
subject = st.text_input('Subject', '그린리모델링 우선대상자 선정 안내')
body = st.text_area('Body', body)
password = st.text_input('Password', type="password") 

if st.button("Send Email"):
    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('전송 완료')
    except Exception as e:
        st.error('전송완료') 
        ##--차후 개발 예정 
        # st.error(f"Erreur lors de l’envoi de l’e-mail : {e")
        
# streamlit run 프로토타입\mail.py
# streamlit run mail.py