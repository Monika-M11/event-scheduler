# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import os




# app = Flask(__name__, template_folder='../UI')
# app.config['SECRET_KEY'] = 'test'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)


# # MODELS
# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200))
#     start = db.Column(db.DateTime)
#     end = db.Column(db.DateTime)


# class Resource(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200))
#     type = db.Column(db.String(100))

# class Allocation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#     resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
#     event = db.relationship('Event')
#     resource = db.relationship('Resource')


# # SIMPLE OVERLAP CHECK
# def overlaps(s1, e1, s2, e2):
#     return not (e1 <= s2 or s1 >= e2)


# with app.app_context():
#     db.create_all()

# # HOME → EVENTS
# @app.route('/')
# def home():
#     return redirect('/events')


# # EVENTS
# @app.route('/events')
# def events():
#     return render_template('events.html', events=Event.query.all())


# @app.route('/events/new', methods=['GET','POST'])
# def event_new():
#     if request.method == 'POST':
#         title = request.form['title']
#         start = datetime.fromisoformat(request.form['start'])
#         end = datetime.fromisoformat(request.form['end'])



#         if end <= start:
#             flash('End time must be after start time')
#             return redirect('/events/new')


#         e = Event(title=title, start=start, end=end)
#         db.session.add(e)
#         db.session.commit()
#         return redirect('/events')


#     return render_template('event_form.html')

# # RESOURCES
# @app.route('/resources')
# def resources():
#     return render_template('resources.html', resources=Resource.query.all())


# @app.route('/resources/new', methods=['GET','POST'])
# def resource_new():
#     if request.method == 'POST':
#         r = Resource(name=request.form['name'], type=request.form['type'])
#         db.session.add(r)
#         db.session.commit()
#         return redirect('/resources')
#     return render_template('resource_form.html')

# # ALLOCATIONS
# @app.route('/allocations')
# def allocations():
#     allocs = Allocation.query.all()
#     return render_template('allocations.html', allocs=allocs)


# @app.route('/allocations/new', methods=['GET','POST'])
# def allocation_new():
#     events = Event.query.all()
#     resources = Resource.query.all()


#     if request.method == 'POST':
#         event_id = int(request.form['event_id'])
#         res_id = int(request.form['resource_id'])


#         ev = Event.query.get(event_id)

#         # conflict check
#         for a in Allocation.query.filter_by(resource_id=res_id).all():
#             if overlaps(ev.start, ev.end, a.event.start, a.event.end):
#                 flash('Conflict detected — resource already booked')
#                 return redirect('/allocations/new')


#         alloc = Allocation(event_id=event_id, resource_id=res_id)
#         db.session.add(alloc)
#         db.session.commit()
#         return redirect('/allocations')


#     return render_template('allocate_form.html', events=events, resources=resources)




# if __name__ == '__main__':
#      app.run(debug=True)



# app.py - Main Flask Application

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------- Models --------------------------

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # room, instructor, equipment, etc.

    allocations = db.relationship('EventResourceAllocation', backref='resource', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Resource {self.name}>"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    allocations = db.relationship('EventResourceAllocation', backref='event', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Event {self.title}>"

class EventResourceAllocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)

# -------------------------- Helper Functions --------------------------

def check_conflicts(event_id_to_ignore, resource_id, new_start, new_end):
    """
    Check if the given time range conflicts with any existing allocation for the resource.
    Ignores the event with event_id_to_ignore (useful when editing).
    """
    conflicting = db.session.query(EventResourceAllocation).join(Event).filter(
        EventResourceAllocation.resource_id == resource_id,
        Event.id != event_id_to_ignore,
        db.or_(
            db.and_(Event.start_time < new_end, Event.end_time > new_start)  # overlap
        )
    ).first()
    return conflicting is not None

# -------------------------- Routes --------------------------

@app.route('/')
def index():
    return redirect(url_for('events'))

# Header navigation will be included in base.html

@app.route('/events')
def events():
    all_events = Event.query.order_by(Event.start_time).all()
    return render_template('events.html', events=all_events)

@app.route('/event/new', methods=['GET', 'POST'])
@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def event_form(event_id=None):
    event = Event.query.get_or_404(event_id) if event_id else None

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

        if start_time >= end_time:
            flash('End time must be after start time.', 'danger')
            return render_template('event_form.html', event=event)

        if event:
            event.title = title
            event.description = description
            event.start_time = start_time
            event.end_time = end_time
        else:
            event = Event(title=title, description=description, start_time=start_time, end_time=end_time)
            db.session.add(event)

        db.session.commit()
        flash('Event saved successfully!', 'success')
        return redirect(url_for('allocate_resources', event_id=event.id))

    return render_template('event_form.html', event=event)

@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'success')
    return redirect(url_for('events'))

# -------------------------- Resources --------------------------

@app.route('/resources')
def resources():
    all_resources = Resource.query.all()
    return render_template('resources.html', resources=all_resources)

@app.route('/resource/new', methods=['GET', 'POST'])
@app.route('/resource/<int:resource_id>/edit', methods=['GET', 'POST'])
def resource_form(resource_id=None):
    resource = Resource.query.get_or_404(resource_id) if resource_id else None

    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']

        if resource:
            resource.name = name
            resource.type = type_
        else:
            resource = Resource(name=name, type=type_)
            db.session.add(resource)

        db.session.commit()
        flash('Resource saved!', 'success')
        return redirect(url_for('resources'))

    return render_template('resource_form.html', resource=resource)

@app.route('/resource/<int:resource_id>/delete', methods=['POST'])
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted.', 'success')
    return redirect(url_for('resources'))

# -------------------------- Allocation --------------------------

@app.route('/allocate/<int:event_id>', methods=['GET', 'POST'])
def allocate_resources(event_id):
    event = Event.query.get_or_404(event_id)
    all_resources = Resource.query.all()
    allocated_resource_ids = [alloc.resource_id for alloc in event.allocations]

    if request.method == 'POST':
        selected_resource_ids = request.form.getlist('resources')  # checkbox list

        # First, check for conflicts on newly added resources
        conflicts = []
        for res_id in selected_resource_ids:
            res_id = int(res_id)
            if res_id not in allocated_resource_ids:  # only check new ones
                if check_conflicts(event.id, res_id, event.start_time, event.end_time):
                    resource = Resource.query.get(res_id)
                    conflicts.append(resource.name)

        if conflicts:
            flash(f"Conflict detected for resource(s): {', '.join(conflicts)}", 'danger')
        else:
            # Remove old allocations
            EventResourceAllocation.query.filter_by(event_id=event.id).delete()

            # Add new ones
            for res_id in selected_resource_ids:
                alloc = EventResourceAllocation(event_id=event.id, resource_id=int(res_id))
                db.session.add(alloc)

            db.session.commit()
            flash('Resources allocated successfully!', 'success')

        return redirect(url_for('allocate_resources', event_id=event.id))

    return render_template('allocate.html', event=event, resources=all_resources, allocated=allocated_resource_ids)

# -------------------------- Conflict View --------------------------

@app.route('/conflicts')
def conflicts():
    conflicts_list = []
    allocations = db.session.query(EventResourceAllocation).all()

    for alloc in allocations:
        resource = alloc.resource
        event = alloc.event

        overlapping = db.session.query(EventResourceAllocation).join(Event).filter(
            EventResourceAllocation.resource_id == resource.id,
            Event.id != event.id,
            db.and_(Event.start_time < event.end_time, Event.end_time > event.start_time)
        ).all()

        if overlapping:
            for overlap_alloc in overlapping:
                conflicts_list.append({
                    'resource': resource.name,
                    'event1': event.title,
                    'event2': overlap_alloc.event.title,
                    'time1': f"{event.start_time} - {event.end_time}",
                    'time2': f"{overlap_alloc.event.start_time} - {overlap_alloc.event.end_time}"
                })

    # Remove duplicates by sorting and unique check
    unique_conflicts = []
    seen = set()
    for c in conflicts_list:
        key = (c['resource'], c['event1'], c['event2'])
        if key not in seen:
            seen.add(key)
            unique_conflicts.append(c)

    return render_template('conflicts.html', conflicts=unique_conflicts)

# -------------------------- Utilisation Report --------------------------

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

        # Add one day to end_date to make it inclusive
        end_date = end_date.replace(hour=23, minute=59, second=59)

        resources = Resource.query.all()
        report_data = []

        for resource in resources:
            allocations = db.session.query(EventResourceAllocation).join(Event).filter(
                EventResourceAllocation.resource_id == resource.id,
                Event.start_time >= start_date,
                Event.end_time <= end_date
            ).all()

            total_hours = 0
            upcoming = []

            for alloc in allocations:
                event = alloc.event
                duration = (event.end_time - event.start_time).total_seconds() / 3600
                total_hours += duration
                upcoming.append({
                    'title': event.title,
                    'time': f"{event.start_time.strftime('%Y-%m-%d %H:%M')} - {event.end_time.strftime('%H:%M')}"
                })

            report_data.append({
                'resource': resource,
                'total_hours': round(total_hours, 2),
                'upcoming': upcoming
            })

        return render_template('report.html', report=report_data, start=start_date.date(), end=end_date.date())

    return render_template('report_form.html')

# -------------------------- Run --------------------------


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_debugger=False, use_reloader=True)