import os

def scan(target):
    # Run Nmap scan to get open ports
    nmap_command = f"nmap -p- -T4 -oN nmap_scan.txt {target}"
    os.system(nmap_command)

    # Parse Nmap output to get list of open ports
    with open("nmap_scan.txt") as f:
        lines = f.readlines()

    open_ports = []
    for line in lines:
        if "tcp" in line and "open" in line:
            port = line.split("/")[0]
            open_ports.append(port)

    # Run NSE scripts to check for vulnerabilities on open ports
    for port in open_ports:
        nse_command = f"nmap -sV -sC -p {port} -oN nse_scan.txt {target}"
        os.system(nse_command)

    # Parse NSE output to get list of vulnerabilities
    with open("nse_scan.txt") as f:
        lines = f.readlines()

    vulnerabilities = []
    for line in lines:
        if "VULNERABILITY" in line:
            vulnerability = line.strip()
            vulnerabilities.append(vulnerability)

    # Print results
    print(f"Open ports: {open_ports}")
    if vulnerabilities:
        print("Vulnerabilities found:")
        for vulnerability in vulnerabilities:
            print(vulnerability)
    else:
        print("No vulnerabilities found.")

if __name__ == "__main__":
    target = input("Enter an IP address or website to scan: ")
    scan(target)
