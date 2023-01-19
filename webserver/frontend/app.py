import pandas as pd 

import streamlit as st
import folium

from streamlit_folium import st_folium
from folium import plugins

from folium.map import Marker
from jinja2 import Template

import streamlit.components.v1 as components
import copy

# from utils import project_array
# from components import get_list_component, get_detail_component
# from screen.header import header
# # from screen.map import my_map
# from screen.login import show_login
# from screen.signup import show_signup
# from screen.infra import show_infra
from screen.components import header
from screen.initial_page import show_login, show_signup,show_infra
from screen.main_page import show_main
from utils import get_example_data
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO_CENTER

import requests
import json

# COORD_MULT = 1000000000 미사용 : lng, lat 실수값 그대로 사용

# if session 없으면 로그인 화면 보여준다. 

# if clicked marker 있으면 right 에 상세 정보 화면 보여준다. 

# if 찜 목록 활성화 되면 '다 지우고' 찜 목록만 보여준다. 
# 지도도 같이 보여주는게 좋을 것 같다. 
# left 는 그대로 두고, marker 뿌리고 오른쪽은 찜 목록으로 대체 

def set_state_key(STATE_KEYS_VALS):
    for k, v in STATE_KEYS_VALS:
        if k not in st.session_state:
            st.session_state[k] = v

STATE_KEYS_VALS = [
    ("is_login", False),
    ("ex_loaction", None),
    ("rand_list",None),
    ("visibility",'collapsed'),
    ('disabled',False),
    ('sidebar_state','collapsed'), 
    ('show_detail',False),
    ('show_heart', False),
    ('show_item_list',None),
    ('page_counter',0),
    ('cur_user_info',{
        "user_id":None, 
        "selected_gu":"",
    }),
    ('ex_user_info',{
        "user_id":None, 
        "selected_gu":"",
    }),
    ('center',[37.4920372,127.0567124] ),
    ('item_list',[]),
    ('page_counter',0),
]

set_state_key(STATE_KEYS_VALS)

# 초기 설정
# if 'is_login' not in st.session_state:
#     st.session_state['is_login'] = False

# if 'ex_loaction' not in st.session_state:
#     st.session_state['ex_loaction'] = None

# if 'rand_list' not in st.session_state:
#     st.session_state['rand_list'] = None

# Store the initial value of widgets in session state
# if "visibility" not in st.session_state:
#     st.session_state.visibility = "collapsed"
#     st.session_state.disabled = False

# if 'sidebar_state' not in st.session_state:
#     st.session_state.sidebar_state = 'collapsed'

# if 'show_detail' not in st.session_state:
#     st.session_state.show_detail = False

# if 'show_heart' not in st.session_state:
#     st.session_state.show_heart = False

# if 'show_item_list' not in st.session_state:
#     st.session_state.show_item_list = None
    

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

# if 'page_counter' not in st.session_state:
#     st.session_state['page_counter'] = 0


st.set_page_config(layout="wide")

# params  = {'userid': 3, 'location': '수영구'}
# url = 'http://27.96.130.120:30002/'
#     # json.dumps(user)
# x = requests.get(url,params=params)
# print(x)
# 로그인

if ( 0 == st.session_state['page_counter']):
    # st.session_state['page_counter']  값이 1 ( 회원가입 ) 또는 2 ( 인프라 ) 로 변경됨 
    show_login(st.session_state)

# 회원가입
elif ( 1 == st.session_state['page_counter']):
    # st.session_state['page_counter']  값이 2 ( 인프라 ) 로 변경됨 
    show_signup(st.session_state)

# 인프라
elif( 2 == st.session_state['page_counter'] ):
    show_infra(st.session_state)

# 지도
elif( 3 == st.session_state['page_counter'] ):
    example_item_list = get_example_data()

    import copy

    if(  False == st.session_state['show_heart']):
        selected_gu = header(st.session_state, st.session_state['cur_user_info']['selected_gu'])
        cache_gu = st.session_state['cur_user_info']['selected_gu']
        st.session_state['cur_user_info']['selected_gu'] = selected_gu

        # Rerendering issue 방지 
        if( ( ( "" != selected_gu ) and (selected_gu != cache_gu) ) or 
            ( 0 == len(st.session_state['item_list']) ) ):
            # ( st.session_state['ex_user_info']['selected_gu']
            # != st.session_state['cur_user_info']['selected_gu'])):
            # TODO FT201
            # TODO Data loader 선택한 지역구의 매물 정보 가져오기 
            user_info = {
                "user_id" : st.session_state['cur_user_info']['user_id'],
                "user_gu" : st.session_state['cur_user_info']['selected_gu'],
                "house_ranking":{}
            }
            st.session_state['center'] = [GU_INFO_CENTER[selected_gu]["lat"],GU_INFO_CENTER[selected_gu]["lng"]]
            url = ''.join([BACKEND_ADDRESS, DOMAIN_INFO['map'], DOMAIN_INFO['items']])
            res = requests.post(url,data=json.dumps(user_info) )
            st.session_state['item_list'] = [*res.json()['houses'][0].values()]

    show_main(st.session_state, st.session_state['item_list'])