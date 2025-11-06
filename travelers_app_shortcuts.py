from flask import Flask, render_template, request, redirect
import webbrowser
import threading
import time
from dataclasses import dataclass
from typing import Dict, List

app = Flask(__name__)

@dataclass
class App:
    name: str
    korean_name: str
    description: str
    ios_url: str
    android_url: str
    icon: str = "📱"
    keywords: List[str] = None

# 한국 필수 앱들 데이터
KOREAN_APPS = {
    "transportation_maps": {
        "category_name": "Transportation & Maps 🚗",
        "category_desc": "Taxi, Train, Subway, Navigation",
        "apps": [
            App(
                name="Kakao T",
                korean_name="카카오 T",
                description="Korea's Uber! Taxi calling app",
                ios_url="https://apps.apple.com/kr/app/kakaot/id981110422",
                android_url="https://play.google.com/store/apps/details?id=com.kakao.taxi",
                icon="🚕",
                keywords=["taxi", "cab", "ride", "uber", "transport", "car", "driver"]
            ),
            App(
                name="Naver Map",
                korean_name="네이버지도",
                description="Korea's best map app",
                ios_url="https://apps.apple.com/kr/app/naver-map-navigation/id311867728",
                android_url="https://play.google.com/store/apps/details/NAVER_Map_Navigation?id=com.nhn.android.nmap",
                icon="🗺️",
                keywords=["map", "navigation", "direction", "location", "gps", "route", "address"]
            ),
            App(
                name="Korail Talk",
                korean_name="코레일톡",
                description="Train ticket reservation",
                ios_url="https://apps.apple.com/kr/app/%EC%BD%94%EB%A0%88%EC%9D%BC%ED%86%A1/id1000558562",
                android_url="https://play.google.com/store/apps/details?id=com.korail.talk",
                icon="🚄",
                keywords=["train", "railway", "ticket", "booking", "reservation", "ktx", "korail"]
            ),
            App(
                name="Subway Korea",
                korean_name="지하철맵",
                description="Seoul subway map",
                ios_url="https://apps.apple.com/app/id325924444",
                android_url="https://play.google.com/store/apps/details?id=com.imagedrome.jihachul",
                icon="🚇",
                keywords=["subway", "metro", "underground", "train", "seoul", "station", "line"]
            )
        ]
    },
    "dining": {
        "category_name": "Dining & Delivery 🍽️",
        "category_desc": "Restaurant reservations and food delivery",
        "apps": [
            App(
                name="Catchtable",
                korean_name="캐치테이블",
                description="Restaurant reservation",
                ios_url="https://apps.apple.com/kr/app/catch-table-book-restaurants/id1639046576",
                android_url="https://play.google.com/store/apps/details?id=kr.co.catchtable.global.catchtable_global",
                icon="🍽️",
                keywords=["restaurant", "reservation", "booking", "table", "dining", "eat", "food"]
            ),
            App(
                name="Baedal Minjok",
                korean_name="배달의민족",
                description="Korea's #1 food delivery app",
                ios_url="https://apps.apple.com/kr/app/baedal-minjog/id378084485",
                android_url="https://play.google.com/store/apps/details?id=com.sampleapp",
                icon="🍕",
                keywords=["delivery", "food", "order", "restaurant", "meal", "korean", "baemin"]
            ),
            App(
                name="Coupang Eats",
                korean_name="쿠팡이츠",
                description="Food delivery by Coupang",
                ios_url="https://apps.apple.com/kr/app/%EC%BF%A0%ED%8C%A1%EC%9D%B4%EC%B8%A0-%EC%99%80%EC%9A%B0%ED%9A%8C%EC%9B%90-%EB%AC%B4%EB%A3%8C%EB%B0%B0%EB%8B%AC/id1445504255",
                android_url="https://play.google.com/store/apps/details?id=com.coupang.mobile.eats",
                icon="🍜",
                keywords=["delivery", "food", "fast", "order", "coupang", "meal", "quick"]
            )
        ]
    },
    "tourist_attractions": {
        "category_name": "Tourist Attractions 🏛️",
        "category_desc": "Discover attractions and tourist information",
        "apps": [
            App(
                name="Visit Korea",
                korean_name="비지트코리아",
                description="Korea tourism information",
                ios_url="https://apps.apple.com/kr/app/visitkorea/id417340885",
                android_url="https://play.google.com/store/apps/details?id=com.visitkorea.eng",
                icon="🇰🇷",
                keywords=["tourism", "tourist", "attraction", "visit", "sightseeing", "korea", "travel"]
            ),
            App(
                name="Visit Seoul",
                korean_name="비지트서울",
                description="Seoul city tourism information",
                ios_url="https://apps.apple.com/kr/app/visit-seoul-%EB%B9%84%EC%A7%93%EC%84%9C%EC%9A%B8/id360156429",
                android_url="https://play.google.com/store/apps/details?id=com.sto.android.client.itourseoul",
                icon="🏙️",
                keywords=["seoul", "tourism", "tourist", "attraction", "city", "guide", "sightseeing"]
            )
        ]
    },
    "utility": {
        "category_name": "Travel Utility 🌐",
        "category_desc": "Translation, messaging and currency tools for tourists",
        "apps": [
             App(
                name="KakaoTalk",
                korean_name="카카오톡",
                description="Korea's national messenger",
                ios_url="https://apps.apple.com/kr/app/kakaotalk/id362057947",
                android_url="https://play.google.com/store/apps/details?id=com.kakao.talk",
                icon="💬",
                keywords=["message", "messenger", "chat", "talk", "communication", "kakao", "text"]
            ),
            App(
                name="Papago",
                korean_name="파파고",
                description="AI translator, best for Korean",
                ios_url="https://apps.apple.com/kr/app/papago-ai-translator/id1147874819",
                android_url="https://play.google.com/store/apps/details?id=com.naver.labs.translator",
                icon="🌐",
                keywords=["translate", "translator", "language", "korean", "english", "communication", "ai"]
            ),
            App(
                name="Currency",
                korean_name="환율계산기",
                description="Real-time currency converter",
                ios_url="https://apps.apple.com/app/id284220417",
                android_url="https://play.google.com/store/apps/details?id=com.currencyapp.currencyandroid",
                icon="💱",
                keywords=["currency", "exchange", "money", "rate", "convert", "won", "dollar"]
            )
        ]
    }
}

@app.route('/')
def index():
    return render_template("index.jinja2", categories=KOREAN_APPS)

@app.route('/download/<category_id>/<int:app_index>/<platform>/')
def download_app(category_id, app_index, platform):
    try:
        category = KOREAN_APPS[category_id]
        app = category['apps'][app_index]
        
        if platform == 'ios':
            url = app.ios_url
        elif platform == 'android':
            url = app.android_url
        else:
            return "Invalid platform", 400
            
        # 리다이렉트
        # return redirect(url)
        return f"""
        <html>
            <head>
                <meta http-equiv="refresh" content="0; url={url}">
            </head>
            <body>
                <p>Redirecting to <a href="{url}">{url}</a>...</p>
            </body>
        </html>
        """
    
        
    except (KeyError, IndexError):
        return "App not found", 404

@app.route('/install-guide/')
def install_guide():
    """Installation guide page"""
    guide_html = """
    <h1>App Installation Guide</h1>
    <h2>iOS Users</h2>
    <ol>
        <li>Click the link to go to App Store</li>
        <li>Tap 'GET' button</li>
        <li>Authenticate with Face ID, Touch ID or password</li>
    </ol>
    
    <h2>Android Users</h2>
    <ol>
        <li>Click the link to go to Google Play Store</li>
        <li>Tap 'Install' button</li>
        <li>Allow permissions if requested</li>
    </ol>
    """
    return guide_html

def open_browser():
    """서버 시작 후 브라우저 자동 열기"""
    time.sleep(1.5)  # 서버 시작 대기
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Korean Essential Apps Guide Server Starting!")
    print("📱 Browser will open automatically...")
    print("🌐 Help foreign tourists easily download essential Korean apps!")
    
    # 백그라운드에서 브라우저 열기
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)