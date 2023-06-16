# IllustShop-backend
為IllustShop網站的後端系統，提供Restful API供前端存取。  
## Swagger API文件：https://illustshop-backend.onrender.com/swagger/
API包含以下功能：  
* 會員系統
* 購物車系統
* 商品上架/下架功能 (管理員限定)

## Quick Start
IllustShop-backend為利用Django開發的系統，可透過以下指令於本地端啟動程式：  
1. 執行`pip install -r requirements.txt` ，安裝必要Python套件
2. 執行`python manage.py makemigrations`及`python manage.py migrate`，將models.py的類別遷移至資料庫
3. 執行`python manage.py runserver`啟動服務