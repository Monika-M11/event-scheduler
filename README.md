# Event Scheduling & Resource Allocation System

A Flask-based web application for scheduling events and allocating shared resources with real-time conflict prevention.

## Features
- Add/Edit/Delete Events and Resources
- Allocate multiple resources to events
- **Conflict detection and prevention** during allocation (immediate error feedback)
- Resource Utilisation Report with total hours and upcoming bookings
- Dark black & white theme (report in white cards for readability)

## Demo Video (Mandatory)

[![Click to watch the screen-recorded demo video](page1.png)](https://raw.githubusercontent.com/Monika-M11/event-scheduler/main/demo-video.mp4)
## Screenshots

### Page 1
![Page 1](page1.png)

### Page 2
![Page 2](page2.png)

### Page 3
![Page 3](page3.png)

### Page 4
![Page 4](page4.png)

*(Add more if you have extra screenshots)*

## How to Run
```bash
pip install flask flask-sqlalchemy
python app.py