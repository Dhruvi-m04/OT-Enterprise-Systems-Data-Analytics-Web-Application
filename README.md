# OT-Enterprise-Systems-Data-Analytics-Web-Application

# Equipment Inventory Tracking System

An equipment inventory management system developed for **TechInnovators Inc.** to centralise equipment tracking, streamline check-in/check-out processes, and provide insights into equipment usage.

The system integrates an **Oracle APEX web application** with a **Python/Tkinter desktop application** through REST APIs. Employees can use QR codes to identify themselves when borrowing or returning equipment, while administrators manage inventory, bookings, and reports through Oracle APEX.

## 🚀 Features

* 📦 Equipment inventory management
* 🔄 Equipment check-in and check-out
* 📷 QR-code employee verification using OpenCV
* 👤 Employee equipment usage history
* 🔗 REST API integration between Python and Oracle APEX
* 📊 Interactive inventory dashboards and reports
* 📈 Equipment usage and resource analytics
* 🔐 Role-based access for administrators and employees

## 🏗️ System Architecture

```text
Employee
   │
   ▼
Python / Tkinter Application
   │
   │ REST API
   ▼
Oracle APEX / ORDS
   │
   ▼
Oracle Database
   │
   ├── Employees
   ├── Inventory
   └── Bookings
```

### Main Components

**Oracle APEX**

* Inventory management
* Booking and allocation management
* Reports and dashboards
* Equipment activity monitoring

**Python Application**

* Employee interface
* Equipment checkout and return
* QR-code scanning
* API communication

**Oracle Database**

* Employee records
* Equipment inventory
* Booking and return records

## 🛠️ Technology Stack

| Technology      | Purpose              |
| --------------- | -------------------- |
| Oracle APEX     | Inventory management |
| Oracle Database | Data storage         |
| ORDS            | REST API integration |
| Python          | Employee application |
| Tkinter         | Desktop GUI          |
| OpenCV          | QR-code scanning     |
| Requests        | API communication    |
| SQL             | Database management  |

## 🔄 How It Works

### Checkout

1. Employee opens the Python application.
2. Employee ID is entered or identified using a QR code.
3. Available equipment is selected.
4. A REST API request creates the booking.
5. Inventory availability is automatically updated.

### Return

1. Employee scans their QR code.
2. Employee enters the Booking ID.
3. The booking is validated.
4. The equipment is marked as returned.
5. Inventory availability is restored.

## 📊 Management Insights

The Oracle APEX application provides dashboards and reports covering:

* Inventory levels
* Active and returned equipment
* Most frequently booked equipment
* Employee equipment usage
* Equipment turnaround time
* Inventory turnover
* Equipment return trends

## ⚙️ Setup

### Requirements

* Python 3.9+
* Oracle Database
* Oracle APEX
* Oracle REST Data Services (ORDS)
* Webcam for QR-code scanning

### Python Installation

```bash
git clone https://github.com/<your-username>/equipment-inventory-tracking-system.git
cd equipment-inventory-tracking-system

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Configure the API endpoints and database environment before running the application.

## 📁 Project Structure

```text
equipment-inventory-tracking-system/
│
├── python/
├── apex/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## 📚 Documentation

Detailed documentation covering the **system architecture, database design, API endpoints, installation, user manuals, administration, reporting, security, and maintenance** is available in the `docs/` directory.

## 🔮 Future Enhancements

* Automated maintenance scheduling
* Equipment reservation functionality
* Automated overdue notifications
* Mobile application support
* Advanced analytics
* Predictive equipment maintenance

## 👩‍💻 Project

**TechInnovators Inc. – Equipment Inventory Tracking System**

Built using **Oracle APEX, Oracle Database, ORDS, Python, Tkinter, OpenCV, and REST APIs**.
