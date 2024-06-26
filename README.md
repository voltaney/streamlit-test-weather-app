# 動作確認用のStreamlit App
下記を確認。

- Cache hit/missはどのように起こるか
  - cache_data & session_stateで状態確認
- st.chartlineとplotlyチャートの素朴な描画

## 使用しているAPI
- [Open-Meteo (Free Weather API)](https://open-meteo.com/)

## 使用しているData
- [日本地理情報を公開してくれているGitリポジトリ](https://github.com/dataofjapan/land/tree/master)の`prefecturalCapital.csv`
  - Public Domain