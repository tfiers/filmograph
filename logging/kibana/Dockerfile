FROM kibana
ENV ELASTICSEARCH_URL http://es-log:9200
# Execute as Kibana user, see here:
# https://github.com/docker-library/kibana/issues/20
RUN gosu kibana kibana plugin --install elastic/sense
