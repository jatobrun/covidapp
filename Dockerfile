FROM python:3.6-slim-stretch

RUN apt update && \
    apt install -y python3-dev gcc

WORKDIR /app
COPY . /app 
# Install pytorch cpu version
RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip install pymongo[srv]
RUN pip install pillow
RUN pip install -r requirements.txt
#pip install --no-cache-dir -r
RUN pip install torchvision==0.1.8
RUN pip install Flask-Bcrypt
RUN pip install requests
