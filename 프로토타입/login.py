import streamlit as st
import pandas as pd


###############################################################################
############## 로그인 페이지 ver 2 #############################################

###############################################################################
#### sqlite는 python 2.5version 이상 자동으로 설치되어 있음  
#### 로그인을 위한 DB 연동 ----------------------------------------------------   
import sqlite3

con = sqlite3.connect('프로토타입/database.db')
cur = con.cursor()

###############################################################################
####---로그인 to DB 사용할 함수 -------------------------------------------------
def login_user(id, pwd):
    cur.execute(f"SELECT * FROM users WHERE id = '{id}' and pwd = '{pwd}'")
    return cur.fetchone()
###############################################################################


###############################################################################
##-----로그인 사이드 바----------------------------------------------------------

st.sidebar.image('프로토타입/green.png') ### 이미지 수정 필요합니다.  
menu = st.sidebar.selectbox('MENU', options=['로그인', '회원가입', '회원목록'])

if menu == '로그인':
    # st.subheader('로그인')
    st.sidebar.subheader('로그인')

    login_id = st.sidebar.text_input('아이디', placeholder='아이디를 입력하세요')
    login_pwd = st.sidebar.text_input('패스워드', 
                                     placeholder='패스워드를 입력하세요', 
                                     type='password')
    
    login_btn = st.sidebar.button('로그인')
    
    if login_btn:
        user_info = login_user(login_id, login_pwd)
        st.write('#### 관리자 계정 확인되었습니다.')
        if user_info:
            st.sidebar.write('로그인에 성공했습니다.')
            st.sidebar.write(user_info[2])
            st.sidebar.write(user_info[3])
            st.sidebar.write(user_info[4])
            
            ######## 로그인시 url로 다음 페이지 버튼 생성 ###### URL을 변경해두면 됩니다!! 
            st.image('https://images.pexels.com/photos/1230157/pexels-photo-1230157.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', use_column_width='always')
            st.link_button('Green Energy Check Page','https://thegreen.streamlit.app/')   #http://localhost:8502

        else:
            st.sidebar.write('로그인에 실패했습니다.')
    else : 
        st.subheader('Green Remodeling')
        st.image('https://images.pexels.com/photos/1230157/pexels-photo-1230157.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', use_column_width='always')
        st.caption('그린리모델링이란 에너지 성능 향상 및 효율 개선 등을 통하여 기존 건축물을 녹색건축물로 전환하는 활동을 말한다. (그린리모델링 지원 사업 운영 등에 관한 고시, 국토교통부고시 제2020-510호, 2020.07.10.)')
        
            
            
###############################################################################            
###--- 회원가입  사이드 바-------------------------------------------------------       
if menu == '회원가입':
    with st.form('my_form', clear_on_submit=True):
        st.info('다음 양식을 모두 입력 후 제출 버튼을 눌러주세요.')
        in_id = st.text_input('아이디', max_chars=12)
        in_name = st.text_input('성명', max_chars=10)
        in_pwd = st.text_input('비밀번호', type='password')
        in_pwd_chk = st.text_input('비밀번호 확인', type='password')
        in_birthday = st.date_input('생년월일')
        in_gender = st.radio('성별', options=['남', '여'], horizontal=True)
        
        # 제출버튼 누르면 DB에 저장하기 
        submitted = st.form_submit_button('제출')
        if submitted:
            cur.execute(f"INSERT INTO users(id, pwd, name, birthday, gender) VALUES ("
                        f"'{in_id}', '{in_pwd}', '{in_name}','{in_birthday}', '{in_gender}')")
            con.commit()  

            
###############################################################################  
##--- 회원목록 조회 사이드 바----------------------------------------------------              
if menu == '회원목록':
    st.subheader('회원목록')
    df = pd.read_sql("SELECT * FROM users", con)
    st.dataframe(df)



###############################################################################

# streamlit run 프로토타입\login.py
