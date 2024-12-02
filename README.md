# SnmpPyLite

**SnmpPyLite** — is a lightweight client for working with the SNMP protocol in Python, supporting the operations `GET`, `GET-NEXT`, `GET-BULK`, `GET-WALK` и `SET`.

## 📦 Installation

Using `pip`:
```bash
pip install snmp_py_lite
```

Or cloning from the repository:
```bash
git clone https://github.com/katzeNilpferd/SnmpPyLite.git
cd SnmpPyLite
python setup.py install
```

## 🚀 Usage

Example of use for performing the `GET` operation:
```bash
from snmp_py_lite.client import SNMPClient

client = SNMPClient(ip="192.168.126.10", community="public", version='1')
response = client.get("1.3.6.1.2.1.1.1.0")
print(response)
```

Example of the `SET` operation:
```bash
value = "New Device Name"
client.set("1.3.6.1.2.1.1.5.0", value, "STRING")
```

## 🌐 Supported versions of the SNMP

- `1` — initial version of the protocol.
- `2c` — includes improvements in performance, security, privacy and communication between managers compared to the previous version.

## 📚 Supported operations

- `GET` — getting the value by OID.
- `GET-NEXT` — getting the next value by OID.
- `GET-BULK` — mass receipt of values (SNMPv2c).
- `GET-WALK` — recursively retrieving values in the table (iterating over the OID).
- `SET` — changing the value by OID.

## 🛠️ Supported data types

- `INTEGER`
- `OCTET STRING`
- `NULL`
- `OID`
- `Ip Address`
- `Counter`
- `Gauge`
- `TimeTicks`

## 📝 License

This project is licensed under the MIT license. For details, see the LICENSE file.

## 🤝 Contribution

Your contribution is welcome! If you want to improve the project, create a fork, make changes and send a Pull Request.

    1. Make a fork of the repository
    2. Create a new branch (`git checkout -b feature/your_feature`)
    3. Commit the changes (`git commit -m "Added a new feature"`)
    4. Start the branch (`git push origin feature/your_feature`)
    5. Open the Pull Request

## 📞 Contacts

- Email: evgeny.ockatiev@gmail.com
