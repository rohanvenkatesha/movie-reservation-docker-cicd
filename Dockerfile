FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install netcat + dos2unix
RUN apt-get update && apt-get install -y netcat-openbsd dos2unix

# Convert script to Unix format and make executable
RUN dos2unix wait-for-mysql.sh && chmod +x wait-for-mysql.sh

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["./wait-for-mysql.sh"]
