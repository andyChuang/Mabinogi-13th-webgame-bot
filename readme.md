# Mabinogi-13th-webgame-bot

瑪奇十三週年農場物語(https://event.beanfun.com/mabinogi/E20180517/index.aspx)

又來啦今年的網頁週年慶活動

目前功能會連續幫你登入所有帳號以及依序執行以下：
1. 登入
2. 培養盆栽
3. 分享FB (TODO)

雞蛋找找樂太賭了不玩所以不寫

## Quick Start
0. 首先你要有裝python
1. Clone this repository to wherever you want
2. `cd Mabinogi-13th-webgame-bot`
2. `pip install -r requirement.txt`
3. 同目錄下建立`account.json`，格式如下：
```
[
{
"account": "帳號1",
"password": "密碼1",
"game_account": "遊戲帳號1"
},
{
"account": "帳號2",
"password": "密碼2",
"game_account": "遊戲帳號2"
},
.
.
.
{
"account": "帳號N",
"password": "密碼N",
"game_account": "遊戲帳號N"
}
]
```
5. python play.py

## To-do
1. FB分享活動



