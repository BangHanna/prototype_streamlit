# /.stremlit/config.toml > 폴더 및 파일 생성 필요
# config.toml 파일
# [theme]
# primaryColor="green"
# --------------------------------------------------------------------------------- 
# streamlit 라이브러리 불러오기 
import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs #pip install streamlit-on-Hover-tabs :sidebar design
import streamlit_nested_layout #pip install streamlit-nested-layout : Dual column

# --------------------------------------------------------------------------------- 
# Page1 라이브러리 불러오기
from datetime import datetime
from streamlit_folium import st_folium
import folium
import branca
import os
import streamlit.config 

# Page2 라이브러리 불러오기
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
# --------------------------------------------------------------------------------- 
# 지도 시각화 라이브러리 불러오기
import geopandas as gpd ####pip install geopandas
import streamlit.components.v1 as components
import json
import folium ##### pip install folium
from folium.plugins import MarkerCluster
import requests
import json
import leafmap ##### pip install leafmap
import leafmap.foliumap as leafmapf

###############################################################################
# map에서 사용하는  기준 경도 위도
# 서울특별시 용산구 이태원로 29
# Latitude : 37.536682709556395
# Longitude : 126.97689056396484
# 대한민국 서울특별시 성동구 옥수동 556-1
# Latitude : 37.547367457666454
# Longitude : 127.0105791091919

###############################################################################
###### 서울지역의 구별 시각화 함수 ver.1
def map_basic_seoul_guo(year_n, month_n, lat=37.547367457666454, long=127.0105791091919): 
    #전체 데이터 파일 불러오기
    seoul_whole = pd.read_csv('프로토타입/시연영상용서울시DB.csv',encoding='utf-8')
    
    # 지도 받아오기 
    r_guo = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
    c_guo = r_guo.content
    seoul_guo = json.loads(c_guo)
    
    # 지도 중앙값 위도
    latitude = lat
    # 지도 중앙값 경도
    longitude = long
    m1 = folium.Map(location=[latitude, longitude],
               zoom_start=10.5, 
               tiles='cartodbpositron'
              )
    
    # 서울지역의 구별 시각화 
    folium.GeoJson(
        seoul_guo,
        name='지역구'
    ).add_to(m1)
    
    #데이터 조건 호출
    year_month_choice_df = seoul_whole.loc[ (seoul_whole['기준 연도']== year_n )&(seoul_whole['월']== month_n)]
    seoul_guo_df_choice = year_month_choice_df.groupby(by='구 이름')['탄소배출량'].sum()
        
    # 구별 색 넣기
    bins1 = list(seoul_guo_df_choice.quantile([0, 0.25, 0.5, 0.75, 1]))
    m1.choropleth(geo_data=seoul_guo,
                data=seoul_guo_df_choice, 
                fill_color= 'YlGn' , # 색상 변경도 가능하다 'YlGn' 'YlOrRd' 'PiYG' 'BuGn'
                fill_opacity=0.5,
                line_opacity=0.2,
                key_on='properties.name',
                legend_name="구별 에너지 탄소 배출량 열량 총합 , 기준: 0.25, 0.5, 0.75",
                bins=bins1
                )     
    st.components.v1.html(m1._repr_html_(), height=400, scrolling=False)  
        
###############################################################################
########## 서울시 동별 시각화 함수 ver2
def map_basic_seoul_dong(year_n2, month_n2, lat=37.547367457666454, long=127.0105791091919 ): 
    # 데이터 파일 불러오기
    seoul_whole = pd.read_csv('프로토타입/시연영상용서울시DB.csv',encoding='utf-8')
    
    # 서울 행정동  json raw파일(githubcontent)
    r_dong = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_submunicipalities_geo_simple.json')
    c_dong = r_dong.content
    seoul_dong = json.loads(c_dong)

    # 위도
    latitude = lat
    # 경도
    longitude = long 

    m2 = folium.Map(location=[latitude, longitude],
                zoom_start=11, 
                tiles='cartodbpositron'
                )

    # 서울시 동 별 시각화 
    folium.GeoJson(
        seoul_dong,
        name='행정동'
    ).add_to(m2)
    
    ## 데이터 조건
    year_month_choice_df2 = seoul_whole.loc[ (seoul_whole['기준 연도']== year_n2 )&(seoul_whole['월']== month_n2)]
    seoul_dong_df_choice = year_month_choice_df2.groupby(by='동 이름')['탄소배출량'].sum() 
          
    # 동별 색 넣기
    bins2 = list(seoul_dong_df_choice.quantile([0, 0.25, 0.5, 0.75, 1])) #0, 0.25, 0.5, 0.75, 1
    m2.choropleth(geo_data=seoul_dong,
                data=seoul_dong_df_choice, 
                fill_color= 'YlGn' , # 색상 변경도 가능하다 'YlGn' 'YlOrRd' 'PiYG' 'BuGn','PiYG'
                fill_opacity=0.5,
                line_opacity=0.2,
                key_on='properties.name',
                legend_name="동 별 에너지 탄소 배출량 열량 총합, 기준: 0.25, 0.5, 0.75 ",
                bins=bins2
                )
    st.components.v1.html(m2._repr_html_(), height=400,scrolling=False)
    
############################################################################### 
########## 서울시  구 별 히트맵 함수 ver4

def map_heat_seoul_guo(year_n3, month_n3): 
    
    seoul_whole = pd.read_csv('프로토타입/프로토타입서울시202312DB.csv', encoding='utf-8') ## 2023년도 12월 데이터만 있음 

    # 행정구역 json raw파일(githubcontent)
    r_guo = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
    c_guo = r_guo.content
    seoul_guo = json.loads(c_guo)

    m3 = leafmapf.Map(center=[37.536682709556395, 126.97689056396484], zoom=11) #,tiles='cartodbpositron'

    # 데이터 조건 
    seoul_heat_df = seoul_whole.loc[ (seoul_whole['기준 연도']== year_n3 )&(seoul_whole['사용 월']== month_n3) ]

    # 내림차순으로 가장 많은 곳 
    heat_df = seoul_heat_df[['위도','경도','에너지 탄소 배출량 총합']].sort_values('에너지 탄소 배출량 총합',ascending=False).iloc[:999]
    
    #히트맵 그리기 
    m3.add_heatmap(
        heat_df ,
        value="에너지 탄소 배출량 총합", #columns to create the heat map 
        latitude="위도",
        longitude="경도",
        name="Heat map",
        radius=20,
    )
    # 지역구 라인 표시 
    folium.GeoJson(
        seoul_guo,
        name='지역구',
        style_function= lambda feature : {
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.2},
    ).add_to(m3)
    # 시각화
    st.components.v1.html(m3.to_html(), height=650,scrolling=False)   
        
###############################################################################
###############################################################################
###############################################################################



# 페이지 레이아웃
st.set_page_config(layout="wide")

# https://fonts.google.com/icons : 아이콘
# st.caption("🌏 Green Remodeling")
st.markdown('<style>' + open('프로토타입/style.css').read() + '</style>', unsafe_allow_html=True)
st.sidebar.image('프로토타입/green2.png')
with st.sidebar:
        tabs = on_hover_tabs(tabName=['통합 대시보드', '에너지 낭비 건물 모니터링', '리모델링 사업 현황 모니터링', '탄소배출량 추이 모니터링'], 
                             iconName=['dashboard','list', 'legend_toggle', 'co2'],
                             styles = {'navtab': {'background-color':'#111', # 메뉴 선택 색
                                                  'color': '#FFFFFF', #아이콘 및 페이지명 색
                                                  'font-size': '16px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabOptionsStyle': {':hover :hover': {'color': 'green',
                                                                      'cursor': 'pointer'}},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'17.5px',
                                                    'text-align': 'left'},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'}},
                             key="1", default_choice=0)
        
# --------------------------------------------------------------------------------- 
# Page1 data 작업
data = pd.read_csv("프로토타입/프로토타입_1페이지_배포용.csv")
data = data[['건물명', '연식', '탄소/연면적','작년 탄소 배출량 월평균','지번주소','사용승인 연도','구 이름', '위도', '경도', '동 이름', '2401 탄소 예측량', '건축면적(㎡)', '지상층수', '연면적(㎡)', '그린리모델링진행', '지하층수', '사용승인일', '지붕코드명', '구조코드명', '주변 평균', '통합용도명', '건축물분류']] 
         
    
# --------------------------------------------------------------------------------- 
# Page2 data 작업
df = pd.read_csv('프로토타입/p2dataframe_1643.csv')    
# 현재 날짜 구하기
current_date = datetime.now()

# 현재 날짜에서 연도 추출
year = current_date.year 


df2 = pd.read_csv('프로토타입/df2_2023.csv')
df2.reset_index(inplace = True, drop = True)
        

# 2023 선정 대상 사업 완료시 감축 기대량
ex = 25.067*len(df2.loc[df2['진행 현황'] == '대상선정',:])
# 2023 완료시 온실가스 감축 기대량(연간) : 2023사업건 * 25.067
    
# 2020이후 2023까지 서울시 연간 누적 감축기대량
ex2 = round(len(df2.loc[df2['연도별 사업 구분'] == 2022,:]) * 25.067 + len(df2.loc[df2['연도별 사업 구분'] == 2021,:]) * 25.067 * 2
    + len(df2.loc[df2['연도별 사업 구분'] == 2020,:])*25.067*3, 2)

# 2020년도 이후 '사업 완료' 건들의 온실가스 누적 감축효과 (2020건 * 25.067 * (year - 2020-1) + 2021건 *25.067 *(year-2021-1) + 2022건 * 25.067 *(year-2022-1) + 2023건 *25.067 *(year-2023)
# date에서 계산되는걸 하고자 했으나 현재 24년이고 우리 대시보드 기준은 23년이라 단순 정수로 넣어둠
# 건당 연간 감축량 25.067 tCO2
    
       
# 2023사업 완료시 전국 감축 기대량
ex3 = 25.067 * 2911
    
# 2020-2023 누적 감축 기대량
ex4 = 821*25.067*(year-2020) + 895*25.067*(year - 2021) + 575*25.067*(year-2022) + 620*25.067*(year-2023)

# --------------------------------------------------------------------------------- 
# Page3 data 불러오기    
df3 = pd.read_csv('프로토타입/프로토타입2050예측.csv', encoding='utf-8')  
        
# 데이터 프레임 재구성
df_grouped = df3.groupby(['연도', '구'])['탄소배출량'].sum().unstack()
df_grouped.reset_index(inplace=True)
df_grouped['연도'] = df_grouped['연도'].astype(str)    
    
    
# --------------------------------------------------------------------------------- 
if tabs == "통합 대시보드":
    st.subheader('▸ 통합 대시보드')
    st.caption("""---""")
    outer_cols = st.columns([0.6,0.3])
    with outer_cols[0]:
            inner_cols = st.columns([0.6, 0.4])
            with inner_cols[0]:
                with st.expander("**▪ 서울시 전체 공공건축물 지도**", expanded=True): 
                    m= folium.Map(location=[df['위도'].mean(), df['경도'].mean()], zoom_start=10)
                    for idx , row in df.iterrows():
                        if row['진행 현황'] == '예비대상':
                            icon_color = 'lightblue'
                        elif row['진행 현황'] == '사업완료':
                            icon_color = 'lightgreen'
                        elif row['진행 현황'] == '대상선정':
                            icon_color = 'lightred'
                        else:
                            icon_color = 'lightgray'
                        icon = folium.Icon(color=icon_color)
                        folium.Marker(location = [row['위도'], row['경도']],
                        tooltip = row['건물명'], icon = icon).add_to(m)
                    st.components.v1.html(m._repr_html_(), height=250)
            with inner_cols[1]:
                with st.expander("**▪ 2023 사업 진행 현황**", expanded=True): 
                    st.write('')
                    
                    fig1 = px.pie(df2, names='진행 현황',color_discrete_sequence=['#D2F2EE', "#DEE8CC", '#FDAAAA'])
                    fig1.update_layout(width=270, height=235)  #plotly pie차트
                    st.plotly_chart(fig1)
            with st.expander("**▪ 2050 탄소배출 시나리오**", expanded=True): 
                selected_region = st.selectbox('지역 선택', ['서울시', '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'], key='sel1', label_visibility='collapsed')
                # 자치구별 사용량 area_chart
                st.area_chart(df_grouped, x='연도', y=[selected_region,'서울시'], color=["#DEE8CC", "#467302"], height=230)

        
    with outer_cols[1]:
        with st.expander("**▪ 온실가스 감축 기대량**", expanded=True):  

            gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value= ex4,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "2023 전국 사업 완료시 2025 목표 대비 달성도 (단위 tCO2)",'font': {'size': 13}},
                    gauge={
                        'axis': {'range': [0, 464195]},  # min 및 max 범위 조절
                        'bar': {'color': "rgba(0, 128, 0, 0.5)"},
                        'borderwidth': 2,
                        'bordercolor': "black",
                        'steps': [
                            {'range': [0, 100000], 'color': "rgba(255, 0, 0, 0.1)"},
                            {'range': [100000, 300000], 'color': "rgba(255, 255, 0, 0.1)"},
                            {'range': [300000, 464195], 'color': "rgba(0, 128, 0, 0.1)"},
                        ],
                        'threshold': {
                            'line': {'color': "green", 'width': 4},
                            'thickness': 0.75,
                            'value': ex4
                        }
                    }
                ))
            gauge.update_layout(width=180, height=180)
            # 여백 없애기
            gauge.update_layout(margin=dict(t=50, b=0, l=0, r=0))
            
            with st.expander('**2023 전국 사업 포함 연간 온실가스 감축효과**', expanded=True):
                st.metric(label = 'tCO2', value = f'{ex3}')
                
            with st.expander('**2023 전국 사업 완료시 2020 이후 온실가스 누적 감축효과**', expanded=True):
                st.metric(label= 'tCO2', value=f'{ex4}')

            # Streamlit 앱에 Plotly 차트 표시
            st.plotly_chart(gauge, use_container_width=True)

            
            
# ---------------------------------------------------------------------------------     
elif tabs == "에너지 낭비 건물 모니터링":
    st.header('에너지 낭비 건물 모니터링')
    # st.markdown("""---""")
    st.title('') # 디자인을 위한 공백 추가
    
    with st.expander("**▪ 구분**", expanded=True):
        st.write('')
        col1110, col1111, col1112 = st.columns([0.2, 0.2, 0.2])
        with col1112:
            st.write('**사용승인일**')
            min_date, max_date = st.slider('사용승인일',
                                  min_value=1963,
                                  max_value=2013,
                                  value=(1963, 2013),
                                 label_visibility = 'collapsed')
        with col1110:
            st.write('**공공건축물 여부**')
            public = st.selectbox('건축물 분류',['공공','민간'], label_visibility = 'collapsed')
        
        with col1111:
            st.write('**리모델링 여부**')
            remodeling = st.selectbox('리모델링 여부', ['미진행','진행'], label_visibility = 'collapsed')
        
        col1130, col1131= st.columns([0.4,0.2])
        with col1130:
            st.write('**주사용용도명**')
            usage = st.multiselect('주사용용도', ['어린이집', '보건소', '의료기관', '파출소', '경로당', '도서관','기타'], ['어린이집', '보건소', '의료기관', '파출소', '경로당', '도서관','기타'],label_visibility = 'collapsed')
        with col1131:
            st.write('**지역구**')
            location = st.multiselect('지역구',['강남구','강동구','강북구', '강서구', '관악구','광진구','구로구','금천구', '노원구','도봉구','동대문구',
                            '동작구','마포구','서대문구','서초구','성동구','성북구', '송파구','양천구','영등포구', '용산구','은평구',
                            '종로구', '중구', '중랑구'],
                            ['강서구'], label_visibility = 'collapsed')
        

    if st.button('추출'):
        col200, col201 = st.columns([0.3, 0.2])
        with col200:
            map_data = data.loc[(data['건축물분류'] == public) &(data['그린리모델링진행'] == remodeling) 
                                & (data['구 이름'].isin(location)) & (data['통합용도명'].isin(usage))
                               & (data['사용승인 연도']>=min_date)& (data['사용승인 연도']<=max_date)]
            if len(map_data) == 0:
                st.info('조건에 맞는 데이터가 없습니다')
            else:
                
                m= folium.Map(location=[map_data['위도'].mean(), map_data['경도'].mean()], zoom_start=13)
                for idx , row in map_data.iterrows():
                    html= """<!DOCTYPE html>
                        <html>
                        <body>
                            <table style="height: 380px; width: 330px;">  <tbody> <tr>
                            <td class="width: 170px;" colspan="2" rowspan="8">
                                <button type="button">
                                    <img src='https://github.com/jungrad8774/building_photo/blob/main/{}.png?raw=true' 
                                    style='width: 140px; height: 180px;'""".format(row['사용승인일'])+"""
                                        onclick="location.href='https://map.kakao.com/link/roadview/{},{}'">""".format(row['위도'],row['경도'])+"""
                                </button>
                            </div></td>
                              <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">건물명</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['건물명'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">용도</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['통합용도명'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">지번주소</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['지번주소'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">승인연도</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['사용승인 연도'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">구조</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['구조코드명'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">지붕</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['지붕코드명'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">건축면적</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['건축면적(㎡)'])+"""
                          </tr>
                          <tr>
                            <td style="width: 60px;background-color: #2A799C;">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">지상층수</div></td>
                            <td style="width: 100px;font-size:11px;background-color: #C5DCE7;">{}</td>""".format(row['지상층수'])+"""
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td style="background-color: #2A799C;" colspan="2">
                            <div style="color: #ffffff;font-size:11px;text-align:center;">연면적</td>
                            <td style="font-size:11px;background-color: #C5DCE7;" colspan="2">{}</td>""".format(row['연면적(㎡)'])+"""
                          </tr>
                          <tr>
                            <td style="background-color: #FFC000;" colspan="2">
                            <div style="color: #000000;font-size:11px;text-align:center;">탄소배출량</td>
                            <td style="font-size:11px;background-color: #FFF2CC;" colspan="2">{}</td>""".format(row['작년 탄소 배출량 월평균'])+"""
                          </tr>
                          <tr>
                            <td style="background-color: #FFC000;" colspan="2">
                            <div style="color: #000000;font-size:11px;text-align:center;">단위면적당 탄소배출량</td>
                            <td style="font-size:11px;background-color: #FFF2CC;" colspan="2">{}</td>""".format(row['탄소/연면적'])+"""
                          </tr>
                          <tr>
                            <td style="background-color: #FFC000;" colspan="2">
                            <div style="color: #000000;font-size:11px;text-align:center;">주변 평균</td>
                            <td style="font-size:11px;background-color: #FFF2CC;" colspan="2">{}</td>""".format(row['주변 평균'])+"""
                          </tr>
                          <tr>
                            <td style="background-color: #FFC000;" colspan="2">
                            <div style="color: #000000;font-size:11px;text-align:center;">다음달 탄소배출 예측량</td>
                            <td style="font-size:11px;background-color: #FFF2CC;" colspan="2">{}</td>""".format(row['2401 탄소 예측량'])+"""
                          </tr>
                          <tr>
                            <td style="background-color: #FFC000;" colspan="2">
                            <div style="color: #000000;font-size:11px;text-align:center;">다음달 단위면적당 탄소배출 예측량</td>
                            <td style="font-size:11px;background-color: #FFF2CC;" colspan="2">{}</td>""".format(row['2401 탄소 예측량']/row['연면적(㎡)'])+"""
                          </tr>
                          <tr>
                            <th style="background-color: #2A799C;" colspan="4">
                            <div style="color: #ffffff;text-align:center;">
                            <a href="https://thegreenmail.streamlit.app/" target="_blank">공문 보내기</a>
                        </tbody > </table>
                    </body>
                    </html> """
                    iframe = branca.element.IFrame(html =html, width = 350, height = 400)
                    popup_text = folium.Popup(iframe, parse_html =True)
                    icon = folium.Icon(color = 'blue')
                    folium.Marker(location = [row['위도'], row['경도']],
                                  popup = popup_text,tooltip = row['건물명'], icon = icon).add_to(m)
                st.components.v1.html(m._repr_html_(), width = 750, height = 700)
                #st_data = st_folium(m, width = 500)
                #st.dataframe(map_data)
        with col201:
            # st.info('컬럼을 눌러 정렬 기준을 선택하세요')
            st.write('')
            st.write("**▪ 컬럼을 눌러 정렬 기준을 선택하세요**")
            st.dataframe(map_data.sort_values(by = '탄소/연면적', ascending = False), height =390, hide_index=True)
            



# --------------------------------------------------------------------------------- 
elif tabs == "리모델링 사업 현황 모니터링":
    st.caption("🌏 Green Remodeling")
    st.header('리모델링 사업 현황 모니터링')
    # st.markdown("""---""")
    st.title('')

    col1,col2,col3 = st.columns([0.4,0.3,0.4]) 
    with col1 :
        st.markdown('##### ▪ 서울시 전체 공공건축물 지도')
        with st.expander("**지도**", expanded=True):      
            
            # 승원 지도 pin 코드 가져오기################################
            #st.image('https://cis.seoul.go.kr/ko/totalalimi_new/images/map/map_0.png', width = 400)
            m= folium.Map(location=[df['위도'].mean(), df['경도'].mean()], zoom_start=10)
            for idx , row in df.iterrows():
                if row['진행 현황'] == '예비대상':
                    icon_color = 'lightblue'
                elif row['진행 현황'] == '사업완료':
                    icon_color = 'lightgreen'
                elif row['진행 현황'] == '대상선정':
                    icon_color = 'lightred'
                else:
                    icon_color = 'lightgray'
                icon = folium.Icon(color=icon_color)
                #icon = folium.Icon(color = 'green')
                folium.Marker(location = [row['위도'], row['경도']],
                tooltip = row['건물명'], icon = icon).add_to(m)
            st.components.v1.html(m._repr_html_(), height=250)
                    #st_data = st_folium(m, width = 500)
                    #st.dataframe(map_data)
            st.caption('* 회색: 사업 부적합')
            st.caption('* 초록: 그린리모델링 완료')
            st.caption('* 파랑: 그린 리모델링 예비 대상')
            st.caption('* 빨강: 2023 사업 선정 대상')
    
    
    with col2 :
        st.markdown('##### ▪ 2023 사업 진행 현황')
        with st.expander("**현황 차트**", expanded=True): 
            fig1 = px.pie(df2, names='진행 현황',color_discrete_sequence=['#D2F2EE', "#DEE8CC", '#FDAAAA'])
            fig1.update_layout(width=300, height=275)  #plotly pie차트
            st.plotly_chart(fig1)
            # fig1.update_traces(textposition='inside', textinfo='percent+label')
            # fig1.update_layout(font=dict(size=11))
            # st.plotly_chart(fig1, use_container_width=True)

            # st.caption('* 예비대상: 대상 조건 부합 건물 중 당해년도 사업 미진행')
            # st.caption('* 대상선정: 대상 조건 부합 건물 중 당해년도 선정 대상')
            st.caption('* 예비대상: 사업 적합 중 당해년도 사업 미진행')
            st.caption('* 대상선정: 사업 적합 중 당해년도 선정 대상')
            st.caption('* 사업완료: 과거 사업 시행 완료')

    with col3 :
        st.markdown('##### ▪ 2023 사업 대상 건축물')
        with st.expander("**건축물 데이터**", expanded=True): 
            st.dataframe( df2.loc[df2['진행 현황'] == '대상선정',:].reset_index(drop = True), height=365,hide_index=True)
    
    
    
     # ----------------------------------------------------------------------------------------
    st.title('')
    st.header('온실가스 감축 기대량')
    st.title('')

    outer_cols = st.columns([0.2, 0.4])
    
    with outer_cols[0]:
        st.markdown('##### ▪ 서울시 사업 기대효과')
        with st.expander('**2023년 서울시 사업 완료시 연간 온실가스 감축 기대량**', expanded=True):
            st.metric(label = 'tCO2', value = f'{ex} ')
        with st.expander('**2023년 기준 2020 이후 서울시 누적 온실가스 감축량**', expanded=True):
            st.metric(label='tCO2', value=f'{ex2}')
    with outer_cols[1]:
        st.markdown('##### ▪ 전국 사업 기대효과')
        inner_cols = st.columns([1, 1])
        with inner_cols[0]:
            with st.expander('**2023 전국 사업 포함 연간 온실가스 감축효과**', expanded=True):
                st.metric(label = 'tCO2', value = f'{ex3}')
            with st.expander('**2023 전국 사업 완료시 2020 이후 온실가스 누적 감축효과**', expanded=True):
                st.metric(label= 'tCO2', value=f'{ex4}')
        with inner_cols[1]:
            inner_cols = st.columns([0.1, 0.8])
            with inner_cols[0]:
                st.write('')
                # st.write('**사업 완료시 2025 목표 대비 달성도**')
            with inner_cols[1]:
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value= ex4,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "2023 전국 사업 완료시 2025 목표 대비 달성도 (단위 tCO2)"},
                    gauge={
                        'axis': {'range': [0, 464195]},  # min 및 max 범위 조절
                        'bar': {'color': "rgba(0, 128, 0, 0.5)"},
                        'borderwidth': 2,
                        'bordercolor': "black",
                        'steps': [
                            {'range': [0, 100000], 'color': "rgba(255, 0, 0, 0.1)"},
                            {'range': [100000, 300000], 'color': "rgba(255, 255, 0, 0.1)"},
                            {'range': [300000, 464195], 'color': "rgba(0, 128, 0, 0.1)"},
                        ],
                        'threshold': {
                            'line': {'color': "green", 'width': 4},
                            'thickness': 0.75,
                            'value': ex4
                        }
                    }
                ))
                gauge.update_layout(width=300, height=300)
                # 여백 없애기
                gauge.update_layout(margin=dict(t=0, b=0, l=20, r=0))

                # Streamlit 앱에 Plotly 차트 표시
                st.plotly_chart(gauge)
            
            
            
            
# ---------------------------------------------------------------------------------           
elif tabs == "탄소배출량 추이 모니터링":
    st.caption("🌏 Green Remodeling")
    st.header('탄소배출량 추이 모니터링')
    # st.markdown("""---""")
    st.title('')
    outer_cols = st.columns([0.6, 0.4])
    
# ---------------------------------------------------------------------------------       
    with outer_cols[0]:
        st.markdown('##### ▪ 탄소배출량 추이')
        with st.expander('**구분**', expanded=True):
            with st.expander('**일자**', expanded=True):
                inner_cols = st.columns([1, 1])
                with inner_cols[0]:
                    year_nu = st.selectbox('Year', [2019,2020,2021,2022,2023], index=None, placeholder="Select Year...")
                with inner_cols[1]:
                    month_nu = st.selectbox('Month', [1,2,3,4,5,6,7,8,9,10,11,12], index=None, placeholder="Select Month...")
            
            ###############################################################################
            ######## 변경 사항 2024.01.03########       
            with st.expander('**지도**', expanded=True):
                option = st.selectbox("지도 선택",
                              ("Map", "Heat Map","S-Map"),
                              index=None, placeholder="Select contact method...",
                             label_visibility='collapsed')
                if option == 'Map':  
                    select_gd = st.radio(label = 'Radio buttons', options = ['구', '동'], label_visibility='collapsed')   
                    if select_gd =='구':
                        map_basic_seoul_guo(year_nu, month_nu)   
                    else : 
                        map_basic_seoul_dong(year_nu, month_nu)                              
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) 
                       
                elif option =='Heat Map' :
                    st.write(' 2023년도 12월 기준 : 최다 탄소 배출 지역 ')
                    map_heat_seoul_guo(year_nu, month_nu)
                    
                   #### 서울시 3D S-Map ##### 
                elif option =='S-Map' :
                    st.components.v1.iframe("https://smap.seoul.go.kr/",height=900,scrolling=True) # width=1600, height=900
        
# --------------------------------------------------------------------------------- 
    with outer_cols[1]:
        st.markdown('##### ▪ 2050 탄소배출량 시나리오')
        
        with st.expander('**지역선택**', expanded=True):
            selected_region = st.selectbox('지역 선택', ['서울시', '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'], key='sel1', label_visibility='collapsed')
            
            # 자치구별 사용량 area_chart
            st.area_chart(df_grouped, x='연도', y=[selected_region,'서울시'], color=["#DEE8CC", "#467302"])
        
            # 자치구별 사용량 dataframe
            with st.expander('**• 서울시 전체 탄소배출량과 비교**'):    
                if selected_region == '서울시':
                    st.dataframe(df_grouped[['연도', selected_region]], hide_index=True, use_container_width=True)
                else:
                    st.dataframe(df_grouped[['연도', selected_region, '서울시']], hide_index=True, use_container_width=True)
        
    
# streamlit run 프로토타입\the_green.py
# streamlit run the_green.py
