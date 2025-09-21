from flask import Flask, render_template_string, request, redirect
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
                ios_url="itms-apps://apps.apple.com/kr/app/kakaot/id981110422",
                android_url="market://details?id=com.kakao.taxi",
                icon="🚕",
                keywords=["taxi", "cab", "ride", "uber", "transport", "car", "driver"]
            ),
            App(
                name="Naver Map",
                korean_name="네이버지도",
                description="Korea's best map app",
                ios_url="itms-apps://apps.apple.com/kr/app/naver-map-navigation/id311867728",
                android_url="market://details?id=com.nhn.android.nmap",
                icon="🗺️",
                keywords=["map", "navigation", "direction", "location", "gps", "route", "address"]
            ),
            App(
                name="Korail Talk",
                korean_name="코레일톡",
                description="Train booking and ticket reservation",
                ios_url="itms-apps://apps.apple.com/kr/app/korail-talk/id1064853845",
                android_url="market://details?id=kr.co.korail.mobile.sealog",
                icon="🚄",
                keywords=["train", "railway", "ticket", "booking", "reservation", "ktx", "korail"]
            ),
            App(
                name="Subway Korea",
                korean_name="지하철맵",
                description="Seoul subway map",
                ios_url="itms-apps://apps.apple.com/app/id325924444",
                android_url="market://details?id=kr.co.citymapper.seoul",
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
                description="Restaurant reservation and booking",
                ios_url="itms-apps://apps.apple.com/kr/app/catch-table-book-restaurants/id1639046576",
                android_url="market://details?id=kr.co.catchtable.global.catchtable_global",
                icon="🍽️",
                keywords=["restaurant", "reservation", "booking", "table", "dining", "eat", "food"]
            ),
            App(
                name="Baedal Minjok",
                korean_name="배달의민족",
                description="Korea's #1 food delivery app",
                ios_url="itms-apps://apps.apple.com/kr/app/baedal-minjog/id378084485",
                android_url="market://details?id=com.sampleapp",
                icon="🍕",
                keywords=["delivery", "food", "order", "restaurant", "meal", "korean", "baemin"]
            ),
            App(
                name="Coupang Eats",
                korean_name="쿠팡이츠",
                description="Fast delivery by Coupang",
                ios_url="itms-apps://apps.apple.com/kr/app/coupang-eats-delivery/id1489897288",
                android_url="market://details?id=com.coupang.mobile.eats",
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
                description="Official Korea tourism information app",
                ios_url="itms-apps://apps.apple.com/kr/app/visit-korea/id1453991828",
                android_url="market://details?id=kr.co.kto.visitkorea",
                icon="🇰🇷",
                keywords=["tourism", "tourist", "attraction", "visit", "sightseeing", "korea", "travel"]
            ),
            App(
                name="Visit Seoul",
                korean_name="비지트서울",
                description="Official Seoul city tourism guide",
                ios_url="itms-apps://apps.apple.com/kr/app/visit-seoul/id1018639300",
                android_url="market://details?id=com.seoul.visitseoul",
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
                description="Korea's national messenger, essential app!",
                ios_url="itms-apps://apps.apple.com/kr/app/kakaotalk/id362057947",
                android_url="market://details?id=com.kakao.talk",
                icon="💬",
                keywords=["message", "messenger", "chat", "talk", "communication", "kakao", "text"]
            ),
            App(
                name="Papago",
                korean_name="파파고",
                description="Naver's AI translator, best for Korean",
                ios_url="itms-apps://apps.apple.com/kr/app/papago-ai-translator/id1147874819",
                android_url="market://details?id=com.naver.labs.translator",
                icon="🌐",
                keywords=["translate", "translator", "language", "korean", "english", "communication", "ai"]
            ),
            App(
                name="Currency",
                korean_name="환율계산기",
                description="Real-time currency converter",
                ios_url="itms-apps://apps.apple.com/app/id284220417",
                android_url="market://details?id=com.xe.currency",
                icon="💱",
                keywords=["currency", "exchange", "money", "rate", "convert", "won", "dollar"]
            )
        ]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Essential Korean Apps Guide - For Foreign Tourists</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #87CEEB 0%, #B0E0E6 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.4rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .search-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
            margin-top: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .search-btn:hover {
            background: white;
            color: #87CEEB;
        }
        
        .categories {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }
        
        .category {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .category:hover {
            transform: translateY(-5px);
        }
        
        .category-header {
            text-align: center;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
            cursor: pointer;
        }
        
        .category-title {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 8px;
        }
        
        .category-desc {
            color: #666;
            font-size: 0.9rem;
        }
        
        .toggle-btn {
            background: linear-gradient(45deg, #87CEEB, #ADD8E6);
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            color: white;
            font-size: 1.4rem;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            margin-top: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 4px 15px rgba(135, 206, 235, 0.4);
            position: relative;
            overflow: hidden;
        }
        
        .toggle-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: all 0.6s ease;
        }
        
        .toggle-btn:hover::before {
            width: 100%;
            height: 100%;
        }
        
        .toggle-btn:hover {
            transform: translateY(-3px) scale(1.1);
            box-shadow: 0 8px 25px rgba(135, 206, 235, 0.6);
        }
        
        .toggle-btn:active {
            transform: translateY(-1px) scale(1.05);
        }
        
        .toggle-icon {
            position: relative;
            z-index: 2;
            transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .toggle-icon.rotated {
            transform: rotate(180deg) scale(1.1);
        }
        
        .toggle-icon svg {
            transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        .apps {
            display: flex;
            flex-direction: column;
            gap: 15px;
            transition: all 0.3s ease;
            overflow: hidden;
        }
        
        .app-card {
            display: flex;
            align-items: center;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 12px;
            transition: all 0.2s ease;
        }
        
        .app-card:hover {
            background: #e9ecef;
            transform: scale(1.02);
        }
        
        .app-icon {
            font-size: 2rem;
            margin-right: 15px;
        }
        
        .app-info {
            flex: 1;
        }
        
        .app-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        
        .app-description {
            font-size: 0.85rem;
            color: #888;
        }
        
        .download-buttons {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .download-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            color: white;
            font-weight: 600;
            font-size: 0.8rem;
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .ios-btn {
            background: #007AFF;
        }
        
        .ios-btn:hover {
            background: #0056CC;
        }
        
        .android-btn {
            background: #34A853;
        }
        
        .android-btn:hover {
            background: #2E7D32;
        }
        
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-content {
            background: white;
            border-radius: 20px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .search-modal {
            max-height: 70vh;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 25px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .modal-header h3 {
            color: #333;
            margin: 0;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 24px;
            color: #666;
            cursor: pointer;
            width: 30px;
            height: 30px;
        }
        
        .close-btn:hover {
            color: #333;
        }
        
        .modal-body {
            padding: 25px;
            overflow-y: auto;
            max-height: 50vh;
        }
        
        #searchInput {
            width: 100%;
            padding: 15px;
            border: 2px solid #eee;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 20px;
            outline: none;
        }
        
        #searchInput:focus {
            border-color: #87CEEB;
        }
        
        .search-result-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: all 0.2s ease;
        }
        
        .search-result-item:hover {
            background: #e9ecef;
            transform: scale(1.02);
        }
        
        .no-results {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            color: white;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .categories {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 1.9rem;
            }
            
            .download-buttons {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Korea App Navigator for International Travelers</h1>
            <p>KANIT be of any help?</p>
            <button class="search-btn" onclick="openSearchModal()">🔍 Search Apps</button>
        </div>
        
        <div class="categories">
            {% for category_id, category_data in categories.items() %}
            <div class="category">
                <div class="category-header">
                    <h2 class="category-title">{{ category_data.category_name }}</h2>
                    <p class="category-desc">{{ category_data.category_desc }}</p>
                </div>
                
                <div class="apps" id="apps-{{ category_id }}" style="display: none;">
                    {% for app in category_data.apps %}
                    <div class="app-card">
                        <div class="app-icon">{{ app.icon }}</div>
                        <div class="app-info">
                            <div class="app-name">{{ app.name }}</div>
                            <div class="app-description">{{ app.description }}</div>
                        </div>
                        <div class="download-buttons">
                            <a href="/download/{{ category_id }}/{{ loop.index0 }}/ios" class="download-btn ios-btn">
                                iOS
                            </a>
                            <a href="/download/{{ category_id }}/{{ loop.index0 }}/android" class="download-btn android-btn">
                                Android
                            </a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <button class="toggle-btn" onclick="toggleCategory('{{ category_id }}')" aria-label="Toggle category">
                    <div class="toggle-icon">
                        <svg width="20" height="12" viewBox="0 0 20 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M2 2L10 8L18 2" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                </button>
            </div>
            {% endfor %}
        </div>
        
        <!-- Search Modal -->
        <div id="searchModal" class="modal" style="display: none;">
            <div class="modal-content search-modal">
                <div class="modal-header">
                    <h3>Search Apps</h3>
                    <button class="close-btn" onclick="closeSearchModal()">×</button>
                </div>
                <div class="modal-body">
                    <input type="text" id="searchInput" placeholder="Search for apps... (e.g., taxi, food, translate)" oninput="searchApps()">
                    <div id="searchResults"></div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Made for tourists visiting South Korea 🇰🇷</p>
            <p>Your essential app guide for Korea</p>
        </div>
    </div>

    <script>
        // 검색 모달 열기/닫기
        function openSearchModal() {
            document.getElementById('searchModal').style.display = 'flex';
            document.getElementById('searchInput').focus();
        }
        
        function closeSearchModal() {
            document.getElementById('searchModal').style.display = 'none';
            document.getElementById('searchInput').value = '';
            document.getElementById('searchResults').innerHTML = '';
        }
        
        // 모달 바깥 클릭 시 닫기
        document.addEventListener('click', function(e) {
            const modal = document.getElementById('searchModal');
            if (e.target === modal) {
                closeSearchModal();
            }
        });
        
        // 앱 검색 함수
        function searchApps() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
            const resultsContainer = document.getElementById('searchResults');
            
            if (!searchTerm) {
                resultsContainer.innerHTML = '';
                return;
            }
            
            const apps = {{ categories | tojson | safe }};
            let results = [];
            
            // 모든 앱에서 검색
            Object.keys(apps).forEach(categoryId => {
                apps[categoryId].apps.forEach((app, index) => {
                    const matchScore = calculateMatchScore(app, searchTerm);
                    if (matchScore > 0) {
                        results.push({
                            app: app,
                            categoryId: categoryId,
                            appIndex: index,
                            score: matchScore
                        });
                    }
                });
            });
            
            // 점수 순으로 정렬
            results.sort((a, b) => b.score - a.score);
            
            // 결과 표시
            displaySearchResults(results);
        }
        
        // 매칭 점수 계산
        function calculateMatchScore(app, searchTerm) {
            let score = 0;
            
            // 앱 이름 매칭 (높은 점수)
            if (app.name.toLowerCase().includes(searchTerm)) score += 10;
            
            // 설명 매칭 (중간 점수)
            if (app.description.toLowerCase().includes(searchTerm)) score += 5;
            
            // 키워드 매칭 (기본 점수)
            if (app.keywords) {
                app.keywords.forEach(keyword => {
                    if (keyword.toLowerCase().includes(searchTerm) || searchTerm.includes(keyword.toLowerCase())) {
                        score += 3;
                    }
                });
            }
            
            return score;
        }
        
        // 검색 결과 표시
        function displaySearchResults(results) {
            const resultsContainer = document.getElementById('searchResults');
            
            if (results.length === 0) {
                resultsContainer.innerHTML = '<div class="no-results">No apps found. Try different keywords!</div>';
                return;
            }
            
            let html = '';
            results.forEach(result => {
                const app = result.app;
                html += `
                    <div class="search-result-item" onclick="selectSearchResult('${result.categoryId}', ${result.appIndex})">
                        <div class="app-icon" style="font-size: 1.5rem; margin-right: 15px;">${app.icon}</div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; color: #333;">${app.name}</div>
                            <div style="font-size: 0.85rem; color: #888;">${app.description}</div>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 5px;">
                            <a href="/download/${result.categoryId}/${result.appIndex}/ios" class="download-btn ios-btn" style="padding: 5px 10px; font-size: 0.7rem;" onclick="event.stopPropagation()">iOS</a>
                            <a href="/download/${result.categoryId}/${result.appIndex}/android" class="download-btn android-btn" style="padding: 5px 10px; font-size: 0.7rem;" onclick="event.stopPropagation()">Android</a>
                        </div>
                    </div>
                `;
            });
            
            resultsContainer.innerHTML = html;
        }
        
        // 검색 결과 선택 시 해당 카테고리 열기
        function selectSearchResult(categoryId, appIndex) {
            closeSearchModal();
            toggleCategory(categoryId);
            
            // 해당 앱으로 스크롤
            setTimeout(() => {
                const appCard = document.querySelectorAll(`#apps-${categoryId} .app-card`)[appIndex];
                if (appCard) {
                    appCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    appCard.style.background = '#e3f2fd';
                    setTimeout(() => { appCard.style.background = '#f8f9fa'; }, 2000);
                }
            }, 300);
        }
        
        // ESC 키로 모달 닫기
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeSearchModal();
            }
        });

        // 카테고리 토글 함수
        function toggleCategory(categoryId) {
            const appsContainer = document.getElementById('apps-' + categoryId);
            const toggleIcon = document.querySelector(`[onclick="toggleCategory('${categoryId}')"] .toggle-icon`);
            
            // 다른 모든 카테고리 닫기
            const allAppsContainers = document.querySelectorAll('[id^="apps-"]');
            const allToggleIcons = document.querySelectorAll('.toggle-icon');
            
            allAppsContainers.forEach(container => {
                if (container.id !== 'apps-' + categoryId) {
                    container.style.display = 'none';
                }
            });
            
            allToggleIcons.forEach(icon => {
                if (icon !== toggleIcon) {
                    icon.style.transform = 'rotate(0deg)';
                }
            });
            
            // 현재 카테고리 토글
            if (appsContainer.style.display === 'none') {
                appsContainer.style.display = 'flex';
                toggleIcon.style.transform = 'rotate(180deg) scale(1.1)';
            } else {
                appsContainer.style.display = 'none';
                toggleIcon.style.transform = 'rotate(0deg)';
            }
        }
        
        // 카테고리 헤더 클릭으로도 토글 가능
        document.addEventListener('DOMContentLoaded', function() {
            const categoryHeaders = document.querySelectorAll('.category-header');
            categoryHeaders.forEach(header => {
                header.addEventListener('click', function(e) {
                    if (!e.target.closest('.toggle-btn')) {
                        const categoryId = this.closest('.category').querySelector('[id^="apps-"]').id.replace('apps-', '');
                        toggleCategory(categoryId);
                    }
                });
            });
        });

        // 사용자 디바이스 감지
        function detectPlatform() {
            const userAgent = navigator.userAgent || navigator.vendor || window.opera;
            if (/android/i.test(userAgent)) {
                return 'android';
            } else if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
                return 'ios';
            }
            return 'android'; // 기본값
        }

        // 플랫폼별 버튼 하이라이트
        document.addEventListener('DOMContentLoaded', function() {
            const platform = detectPlatform();
            const buttons = document.querySelectorAll('.download-btn');
            
            buttons.forEach(button => {
                if (button.classList.contains(platform + '-btn')) {
                    button.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
                    button.style.fontWeight = '700';
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, categories=KOREAN_APPS)

@app.route('/download/<category_id>/<int:app_index>/<platform>')
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
        return redirect(url)
        
    except (KeyError, IndexError):
        return "App not found", 404

@app.route('/install-guide')
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
    
    app.run(debug=False, host='0.0.0.0', port=5000)