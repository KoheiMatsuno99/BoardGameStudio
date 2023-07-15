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
今回開発するアプリは盤面のマスごとに再レンダリングする必要があり、かつそれが頻繁に行われるという特徴がある。そのため、フレームワークを使用せずにJavaScript/TypeScriptで開発するよりも、仮想DOMを提供しているフレームワークを使用した方が効率的な開発ができるといえる。その中でJavaScriptのメジャーなフレームワークであるVueとReactが候補に上がる。Reactを選定した理由はアプリを開発した2023年時点で最もメジャーなフレームワークであることと、Reactはフレームワークを使用しないJavaScriptに近くVueよりも馴染みやすいという個人的な好みが挙げられる。
TypeScriptを選定した最大の理由は型付けによる恩恵があるためである。明示的に型を示すことでどのような型の入出力を期待しているのかがわかるため、ソースコードの可読性を高めることができる。また、nullチェックを忘れずに行うため、オブジェクトがnullであることによる実行時エラーを未然に防ぐことができるという点も型付けによるメリットである。

### Backend
今回開発するアプリは、高負荷なアクセスは想定されず、ターン制のボードゲームのため信頼性やレイテンシーを厳格に意識する必要性は薄い。
そのため、GolangやJavaなどでは長所を活かしきれず、バックエンドを短いコードで高速に開発できる動的型付け言語の方が適していると判断した。
バックエンドにNodeJSを採用しなかったのはフロントエンドとバックエンドの責務を明確に分離することを意識したかったことが挙げられる。
また、PHPやRubyを採用しなかったのはPythonの方が馴染みがあったという理由によるものである。
Pythonの弱点である弱い型付けについては、型ヒントやmypyを使用することで型安全性の改善と高速な開発を両立した。
また、Pythonの中では最もメジャーなフレームワークであり、REST APIを開発する上で便利かつ枯れた技術であるDjango Rest Frameworkを提供しているため、Djangoを選定した。


### CI/CD
ソースコードをGitHubで管理しているため、GitHubとの相性が良いGitHub Actionsを採用した。
バックエンドはPythonで書いているため、PEP8に準拠するようにFlake8、BlackをCIで実行させた。

# Design

## Architecture

３層アーキテクチャ・MVCを採用
アプリ全体の構成としては画面の描画を行うプレゼンテーション層・ゲームのロジックを処理するドメイン層・ゲームの状態管理を行うデータ層の3層アーキテクチャに基づいている。
フロントエンドとバックエンドの責務の分離、フロントエンド・バックエンド内でもそれぞれの責務の分離を意識した。

![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/528b6765-f9a3-477f-b69c-8aee42e2e29e)


## Activity Diagram
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/cae52556-86fe-43f0-8087-734b4641b61f)

## Class Diagram
![image](https://github.com/Amnis333/BoardGameStudio/assets/83019007/3bad1098-bd9c-4057-9e33-640a32ff900f)


