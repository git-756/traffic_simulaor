# 交通信号シミュレーター (Traffic Signal Simulator)

https://samurai-human-go.com/gif/py_simu_traffic.gif

## 概要

このプロジェクトは、PythonとPySide6を使用して構築された交通信号シミュレーターです。
基本的なシーケンス制御（定周期制御）による交差点の交通流を視覚化し、将来的には交通量に応じた信号制御の最適化アルゴリズムを研究・実装することを目的としています。

## 主な機能

* **GUIによる可視化**: PySide6を用いたグラフィカルな画面で、車両や信号の動きをリアルタイムに確認できます。
* **現実的な車両挙動**: 車両は信号を遵守し、先行車との安全な車間距離を保って停止します。
* **基本的な信号サイクル**: 現実の信号機に近い、青・黄・赤のサイクルを再現しています。
* **4方向からの車両生成**: 交差点の上下左右からランダムに車両が生成されます。

## 動作環境

* Python 3.8 以上
* PySide6

## インストールと実行方法

1.  **リポジトリをクローン**
    ```bash
    git clone [https://github.com/](https://github.com/)[あなたのユーザー名]/[リポジトリ名].git
    cd [リポジトリ名]
    ```

2.  **仮想環境の作成と有効化**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *Windowsの場合は `venv\Scripts\activate`*

3.  **必要なライブラリをインストール**
    ```bash
    pip install PySide6
    ```
    *（もし`requirements.txt`を作成した場合は `pip install -r requirements.txt`）*

4.  **シミュレーターの実行**
    ```bash
    python3 src/traffic_simulator/main.py
    ```
    *（ご自身のプロジェクトのパス構成に合わせてください）*

## 使い方

アプリケーションが起動したら、「シミュレーション開始」ボタンをクリックしてください。シミュレーションが開始されます。もう一度クリックすると一時停止します。

## 今後の展望

* 右左折する車両の実装
* 交通量に応じて信号が変化する「交通感応式制御」の実装
* 強化学習を用いた信号サイクルの最適化

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 作者

Samurai-Human-Go
https://samurai-human-go.com/