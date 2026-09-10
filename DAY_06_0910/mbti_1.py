# --------------------------------------------------
# 0. 한글 폰트 설정 (Streamlit Cloud 리눅스 환경 대응)
# --------------------------------------------------
import urllib.request
import matplotlib.font_manager as fm

def setup_cloud_korean_font():
    # 윈도우나 맥 로컬 환경일 경우 기존 시스템 폰트 우선 적용
    if platform.system() == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"
    elif platform.system() == "Darwin":
        plt.rcParams["font.family"] = "AppleGothic"
    else:
        # Streamlit Cloud(Linux) 환경: 구글 Noto Sans KR 폰트를 자동 다운로드하여 등록
        font_filename = "NotoSansKR-Regular.ttf"
        if not os.path.exists(font_filename):
            font_url = "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"
            try:
                urllib.request.urlretrieve(font_url, font_filename)
            except Exception:
                pass
        
        if os.path.exists(font_filename):
            fm.fontManager.addfont(font_filename)
            font_prop = fm.FontProperties(fname=font_filename)
            plt.rcParams["font.family"] = font_prop.get_name()
        else:
            plt.rcParams["font.family"] = "sans-serif"
            
    plt.rcParams["axes.unicode_minus"] = False

setup_cloud_korean_font()