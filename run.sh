#!/usr/bin/env bash
docker run \
  --env-file ./.env \
  -v /Users/Xander/python/namecheap-updater/domains.txt:/usr/src/app/domains.txt \
  -v /Users/Xander/python/namecheap-updater/logs:/usr/src/app/logs \
  jakks/namecheapupdater "$@"
