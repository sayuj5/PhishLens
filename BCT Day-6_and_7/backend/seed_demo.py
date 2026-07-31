import sys
import os

# Add the parent directory to sys.path so we can import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine
from backend import models, auth
import random
from datetime import datetime, timedelta, timezone

def seed_data():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Create Admin User
    existing_user = db.query(models.User).filter(models.User.email == "admin@blackfalcon.local").first()
    if not existing_user:
        user = models.User(
            email="admin@blackfalcon.local",
            hashed_password=auth.get_password_hash("Admin123!"),
            role="admin"
        )
        db.add(user)
        print("Created admin user: admin@blackfalcon.local / Admin123!")

    # 2. Create Networks
    if db.query(models.Network).count() == 0:
        net1 = models.Network(cidr="192.168.1.0/24", name="Corporate LAN", description="Primary office network")
        net2 = models.Network(cidr="10.0.0.0/16", name="Data Centre", description="Production servers")
        net3 = models.Network(cidr="172.16.0.0/20", name="DMZ", description="Public-facing services")
        db.add_all([net1, net2, net3])
        db.commit()
        print("Created demo networks.")
    
    # 3. Create Assets & Services
    networks = db.query(models.Network).all()
    if db.query(models.Asset).count() == 0 and networks:
        now = datetime.now(timezone.utc)
        assets = []
        for i in range(1, 41):
            net = random.choice(networks)
            ip_base = net.cidr.split('/')[0].rsplit('.', 1)[0]
            ip = f"{ip_base}.{random.randint(2, 250)}"
            
            os_type = random.choice(["Windows Server 2019", "Windows 10", "Ubuntu 22.04", "CentOS 8", "Debian 11", "Cisco IOS", "VMware ESXi"])
            
            asset = models.Asset(
                ip_address=ip,
                hostname=f"host-{i}.local",
                os=os_type,
                network_id=net.id,
                is_active=random.random() > 0.1,
                first_seen=now - timedelta(days=random.randint(1, 30)),
                last_seen=now - timedelta(hours=random.randint(1, 48)),
                risk_score=random.uniform(0, 85)
            )
            assets.append(asset)
        db.add_all(assets)
        db.commit()
        print(f"Created {len(assets)} demo assets.")

        # Add Ports and Services
        all_assets = db.query(models.Asset).all()
        common_ports = [
            (22, "tcp", "ssh", "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5"),
            (80, "tcp", "http", "Apache/2.4.41 (Ubuntu)"),
            (443, "tcp", "https", None),
            (3389, "tcp", "rdp", None),
            (21, "tcp", "ftp", "vsFTPd 3.0.3"),
            (445, "tcp", "smb", None),
            (23, "tcp", "telnet", None),
        ]
        
        for asset in all_assets:
            num_ports = random.randint(1, 5)
            selected_ports = random.sample(common_ports, num_ports)
            for p, proto, svc_name, banner in selected_ports:
                port = models.Port(
                    asset_id=asset.id,
                    port_number=p,
                    protocol=proto,
                    state="open"
                )
                db.add(port)
                db.commit()
                db.refresh(port)
                
                svc = models.Service(
                    port_id=port.id,
                    service_name=svc_name,
                    banner=banner
                )
                db.add(svc)
            db.commit()
        print("Populated open ports and services.")

    # 4. Create Findings
    if db.query(models.Finding).count() == 0:
        all_assets = db.query(models.Asset).all()
        findings = []
        for _ in range(50):
            asset = random.choice(all_assets)
            sev = random.choice(["critical", "high", "medium", "low"])
            status = random.choice(["open", "open", "open", "acknowledged", "resolved"])
            
            titles = {
                "critical": ["Unauthenticated RDP Exposed", "Default Credentials on Web Admin", "Cleartext Telnet Service"],
                "high": ["Outdated OpenSSH Version", "FTP Allows Anonymous Login", "Unencrypted HTTP Access"],
                "medium": ["Missing Security Headers", "Self-Signed TLS Certificate"],
                "low": ["ICMP Timestamp Response", "Verbose Banner Disclosure"]
            }
            
            finding = models.Finding(
                asset_id=asset.id,
                plugin_id="demo_plugin",
                title=random.choice(titles[sev]),
                description="This is a demonstration finding seeded for portfolio review purposes.",
                severity=sev,
                status=status,
                category=random.choice(["port", "service", "banner", "config"]),
                risk_score=random.uniform(10, 95),
            )
            findings.append(finding)
        db.add_all(findings)
        db.commit()
        print(f"Created {len(findings)} demo findings.")

    db.close()
    print("Demo data seeding complete.")

if __name__ == "__main__":
    seed_data()
