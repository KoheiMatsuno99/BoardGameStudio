# Abstract
ガイスターというボードゲームを開発します。
ガイスターは1対1で対戦するボードゲームです。

# Rules

## Preparation
- ガイスターには青いオバケと赤いオバケの二つのコマがあります。
- 各プレイヤーは、青いオバケと赤いオバケのコマをそれぞれ4つずつ持っています。
- 各プレイヤーは手前の14マスに8つの自分のコマを自由に配置します。
- 各プレイヤーは自分のコマが青いオバケと赤いオバケかは見えますが、相手のコマが青いオバケか赤いオバケかは見えません。

## Game
- 各プレイヤーは交互に自分のコマを縦・横に1マスずつ進めます。
- 進めた先に相手のコマがある場合は、そのコマを取らなければなりません。
- 相手のコマを取った時、そのコマが青いオバケなのか赤いオバケなのかを知ることができます。
- 各プレイヤーから見て相手側の一番奥のマスは脱出マスとなっています。
- 自分のコマが脱出マスに到達し、その次のターンで相手に取られなければ、そのコマをボードから脱出させることができます。

## Game set
- 勝利条件は以下の3つです。
    - 相手の青いオバケを4つ全て取る。
    - 自分の赤いオバケを4つ全て取らせる。
    - 自分の青いオバケのコマを1つでも脱出させる。

# Functional requirements
- 上記のルールに従い、オフラインモードを実装すること
    - オフラインモードではCPUとの対戦を行う

## TBD
- オンラインモードを実装すること
    - オンラインモードではホストがロビー画面からルームを作成する
    - ルームコードを入力したプレイヤーはホストのルームに入り対戦を行う
- 通常のガイスターに加えて、相手の手駒のみ見ることができるリバースモードを実装すること 

# Non-functional requirements
- ゲームの追加・変更が容易なコードであること
- スマホ・PCでも見やすいUIとなっていること

# Technology Stack
使用技術は以下の通り
- Frontend
    - TypeScript
    - React
- Backend
    - Python
    - Django
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
Djangoを選定したのはPythonの中では最もメジャーなフレームワークであり、REST APIを開発する上で便利なDjango Rest Frameworkを提供しているから。


### CI/CD
ソースコードをGitHubで管理しているため、GitHubとの相性が良いGitHub Actionsを採用。
バックエンドはPythonで書いているため、PEP8に準拠するようにFlake8、BlackをCIで実行させた。

# Design

## Architecture

MVCモデルを採用
ViewはReactで実装した。
ControllerとしてクライアントサイドはTypeScript、サーバーサイドはDjangoで実装し、JSON形式でデータの受け渡しを行った。
ModelはPythonで実装した。

## Activity Diagram
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/cae52556-86fe-43f0-8087-734b4641b61f)

## Class Design
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/c3bbcc16-86e4-4b04-af1a-be7ce20f56f9)

