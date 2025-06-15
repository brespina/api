## populate db

```sh
mysql -u your_user -p your_db < app/seed.sql
```

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

checkout `http://127.0.0.1:8000/docs` with dbeaver or mysql terminal open and see if crud operations work

todo:
need to hook up front end admin with api, also audit existing website
