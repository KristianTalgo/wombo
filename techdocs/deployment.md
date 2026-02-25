# Deployment

Prosjektet deployes på en virtuell maskin (VM) som fungerer som en lokal server.

VM-en opprettes i Proxmox, som kjører på skolens serverinfrastruktur.
Proxmox brukes kun til virtualisering, mens VM-en er miljøet hvor
applikasjonen installeres og kjøres.

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

VM opprettes i Proxmox med følgende spesifikasjoner:

| Ressurs | Verdi |
|---|---|
| Operativsystem | Ubuntu Server 22.04 LTS |
| CPU | 2 cores |
| RAM | 2 GB |
| Disk | 20 GB |
| Nettverk | vmbr0 (bridged) |

VM-en bruker maskinressurser fra skolens server, men fungerer som
prosjektets lokale server.

---

## Klargjøring av server

Oppdater systemet:

```bash
sudo apt update && sudo apt upgrade -y
