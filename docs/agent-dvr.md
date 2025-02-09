# DVR server with HA integration

Allows to add camera view to HA that can't be watched through other integration

You need to deploy docker container in your local network (on the HA machine for example)

[Docker run command](https://www.ispyconnect.com/download.aspx/)

```bash
docker run -d --name=AgentDVR -e PUID=1000 -e PGID=1000 -e TZ=America/New_York -e AGENTDVR_WEBUI_PORT=8090 -p 8090:8090 -p 3478:3478/udp -p 50000-50100:50000-50100/udp -v /appdata/AgentDVR/config/:/AgentDVR/Media/XML/ -v /appdata/AgentDVR/media/:/AgentDVR/Media/WebServerRoot/Media/ -v /appdata/AgentDVR/commands:/AgentDVR/Commands/ --restart unless-stopped mekayelanik/ispyagentdvr:latest
```

[Home Assistant Doc](https://www.home-assistant.io/integrations/agent_dvr/)