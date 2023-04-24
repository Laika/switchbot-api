# SwitchBot API

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

## Demo

[![demo](https://asciinema.org/a/Uo6FmVP2etW5AvrxxJMdmTkWO.svg)](https://asciinema.org/a/Uo6FmVP2etW5AvrxxJMdmTkWO?autoplay=1)
