# Deployment

Prosjektet deployes på en virtuell maskin (VM) som fungerer som en lokal server.

VM-en opprettes i Oracle VirtualBox og kjører lokalt på en Windows-PC.
Virtualisering brukes for å simulere et separat servermiljø (Ubuntu Server)
uavhengig av vertsoperativsystemet.

---

## Oversikt

Applikasjonen kjører i Docker-containere på en Ubuntu Server VM.

Arkitektur:

VM (Ubuntu Server)
→ Docker
→ web (Flask backend)
→ db (MariaDB database)

Containerne kommuniserer via Docker network.

---

## Virtuell maskin

Anbefalte VM-spesifikasjoner:

| Ressurs | Verdi |
|---|---|
| Operativsystem | Ubuntu Server 22.04 LTS |
| CPU | 2 cores |
| RAM | 2 GB |
| Disk | 20 GB |
| Nettverk | Bridged Adapter |

Bridged nettverk gir VM-en egen IP-adresse på lokalnettet.

---

## Klargjøring av server (Ubuntu VM)

Oppdater systemet:

```bash
sudo apt update && sudo apt upgrade -y
