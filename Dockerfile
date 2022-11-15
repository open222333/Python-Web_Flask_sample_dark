FROM python:3.9.15-buster

# set environment variables
# https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation
ENV PYTHONDONTWRITEBYTECODE 1

# 對於3.7以上版本：標準輸出stdout和標準錯誤stderr全部採用unbuffered 在 3.7 版更改: stdout 和 stderr 流的文本層現在是無緩衝的。
# ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY . .


# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
