# amplify-review-environment-cleaner
amplifyのPRレビュー機能によって作成された環境のゴミを削除するLambda関数


## Prerequisuites

* [Docker](https://docs.docker.com/install/)
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Python 3.8


## Deletion Policy

* Lambdaがデプロイされたリージョンと同一リージョンのamplifyアプリを対象とする
* amplifyで作成されたPR環境のみを対象とする
* 削除失敗状態のまま放置されているcfnを対象とする
* S3にcfnテンプレートファイルが存在するがcfnテンプレート自体は削除済みのものを対象とする
* `production`ブランチは削除対象外
* 1日に1回だけ実行する（時間指定なし）

## regionの指定
環境変数 `AWS_DEFAULT_REGION`にリージョン名を指定してください。  
ローカルで実行する場合に `AWS_DEFAULT_REGION`の指定がないと失敗します。


## Usage
### Build

`sam build`

### Run(local)

`sam local invoke`

### How to deploy

`sam deploy`
