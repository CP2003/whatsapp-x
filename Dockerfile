FROM python:3.8 AS clone
RUN git clone https://github.com/CP2003/whatsapp-x.git /root/PAMOD/
FROM python:3.8
ENV PYTHONUNBUFFERED 1
COPY --from=clone /root/PAMOD /root/PAMOD
WORKDIR /root/PAMOD
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["bash", "start.sh"]

