# Smart Gate System

A professional RFID/UHF-based gated community access control system built with Django REST Framework and MySQL.  
The system automates vehicle access verification, payment validation, and smart barrier gate control for residential communities using local-network hardware integration.

Designed for real-world village deployment, the platform enforces monthly community payment compliance before granting gate access.

---

# Overview

The system uses UHF RFID stickers attached to vehicles.  
When a vehicle approaches the gate, a UHF reader scans the sticker and sends the request to the backend server.

The backend performs multiple validation checks including:

- Card activity status
- Customer status
- Card type verification
- Monthly payment validation
- Door-reader relationship validation

If validation succeeds, the backend sends an `OPEN` command to the access controller, which triggers the smart barrier gate.

---

# Core Features

- RFID/UHF-based vehicle authentication
- Smart barrier gate integration
- Real-time access verification
- Monthly payment enforcement
- Master and member card management
- Local network access controller communication
- Automated access logging
- Attendance monitoring
- REST API architecture
- Role-based access control
- Modular Django application structure
- Ethiopian calendar payment logic
- Leap year and Pagume handling
- Community resident management
- Gate and reader management
- Payment tracking system

---

# System Workflow

```text
Vehicle Arrives
       ↓
UHF Reader Scans RFID Sticker
       ↓
Reader Sends Request to Backend API
       ↓
Backend Validates:
    - Card Exists
    - Card Active
    - Customer Active
    - Card Type
    - Payment Status
       ↓
If Approved:
Backend Sends OPEN Command
       ↓
Access Controller Opens Barrier Gate
