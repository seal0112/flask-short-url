# Short Url

## Crawler and Back-End for Taiwan stocks
使用flask以及sqlite製作的短網址服務

## Prerequisites

請事先安裝好python3以及SQL database
- [python3](https://www.python.org/downloads/)
- [SQLite)]()

## Installation
```shell
$ git https://github.com/seal0112/flask-short-url
$ cd flask-short-url/
```

#### 安裝virtual environment
```shell
$ pip install virtualenv
```

#### 建立虛擬環境
```shell
$ virtualenv venv
```

#### 啟動虛擬環境
在 Windows 系統中，使用：
```shell
venv\Scripts\activate.bat
```
在 Unix 或 MacOS 系統，使用：
```shell
$ source venv/bin/activate
```

#### 安裝需要的module
```shell
$ pip install -r requirements.txt
```

#### 初始化migrate
````shell
$ flask db init
$ flask db migrate -m "commit message"
$ flask db upgrade
````

#### 啟動
```shell
$ gunicorn wsgi:app
$ gunicorn --bind=0.0.0.0:5000 wsgi:app # 指定host以及port
```

#### 測試用的啟動, 程式更動時會重啟
```shell
$ gunicorn --reload wsgi:app
```

## API
**Show all short Url**
----
  Returns array of json data about all short url.

* **URL**

  /created-url

* **Method:**

  `GET`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[
        {"alias": "http://0.0.0.0:5000/1234567", "origin": "https://www.gmail.com/"},
        {"alias": "http://0.0.0.0:5000/BFffktj", "origin": "https://www.gmail.com"}
    ]`


**create new short Url**
----
  create new short url.

* **URL**

  /created-url

* **Method:**

  `POST`

* **Data Params**

  `{ 'origin: 'http://google.com'} or { 'origin: 'http://google.com', 'alias': '1234567'}`

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{"alias": "http://0.0.0.0:5000/1234567", "origin": "https://www.gmail.com/"}`

* **Error Response:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "alias collision" }`


**redirect to origin Url**
----
  redirect browser to origin url.

* **URL**

  /<token>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `token=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 302 <br />
    **Content:** None

* **Error Response:**

  * **Code:** 404 Not Found <br />
    **Content:** `{ error : "Couldn't find long url for <token>" }`


**get top three visited url**
----
  redirect browser to origin url.

* **URL**

  /top-three-visited

* **Method:**

  `GET`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[
        {
            "alias": "http://0.0.0.0:5000/1234567",
            "count": 2,
            "origin": "https://www.gmail.com/"
        },
        {
            "alias": "http://0.0.0.0:5000/9dRreG0",
            "count": 13,
            "origin": "https://tw.yahoo.com/"
        },
        {
            "alias": "http://0.0.0.0:5000/o5HDQR",
            "count": 16,
            "origin": "https://www.google.com"
        }
    ]`

**get short url total hit count**
----
  Return <token>'s hit count.

* **URL**

  /hit-count/<token>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `token=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
        "alias": "http://0.0.0.0:5000/9dRreG0",
        "count": 13,
        "origin": "https://tw.yahoo.com/"
    }`

* **Error Response:**

  * **Code:** 404 Not Found <br />
    **Content:** `{ error : "Couldn't find hit count record for <token>" }`


**get short url total hit count**
----
  Return short url hit count record, group by date, of all time.

* **URL**

  /hit-count-group-by-date

* **Method:**

  `GET`

*  **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[
      {
        "Date": "2020-01-01",
        "Values": [
          {
            "alias": "https://url-shortener.com/<token-1>",
            "origin": "https://www.google.com.tw?region=zh_tw#/firstpage",
            "count": 1
          }
        ]
      },
      {
        "Date": "2020-01-02",
        "Values": [
          {
            "alias": "https://url-shortener.com/<token-1>",
            "origin": "https://www.google.com.tw?region=zh_tw#/firstpage",
            "count": 2
          },
          {
            "alias": "https://url-shortener.com/<token-2>",
            "origin": "https://www.facebook.com.tw",
            "count": 2
          }
        ]
      }
    ]`

## License
MIT