from flask_frozen import Freezer
from travelers_app_shortcuts import app, KOREAN_APPS

freezer = Freezer(app)

app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
app.config['FREEZER_RELATIVE_URLS'] = True

@freezer.register_generator
def download_app():
    for category_id, category in KOREAN_APPS.items():
        apps = category["apps"]
        for idx, app in enumerate(apps):
            # iOS
            yield {
                "category_id": category_id,
                "app_index": idx,
                "platform": "ios"
            }

            # Android
            yield {
                "category_id": category_id,
                "app_index": idx,
                "platform": "android"
            }

if __name__ == '__main__':
    freezer.freeze()