FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV MAIL_USERNAME=sumonpaul267@gmail.com
ENV MAIL_PASSWORD=Sumon#@9519#@
EXPOSE 5000
CMD ["python", "app.py"]
