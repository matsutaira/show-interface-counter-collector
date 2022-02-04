# show interface counter collector

## 目的
- ```show interfaces``` コマンドを大量に取得したログから特定のカウンター値を取得したい
- 取得した値は編集しやすいように CSV へ出力させたい

## 実行コマンド
```python show_interface_counter_collector.py [ログファイル名] [オプション: 任意の IF 名]```

### 実行内容
- 実行コマンドのオプションが無い場合、ログファイルの中にある最初と最後の ```show interfaces``` から **[counter_checker]** で検索した値を比較して変化のあるインターフェースを選出
- 実行コマンドのオプションがある場合、任意のインターフェースを選出
- 選出したインターフェースのログから **[counter]** で検索したカウンター値を取得
- ```show interfaces``` に記載の時刻と取得したカウンター値をインターフェース毎に CSV として出力
- 実行コマンドのオプションを含む各インターフェースは **[if_checker]** にマッチしたもののみ利用

## ツール
- show_interface_counter_collector.py

## 設定ファイル
- show_interface_counter_collector.ini

### 設定内容
- **[counter_checker]** は実行コマンドのオプションを使わなかったときに ```show interfaces``` の最初と最後のカウンター値を比較する対象を探すための正規表現
- **[if_checker]** は各インターフェースが想定の名称か確認するための正規表現
- **[counter]** は取得したい任意のカウンター値を検索するための正規表現
- **[counter_checker]** と **[if_checker]** は ```pattern = [正規表現]``` で書くこと、単独記載のみ
- **[counter]** は ```[値の名称] = [正規表現]``` で書くこと、複数記載可能
