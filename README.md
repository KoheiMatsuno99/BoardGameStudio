# Abstract
ガイスターというボードゲームを開発します。
ガイスターは1対1で対戦するボードゲームです。

アプリケーションURL：https://board-game-studio.vercel.app/

作成期間：2ヶ月


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


## Why these technology ?

### Frontend

#### TypeScript選定理由
TypeScriptを選定した最大の理由は型付けによる恩恵があるためである。明示的に型を示すことでどのような型の入出力を期待しているのかがわかるため、ソースコードの可読性を高めることができる。また、nullチェックを忘れずに行うため、オブジェクトがnullであることによる実行時エラーを未然に防ぐことができるという点も型付けによるメリットである。

#### React選定理由
今回開発するアプリは**盤面のマスごとに再レンダリングする必要があり、かつそれが頻繁に行われる**という特徴がある。そのため、フレームワークを使用せずにJavaScript/TypeScriptで開発するよりも、仮想DOMを提供しているフレームワークを使用した方が効率的な開発ができるといえる。その中でJavaScriptのメジャーなフレームワークであるVueとReactが候補に上がる。

Reactを選定した理由はアプリを開発した2023年時点で最もメジャーなフレームワークであることと、ReactはJavaScriptに近くVueよりも馴染みやすいという個人的な好みが挙げられる。また、今回開発するゲームはそれほど多くのページは必要がないため、サーバーサイドレンダリングを行う必要性は薄い。そのため、Next.jsは選定しなかった。

### Backend

#### Python選定理由
今回開発するアプリは、**高負荷なアクセスは想定されず、ターン制のボードゲームのため信頼性やレイテンシーを厳格に意識する必要性は薄い**。
そのため、大規模サービスで使用されるもののコードが冗長になりがちなGolangやJavaなどでは長所を活かしきれず、バックエンドを**短いコードで高速に開発できる**動的型付け言語の方が適していると判断した。

バックエンドにNodeJSを採用しなかったのは**フロントエンドとバックエンドの責務を明確に分離する**ことを意識したかったことが挙げられる。なぜなら、フロントエンドとバックエンドを分離することによって問題が発生した時の原因特定がしやすくなることや、アプリ全体の設計の見通しが良くなるためである。また、PHPやRubyを採用しなかったのはPythonの方が馴染みがあったという理由によるものである。

ただし、Pythonは動的型付け言語のため、事前にバグを発見することが静的型付け言語に比べると難しく、例えばオブジェクトがNoneになっていることなどによる実行時エラーが起こりやすいといった弱点がある。
そのため、Pythonの弱点である弱い型付けについては、型ヒントやmypyを使用することで**型安全性の改善と高速な開発**を両立した。

#### Django選定理由
サーバーサイドの言語をPythonにする上で、フレームワークとしてDjango, Flask, FastAPIが候補に挙げられる。
フレームワークが提供している機能はDjangoが最も多く、FastAPIが最も少ない。そのため、開発規模もDjangoが最も大規模開発に向いており、FastAPIが最も小規模開発に向いている。FlaskはDjangoとFastAPIの中間に位置する。

しかし、今回あえてDjangoを選定したのは、Pythonの中で最もメジャーなフレームワークであることが挙げられる。メジャーなフレームワークであるために開発する上で実例が多いことは大きなメリットである。
また、多くの機能を提供しているため、高速な開発が可能であるという点も魅力である。

特に、フロントエンドとバックエンドを分離した開発をする上でREST APIが必要となるが、**REST APIを素早く構築でき、かつ枯れた技術であるDjango Rest Frameworkを提供している**ことは今回Djangoを選定した上で大きな理由となった。

さらに、ORMを提供しているということもDjangoのメリットである。開発当初はデータベースを使用しておらず、Cookieによるゲームの状態管理を行っていた。しかし、リリース後、一部のブラウザで動作しないという報告をユーザーから受けた。
そこで、Cookieからデータベースによる状態管理に移行することとなったが、DjangoがデフォルトでORMを提供しているため、スムーズに移行することができた。

### CI/CD
ソースコードをGitHubで管理しているため、GitHubとの相性が良いGitHub Actionsを採用した。
バックエンドはPythonで書いているため、PEP8に準拠するようにFlake8、BlackをCIで実行させた。

# Design

## Architecture

アプリ全体の構成としては**3層アーキテクチャ**に準拠している。プレゼンテーション層はReactによる画面の描画・イベントの処理およびTypeScriptによるAPIのクライアントサイドの実装が含まれている。そして、アプリケーション層にはDjangoによるAPIのサーバーサイドの実装およびゲームのロジックが含まれている。そして、データ層ではDjangoがMySQLと通信し、データの読み書きを行うようにしている。

![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/ff2ebeba-8d6b-4828-9b24-7259b1dabe0b)


## Activity Diagram
以下はアプリケーション全体の操作フローを示したものである。

ロビー画面からゲーム説明画面に遷移した後、ゲーム画面に遷移する。そして、ゲーム終了後にはロビー画面に戻るようなフローになっている。


![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/c19d3e37-7732-4b14-9579-5d79aa5623ba)


## Class Diagram
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/3bad1098-bd9c-4057-9e33-640a32ff900f)


