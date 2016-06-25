FROM logstash

COPY logstash.conf /etc/logstash/conf.d/logstash.conf

EXPOSE 5000

# Install logstash plugins here, eg:
# RUN logstash-plugin install logstash-filter-json

CMD ["logstash", "-f", "/etc/logstash/conf.d/logstash.conf"]
