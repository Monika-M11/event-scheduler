# Event Scheduling & Resource Allocation System

A Flask-based web application for scheduling events and allocating shared resources with real-time conflict prevention.

## Features
- Add/Edit/Delete Events and Resources
- Allocate multiple resources to events
- **Conflict detection and prevention** during allocation (immediate error feedback)
- Resource Utilisation Report with total hours and upcoming bookings
- Dark black & white theme (report in white cards for readability)

## Demo Video (Mandatory)
[Click to watch the demo video](https://raw.githubusercontent.com/Monika-M11/event-scheduler/main/Demo/Demo_video.mp4)

## Screenshots

### Events List
![Events List](https://raw.githubusercontent.com/Monika-M11/event-scheduler/main/screenshots/page1.png)

### Add Event / Resources
![Add Event](https://raw.githubusercontent.com/Monika-M11/event-scheduler/main/screenshots/page2.png)

### Allocation Page
![Allocation](https://raw.githubusercontent.com/Monika-M11/event-scheduler/main/screenshots/page3.png)

### Conflict Error or Report
![Report / Conflict](https://raw.githubusercontent.com/Monika-M11/event-scheduler/main/screenshots/page4.png)

## How to Run
```bash
pip install flask flask-sqlalchemy
python app.py
