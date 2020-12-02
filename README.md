Simple Flask application with Vue.js kanban board
=================================================

This is monorepo application containing FE (frontend) and BE (backend) parts together with a development environment (Vagrant). Running development ENV of this application is as easy as using Makefile, please try run make in root directory of that repo to see more help.

Run the application (devel)
---------------------------

```bash
make run-dev    # install dependencies, build FE etc...
```

If you run the application first time, please run this commands before:
```bash
make db-init    # initialize new empty database and provides admin's password to you
```

Start in GCP
============
```bash
make gcp
```

Run instance
------------
```bash
# Start instance with access to apis
gcloud beta compute --project=pirple-lab instances create flask-pirple --zone=us-central1-a --machine-type=g1-small --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=742638129389-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/sqlservice.admin,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/devstorage.read_only --tags=http-server,https-server --image=debian-10-buster-v20201014 --image-project=debian-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-1 --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any

# Allow ingress HTTP and HTTPS
gcloud compute --project=pirple-lab firewall-rules create default-allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server

gcloud compute --project=pirple-lab firewall-rules create default-allow-https --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:443 --source-ranges=0.0.0.0/0 --target-tags=https-server

```
