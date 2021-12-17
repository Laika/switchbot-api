# SwitchBot thermometer API

## Configure
Change `MAC_ADDR` to your thermometer's MAC address in docker-compose.yaml
```yaml
services:
  sensor:
    environment:
      - MAC_ADDR=XX:XX:XX:XX:XX:XX
```

## Run
```bash
docker compose up -d
```
