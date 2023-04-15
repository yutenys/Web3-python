**********************使用说明**********************
python3.9环境
1.安装依赖库：pip install -r requirements.txt
2.直接在main.py中执行
3.config.ini文件：
WalletPath：创建钱包的文件存放地址，默认是在data文件下，例如，data/Wallets.csv
EN_WalletPath：加密后钱包的文件存放地址，默认是在data文件下，例如，data/EN_Wallets.csv
DE_WalletPath：解密后钱包的文件存放地址，默认是在data文件下，例如，data/DE_Wallets.csv
IV：加密/解密向量，可以删除，但是一定要保证同一个加密和解密的向量一致，296709cf6f3ed0e179d4a9d1728409bb
4.加密/解密密码要一致，一定要为16位或者16的倍数位
5.account.csv
.必填字段为account,amount，选填为rand(随机金额，格式为xx/xx),add(随机小金额，格式为xx/xx)
.add存在时转账金额为amount+add(随机数)；rand存在时转账金额为rand(随机数))；add,rand都不存在时转账金额为固定的amount，优先级为add > rand > amount
6.API_KEY：api_key
7.IP：api关联的ip，可以去api里面编辑修改
8.SECRET_KEY：api_secret
9.PASSPHRASE：api_password
10.COIN:提取的币种
11.FEE:手续费，去okx上提币页面查看
12.CHAIN:提币的目的链
13.常用chain：
*******ETH*******
ETH-ERC20
ETHK-OKC
ETH-Arbitrum one
ETH-zkSync Lite
ETH-Optimism
*******USDT*******
USDT-ERC20
USDT-OKC
USDT-Arbitrum one
USDT-TRC20
USDT-Optimism
USDT-Ploygon
USDTAvalanche C-Chain
14.指令说明
**********指令说明**********
*输入'1'批量创建钱包
*输入'2'批量加密钱包
*输入'3'批量解密钱包
*输入'4'加密配置文件
*输入'5'解密配置文件
*输入'6'okx批量提现
*输入'7'查询okx余额
*输入'0'或者'h'或者'help'唤出功能说明
***************************