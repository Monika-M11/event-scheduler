# Event Scheduling & Resource Allocation System

A Flask-based web application for scheduling events and allocating shared resources with real-time conflict prevention.

## Features
- Add/Edit/Delete Events and Resources
- Allocate multiple resources to events
- **Conflict detection and prevention** during allocation (immediate error feedback)
- Resource Utilisation Report with total hours and upcoming bookings
- Dark black & white theme (report in white cards for readability)

## Demo Video 
 
[Click here to watch demo video](Events%20-%2015%20December%202025.mp4)

*(Directly playable in GitHub — no YouTube needed since file is small enough)*

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