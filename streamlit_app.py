import streamlit as st
import pandas as pd

st.title("📋 학생 정보 조회 시스템")

# 1. 구글 시트 URL 설정 (공유 링크 복사 후 사용)
# 형식: https://docs.google.com/spreadsheets/d/시트ID/edit?usp=sharing
SHEET_URL = "https://docs.google.com/spreadsheets/d/1zQTFjP03WnIx1XtDKspVb4PF_b512vIlTmgtuTNhVjM/edit?gid=2105166362#gid=2105166362"

try:
    # 공유 링크를 판다스가 읽을 수 있는 csv 다운로드 형태로 변환
    csv_url = SHEET_URL.replace("/edit?usp=sharing", "/export?format=csv")
    csv_url = csv_url.split("/edit")[0] + "/export?format=csv"
    
    # 구글 시트 데이터 불러오기 (캐싱 처리로 속도 향상)
    @st.cache_data
    def load_data(url):
        # 헤더가 없거나 다를 수 있으므로 기본 로드 후 가공
        df = pd.read_csv(url, header=None)
        return df

    df = load_data(csv_url)
    
except Exception as e:
    st.error("구글 시트 데이터를 불러오는데 실패했습니다. 링크 공유 설정을 확인해주세요.")
    st.stop()

# 2. 사용자 입력 받아오기
grade_class = st.text_input("반을 입력하세요 (ex: 1, 2)", key="class")
student_num = st.text_input("번호를 입력하세요 (ex: 5, 11)", key="num")

if st.button("조회하기", type="primary"):
    if not grade_class or not student_num:
        st.warning("반과 번호를 모두 입력해주세요.")
    else:
        # B열(인덱스 1)은 반, C열(인덱스 2)은 번호, J열(인덱스 9)은 정보
        # 문자와 숫자 혼용 충돌을 막기 위해 string으로 형변환 후 비교
        match = df[
            (df[1].astype(str).str.strip() == str(grade_class).strip()) & 
            (df[2].astype(str).str.strip() == str(student_num).strip())
        ]
        
        if not match.empty:
            # 일치하는 첫 번째 행의 J열(인덱스 9) 데이터 가져오기
            student_info = match.iloc[0][9]
            st.success(f"🎉 조회 성공!")
            st.info(f"**제공된 정보:** {student_info}")
        else:
            st.error("❌ 일치하는 학생 정보가 없습니다. 반과 번호를 확인해주세요.")