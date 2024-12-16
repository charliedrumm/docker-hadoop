FROM apache/hadoop:3.4.0

RUN mkdir -p /opt/hadoop/dfsdata/namenode
RUN mkdir -p /opt/hadoop/tmpdata/dfs/name/

COPY ./entrypoint.sh /opt/hadoop/entrypoint.sh
RUN sudo chmod +x /opt/hadoop/entrypoint.sh

EXPOSE 9870

ENTRYPOINT ["sh", "-c", "/opt/hadoop/entrypoint.sh"]