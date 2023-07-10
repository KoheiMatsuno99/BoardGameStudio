# Abstract
ガイスターというボードゲームを開発します。
ガイスターは1対1で対戦するボードゲームです。

アプリケーションURL：https://board-game-studio.vercel.app/



https://github.com/Amnis333/BoardGameStudio/assets/83019007/7eb81900-0217-4ce0-95d0-ee04d0c6d31d



# Rules

- ゲームの目的は、相手のゴーストを捕まえることです
- ゴーストは、赤と青の2色があります。ただし、相手のゴーストの種類は捕まえるまでわかりません
- 各プレイヤーから見て相手側の角のマスは脱出マスとなっています
- 自分の青ゴーストが脱出マスに到達し、その次のターンで取られなければ、そのゴーストはボードから脱出します
- 勝利条件は、「相手の青ゴーストを全て取る」「自分の赤ゴーストを全て取らせる」「自分の青ゴーストを脱出させる」のどれかを満たすことです

# Functional requirements
- 上記のルールに従い、CPUとの対戦モードを実装すること

# Non-functional requirements
- ゲームの追加・変更が容易なコードであること
- スマホ・PCでも見やすいUIとなっていること

# Technology Stack
使用技術は以下の通り
- Frontend
    - TypeScript 4.9.5
    - React　18.2.0
- Backend
    - Python 3.9.6
    - Django 4.2.1
- CI/CD
    - GitHub Actions
- Deploy
    - Vercel
    - Elastic Beanstalk    


## Why are these technology ?

### Frontend
TypeScriptを差し置いてあえてJavaScriptで開発する理由がないため。

### Backend
今回開発するアプリは、高負荷なアクセスは想定されず、ターン制のボードゲームのため信頼性やレイテンシーを厳格に意識する必要性は薄い。
そのため、GolangやJavaなどでは長所を活かしきれず、バックエンドを短いコードで高速に開発できる動的型付け言語の方が適していると判断した。
バックエンドにNodeJSを採用しなかったのはフロントエンドとバックエンドの責務を明確に分離することを意識したかったため。
PHPやRubyを採用しなかったのはPythonの方が馴染みがあり好みの言語のため。
Pythonの弱点である弱い型付けについては、型ヒントやmypyを使用することで型安全性の改善と高速な開発を両立した。
また、Pythonの中では最もメジャーなフレームワークであり、REST APIを開発する上で便利かつ枯れた技術であるDjango Rest Frameworkを提供しているため、Djangoを選定した。


### CI/CD
ソースコードをGitHubで管理しているため、GitHubとの相性が良いGitHub Actionsを採用。
バックエンドはPythonで書いているため、PEP8に準拠するようにFlake8、BlackをCIで実行させた。

# Design

## Architecture

３層アーキテクチャ・MVCを採用
アプリ全体の構成としては画面の描画を行うプレゼンテーション層・ゲームのロジックを処理するドメイン層・ゲームの状態管理を行うデータ層の3層アーキテクチャに基づいている。
フロントエンドとバックエンドの責務の分離、フロントエンド・バックエンド内でもそれぞれの責務の分離を意識した。

フロントエンドでは、コンポーネントが画面の描画を行い、useStateがイベントの状態を検知して画面制御のロジックを担当、バックエンドへリクエストを送るAPIがコントローラーとしてMVCを再現している。
バックエンドでは、ゲームのロジックをgeister.pyで処理し、ゲームの状態管理（コマの位置情報など）をデータベース（models.py）が担当し、views.pyがフロントエンドから送られたデータの受け取りおよび、バックエンドから送るデータの受け渡しを担当している。
そして、フロントエンドから送られたデータのデシリアライズ・フロントエンドへ送るデータのシリアライズはserializer.pyが担当している。

## Activity Diagram
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/cae52556-86fe-43f0-8087-734b4641b61f)

## Class Diagram
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/3bad1098-bd9c-4057-9e33-640a32ff900f)


