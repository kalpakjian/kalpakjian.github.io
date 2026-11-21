# 第 16 章（附加）· Iris 分類：Django × 機器學習

**導讀**：這個範例把**機器學習模型接進 Django**：先用 scikit-learn 訓練一個鳶尾花（Iris）分類器並存成檔案，再由 Django 提供**網頁表單**與 **JSON API** 兩種預測介面。是「把 ML 模型變成服務」的最小實作。

**專案原始碼（GitHub）**：https://github.com/kalpakjian/django-ml-app

## 1. 專案簡介

- **主題**：輸入鳶尾花的 4 個尺寸特徵，預測品種（setosa／versicolor／virginica）。
- **模型**：`RandomForestClassifier`（200 棵樹），以 scikit-learn 內建 Iris 資料集訓練。
- **兩種介面**：網頁表單（`/predict/`）與 JSON API（`/api/predict/`）。
- **技術**：Django 5.2 + scikit-learn + joblib。

## 2. 專案結構

```
django-ml-app/
    manage.py
    train.py                    # 訓練並存出模型
    db.sqlite3
    requirements.txt
    README.md
    mlapp/                      # 專案設定
        settings.py
        urls.py
        wsgi.py / asgi.py
    predictor/                  # 應用（App）
        forms.py                # IrisForm（4 個特徵欄位）
        services.py             # 載入模型 + 預測
        views.py                # 表單 / 表單預測 / API
        urls.py
        model/iris_rf.joblib    # 訓練好的模型
    templates/predictor/predict_form.html
```

設計上把「**訓練**」（`train.py`）與「**服務**」（`predictor/`）分開：訓練只跑一次、產出模型檔；Django 只負責載入模型與推論。
## 3. 訓練模型（train.py）

<figure class="fig-svg"><svg viewBox="0 0 820 192" width="100%" role="img" aria-label="Iris 範例流程：載入資料 → 切分 → 訓練隨機森林 → 存檔；Django 載入模型做預測" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="16" y="58" width="150" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="91" y="84" text-anchor="middle" font-size="13" fill="#e6edf3">load_iris()</text><text x="91" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">150 筆 · 4 特徵</text><line x1="168" y1="88" x2="204" y2="88" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="208" y="58" width="160" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="288" y="84" text-anchor="middle" font-size="12.5" fill="#e6edf3">train_test_split</text><text x="288" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">80／20 分層切分</text><line x1="370" y1="88" x2="406" y2="88" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="410" y="58" width="180" height="60" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="500" y="84" text-anchor="middle" font-size="13" fill="#e6edf3">RandomForest</text><text x="500" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">n_estimators=200</text><line x1="592" y1="88" x2="628" y2="88" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="632" y="58" width="172" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="718" y="84" text-anchor="middle" font-size="13" fill="#e6edf3">joblib 存檔</text><text x="718" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">iris_rf.joblib</text><path d="M718 120 L718 156 L91 156 L91 122" fill="none" stroke="#39d0d8" stroke-width="1.5" stroke-dasharray="5 4"/></g><text x="410" y="182" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">Django 啟動時載入模型 → 表單／API 送入 4 個特徵 → predict_proba 回傳各類別機率</text><figcaption>圖：Iris 範例的訓練與服務流程。</figcaption></svg></figure>

```
# train.py
from pathlib import Path
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_DIR = Path("predictor") / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "iris_rf.joblib"

def main():
    data = load_iris()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    joblib.dump(
        {
            "estimator": clf,
            "target_names": data.target_names,
            "feature_names": data.feature_names,
        },
        MODEL_PATH,
    )
    print(f"Saved model to {MODEL_PATH.resolve()}")

if __name__ == "__main__":
    main()
```

**重點**

- `load_iris()`：scikit-learn 內建的鳶尾花資料集（150 筆、4 特徵、3 類）。
- `train_test_split(..., stratify=y)`：依類別比例分層切分訓練／測試集。
- `RandomForestClassifier(n_estimators=200)`：200 棵決策樹的隨機森林。
- 把 **estimator + 類別名稱 + 特徵名稱** 一起 `joblib.dump` 存檔——推論時才知道欄位順序與標籤。
## 4. 推論服務（services.py）

```
# predictor/services.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import joblib
import numpy as np

_MODEL_CACHE: Dict[str, Any] = {}

def get_model_bundle():
    """載入並快取模型（estimator / target_names / feature_names）。"""
    global _MODEL_CACHE
    if "bundle" not in _MODEL_CACHE:
        model_path = Path(__file__).resolve().parent / "model" / "iris_rf.joblib"
        _MODEL_CACHE["bundle"] = joblib.load(model_path)
    return _MODEL_CACHE["bundle"]

def predict_iris(features):
    """features: 4 個 float（sepal_length, sepal_width, petal_length, petal_width）"""
    bundle = get_model_bundle()
    clf = bundle["estimator"]
    target_names = bundle["target_names"]

    X = np.array([features], dtype=float)
    proba = clf.predict_proba(X)[0]
    idx = int(np.argmax(proba))
    return {
        "class_index": idx,
        "class_name": str(target_names[idx]),
        "probabilities": {str(name): float(p) for name, p in zip(target_names, proba)},
    }
```

**重點**：`_MODEL_CACHE` 讓模型**只載入一次**（避免每個請求都重讀檔案）；`predict_proba` 回傳各類別機率。

## 5. 表單與視圖

```
# predictor/forms.py
from django import forms

class IrisForm(forms.Form):
    sepal_length = forms.FloatField(min_value=0, label="Sepal length (cm)")
    sepal_width  = forms.FloatField(min_value=0, label="Sepal width (cm)")
    petal_length = forms.FloatField(min_value=0, label="Petal length (cm)")
    petal_width  = forms.FloatField(min_value=0, label="Petal width (cm)")
```

```
# predictor/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .forms import IrisForm
from .services import predict_iris
import json

def home(request):
    return render(request, "predictor/predict_form.html", {"form": IrisForm()})

@require_http_methods(["POST"])
def predict_view(request):
    form = IrisForm(request.POST)
    if not form.is_valid():
        return render(request, "predictor/predict_form.html", {"form": form})
    data = form.cleaned_data
    features = [data["sepal_length"], data["sepal_width"], data["petal_length"], data["petal_width"]]
    result = predict_iris(features)
    return render(request, "predictor/predict_form.html",
                  {"form": IrisForm(), "result": result, "submitted": True})

@csrf_exempt
@require_http_methods(["POST"])
def predict_api(request):
    if request.META.get("CONTENT_TYPE", "").startswith("application/json"):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    else:
        payload = request.POST.dict()

    required = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    missing = [k for k in required if k not in payload]
    if missing:
        return JsonResponse({"error": f"Missing: {', '.join(missing)}"}, status=400)

    try:
        features = [float(payload[k]) for k in required]
    except ValueError:
        return JsonResponse({"error": "All features must be numeric."}, status=400)

    return JsonResponse(predict_iris(features))
```

**重點**

- `predict_view`：網頁表單走 POST，驗證後呼叫 `predict_iris`，再渲染結果。
- `predict_api`：JSON API，接受 `application/json` 或表單編碼；缺欄位／非數字都回 400。
- `@csrf_exempt`：API 端點的示範用法（正式環境建議改用 Token 驗證）。
## 6. 路由與模板

```
# predictor/urls.py
from django.urls import path
from .views import home, predict_view, predict_api

urlpatterns = [
    path("", home, name="home"),
    path("predict/", predict_view, name="predict"),
    path("api/predict/", predict_api, name="predict_api"),
]
```

模板 `templates/predictor/predict_form.html`：一個 4 欄表單 + 結果區塊。

```
<form action="/predict/" method="post">
    {% csrf_token %}
    <label for="id_sepal_length">Sepal length (cm)</label>
    {{ form.sepal_length }}
    ...（其餘 3 個欄位同理）
    <button type="submit">Predict</button>
</form>

{% if submitted and result %}
<div class="result">
    Predicted class: {{ result.class_name }}
    <ul>
    {% for name, p in result.probabilities.items %}
        <li>{{ name }}: {{ p|floatformat:3 }}</li>
    {% endfor %}
    </ul>
</div>
{% endif %}
```

## 7. 執行步驟

```
# 1. 建立並啟用虛擬環境
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # macOS / Linux

# 2. 安裝套件
pip install -r requirements.txt

# 3. 訓練並存出模型（產生 predictor/model/iris_rf.joblib）
python train.py

# 4. 遷移並啟動
python manage.py migrate
python manage.py runserver
```

- 網頁預測：http://127.0.0.1:8000/
- JSON API：

```
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

## 8. 重點整理

- **訓練與服務分離**：`train.py` 只管訓練存檔；Django 只負責載入模型與推論。
- **模型快取**：模組層級的 `_MODEL_CACHE` 讓模型只載入一次。
- **雙介面**：同一套 `predict_iris()` 同時服務網頁表單與 JSON API。
- **存檔要帶 metadata**：類別名稱與特徵名稱一起存，才不會搞錯欄位順序與標籤。
