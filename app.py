from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone
import requests
from icalendar import Calendar
import io
import time

app = Flask(__name__)

# ==============================
# 💪 WORKOUT DATA CONFIGURATION  
# ==============================
exercises = {
    "chest_triceps": {
        "day1": {
            "chest": [
                {
                    "name": "Bench Press",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Chest/Day1/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Chest.png",
                    "description": "Lie flat on a bench, grip slightly wider than shoulder-width. Lower the bar under control to mid-chest and press up explosively. Keep feet planted and core tight.",
                    "sets": "4 sets",
                    "reps": "8-12 reps",
                    "rest": "90s rest"
                },
                {
                    "name": "Incline Dumbbell Press",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Chest/Day1/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Chest.png",
                    "description": "Set bench to 30–45°. Press dumbbells up and slightly together. Focus on pressing with the upper chest and control the negative.",
                    "sets": "3 sets",
                    "reps": "10-15 reps",
                    "rest": "75s rest"
                }
            ],
            "triceps": [
                {
                    "name": "Triceps Dips",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Triceps/Day1/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Triceps.png",
                    "description": "Lower your body until elbows are ~90°. Keep torso upright to emphasize triceps. Push back until arms are extended.",
                    "sets": "3 sets",
                    "reps": "12-15 reps",
                    "rest": "60s rest"
                },
                {
                    "name": "Cable Pushdowns",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Triceps/Day1/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Triceps.png",
                    "description": "Keep elbows locked at your sides; push the bar down to full extension while squeezing the triceps.",
                    "sets": "4 sets",
                    "reps": "15-20 reps",
                    "rest": "45s rest"
                }
            ]
        },
        "day2": {
            "chest": [
                {
                    "name": "Chest Fly",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Chest/Day2/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Chest.png",
                    "description": "Maintain a slight bend in the elbow, open wide feeling a stretch in the chest, then bring hands together with control.",
                    "sets": "4 sets",
                    "reps": "12-15 reps",
                    "rest": "60s rest"
                },
                {
                    "name": "Push-ups",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Chest/Day2/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Chest.png",
                    "description": "Keep a straight body line. Lower until chest nears the floor, then push up. Can modify on knees or elevate hands for progression.",
                    "sets": "3 sets",
                    "reps": "AMRAP",
                    "rest": "90s rest"
                }
            ],
            "triceps": [
                {
                    "name": "Close-Grip Bench Press",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Triceps/Day2/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Triceps.png",
                    "description": "Use a narrower grip to shift emphasis to triceps. Keep elbows close during descent and press focusing on triceps drive.",
                    "sets": "4 sets",
                    "reps": "8-12 reps",
                    "rest": "75s rest"
                },
                {
                    "name": "Overhead Dumbbell Extension",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Triceps/Day2/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Triceps.png",
                    "description": "Stabilize core, lower the dumbbell behind the head with a controlled motion and extend to feel the long head of the triceps.",
                    "sets": "3 sets",
                    "reps": "12-15 reps",
                    "rest": "60s rest"
                }
            ]
        }
    },
    "back_biceps": {
        "day1": {
            "back": [
                {
                    "name": "Pull-Ups",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Back/Day1/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Back.png",
                    "description": "Grip slightly wider than shoulder width, pull your chest toward the bar. Lead with the elbows and squeeze shoulder blades.",
                    "sets": "4 sets",
                    "reps": "6-10 reps",
                    "rest": "90s rest"
                },
                {
                    "name": "Barbell Row",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Back/Day1/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Back.png",
                    "description": "Hinge at hips, keep back flat, pull bar toward lower ribs and control on the way down.",
                    "sets": "4 sets",
                    "reps": "8-12 reps",
                    "rest": "75s rest"
                }
            ],
            "biceps": [
                {
                    "name": "Barbell Curl",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Biceps/Day1/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Biceps.png",
                    "description": "Keep elbows fixed at sides, curl the bar with controlled motion and squeeze at the top.",
                    "sets": "3 sets",
                    "reps": "10-15 reps",
                    "rest": "60s rest"
                },
                {
                    "name": "Hammer Curl",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Biceps/Day1/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Biceps.png",
                    "description": "Neutral grip to emphasize brachialis and forearm; lift with control and avoid swinging.",
                    "sets": "3 sets",
                    "reps": "12-15 reps",
                    "rest": "60s rest"
                }
            ]
        },
        "day2": {
            "back": [
                {
                    "name": "Lat Pulldown",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Back/Day2/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Back.png",
                    "description": "Pull the bar to upper chest while squeezing the lats; avoid leaning too far back.",
                    "sets": "4 sets",
                    "reps": "10-12 reps",
                    "rest": "75s rest"
                },
                {
                    "name": "Seated Cable Row",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Back/Day2/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Back.png",
                    "description": "Keep torso upright, pull handle to abdomen and squeeze shoulder blades together.",
                    "sets": "4 sets",
                    "reps": "12-15 reps",
                    "rest": "60s rest"
                }
            ],
            "biceps": [
                {
                    "name": "Concentration Curl",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Biceps/Day2/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Biceps.png",
                    "description": "Seated, elbow braced on knee; curl slow and squeeze at the top to isolate the biceps.",
                    "sets": "3 sets",
                    "reps": "12-15 reps",
                    "rest": "45s rest"
                },
                {
                    "name": "Preacher Curl",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Biceps/Day2/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Biceps.png",
                    "description": "Use preacher bench to eliminate momentum; focus on full range with controlled negatives.",
                    "sets": "3 sets",
                    "reps": "10-12 reps",
                    "rest": "60s rest"
                }
            ]
        }
    },
    "legs_shoulders": {
        "day1": {
            "legs": [
                {
                    "name": "Squats",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Legs/Day1/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Legs.png",
                    "description": "Feet shoulder-width, drive hips back and down. Keep chest up and knees tracking toes. Drive through heels.",
                    "sets": "4 sets",
                    "reps": "6-10 reps",
                    "rest": "120s rest"
                },
                {
                    "name": "Lunges",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Legs/Day1/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Legs.png",
                    "description": "Step forward, lower until both knees ~90°. Keep torso vertical and push through front heel.",
                    "sets": "3 sets",
                    "reps": "10-12 reps",
                    "rest": "90s rest"
                }
            ],
            "shoulders": [
                {
                    "name": "Overhead Press",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Shoulders/Day1/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Shoulders.png",
                    "description": "Press the weight overhead with a tight core, avoid excessive lumbar extension. Lock out and control the descent.",
                    "sets": "4 sets",
                    "reps": "8-12 reps",
                    "rest": "90s rest"
                },
                {
                    "name": "Lateral Raise",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Shoulders/Day1/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Shoulders.png",
                    "description": "Slight bend in elbow, raise to shoulder height focusing on the lateral deltoid.",
                    "sets": "3 sets",
                    "reps": "15-20 reps",
                    "rest": "60s rest"
                }
            ]
        },
        "day2": {
            "legs": [
                {
                    "name": "Leg Press",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Legs/Day2/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Legs.png",
                    "description": "Place feet mid-plate, push with heels and mid-foot. Avoid locking knees at top.",
                    "sets": "4 sets",
                    "reps": "12-15 reps",
                    "rest": "90s rest"
                },
                {
                    "name": "Romanian Deadlift",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Legs/Day2/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Legs.png",
                    "description": "Hinge at hips with slight knee bend; feel stretch in hamstrings and control the ascent.",
                    "sets": "4 sets",
                    "reps": "10-12 reps",
                    "rest": "90s rest"
                }
            ],
            "shoulders": [
                {
                    "name": "Front Raise",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Shoulders/Day2/1.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Shoulders.png",
                    "description": "Raise weight in front of the body to shoulder height with straight arms (slight bend) to target anterior delts.",
                    "sets": "3 sets",
                    "reps": "12-15 reps",
                    "rest": "60s rest"
                },
                {
                    "name": "Arnold Press",
                    "image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Pictures/Shoulders/Day2/2.gif",
                    "muscle_image": "https://raw.githubusercontent.com/Jonatan0234/workoutplanner/main/Muscles/Shoulders.png",
                    "description": "Rotate dumbbells as you press to engage multiple heads of the deltoid; control both phases.",
                    "sets": "4 sets",
                    "reps": "10-12 reps",
                    "rest": "75s rest"
                }
            ]
        }
    }
}

# ==============================
# 🗓️ GOOGLE CALENDAR CONFIG
# ==============================
GOOGLE_CALENDAR_URL = "https://calendar.google.com/calendar/ical/n9kbghpits33lfhkfels27i1afosnkic%40import.calendar.google.com/public/basic.ics"

# ==============================
# 🖥️ ROUTES
# ==============================
@app.route('/')
def home():
    return render_template('home.html', calendar_url=GOOGLE_CALENDAR_URL)

@app.route('/workout')
def workout():
    category = request.args.get('category')
    day = request.args.get('day')
    selected = None

    if category and day:
        selected = exercises.get(category, {}).get(day, {})

    return render_template('workout.html', selected=selected, category=category, day=day)

@app.route('/api/workout-progress')
def workout_progress():
    progress_data = {
        'completed_workouts': 12,
        'total_workouts': 16,
        'strength_increase': 18,
        'consistency_score': 85
    }
    return jsonify(progress_data)

@app.route('/api/real-calendar-events')
def real_calendar_events():
    """Eventos REALES de Google Calendar - 3 días antes + hoy + 4 días después"""
    try:
        events = get_google_calendar_events()
        
        # Filtrar eventos del rango: 3 días antes hasta 4 días después
        today = datetime.now().date()
        start_date = today - timedelta(days=3)
        end_date = today + timedelta(days=4)
        
        filtered_events = []
        for event in events:
            try:
                event_date = datetime.fromisoformat(event['datetime'].replace('Z', '+00:00')).date()
                if start_date <= event_date <= end_date:
                    filtered_events.append(event)
            except Exception as e:
                print(f"⚠️ Error filtrando evento: {e}")
                continue
        
        print(f"🎯 Eventos del rango {start_date} a {end_date}: {len(filtered_events)}")
        
        return jsonify({
            'success': True,
            'events': filtered_events,
            'count': len(filtered_events),
            'message': f'✅ Mostrando {len(filtered_events)} eventos (3 días antes + hoy + 4 días después)',
            'source': 'google_calendar',
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'today': today.isoformat()
            }
        })
            
    except Exception as e:
        print(f"❌ Error cargando calendario: {str(e)}")
        return jsonify({
            'success': False,
            'events': [],
            'count': 0,
            'message': f'❌ Error: {str(e)}',
            'source': 'error'
        })

def get_google_calendar_events():
    """Obtener eventos de Google Calendar"""
    try:
        print(f"🔗 Conectando a Google Calendar...")
        
        # Descargar el archivo iCal
        response = requests.get(GOOGLE_CALENDAR_URL, timeout=10)
        response.raise_for_status()
        
        print(f"📥 Calendario Google descargado: {len(response.text)} caracteres")
        
        # Parsear con biblioteca iCalendar
        events = parse_with_icalendar_lib(response.text)
        print(f"📅 Eventos Google parseados: {len(events)}")
        
        return events
        
    except Exception as e:
        print(f"❌ Error cargando Google Calendar: {str(e)}")
        return []

def parse_with_icalendar_lib(ical_content):
    """Parsear usando biblioteca iCalendar"""
    events = []
    
    try:
        # Parsear el calendario con la biblioteca
        cal = Calendar.from_ical(ical_content)
        
        # Recorrer todos los componentes del calendario
        for component in cal.walk():
            if component.name == "VEVENT":
                try:
                    event_data = parse_icalendar_component(component)
                    if event_data:
                        events.append(event_data)
                except Exception as e:
                    print(f"⚠️ Error parseando componente: {str(e)}")
                    continue
                    
    except Exception as e:
        print(f"❌ Error parseando calendario: {str(e)}")
        raise e
    
    return events

def parse_icalendar_component(component):
    """Parsear componente VEVENT"""
    try:
        # Obtener campos básicos
        summary = component.get('SUMMARY')
        dtstart = component.get('DTSTART')
        
        if not summary or not dtstart:
            return None
        
        # Extraer datetime
        start_dt = dtstart.dt
        
        # Crear evento
        event = {
            'title': str(summary),
            'isReal': True
        }
        
        # Manejar fecha/hora
        if isinstance(start_dt, datetime):
            event_start = start_dt
            event['allDay'] = False
        else:
            event_start = datetime.combine(start_dt, datetime.min.time())
            event['allDay'] = True
        
        event['datetime'] = event_start.isoformat()
        event['date'] = event_start.strftime("%Y-%m-%d")
        event['day_name'] = event_start.strftime("%A")
        event['day_number'] = event_start.day
        event['month_name'] = event_start.strftime("%B")
        event['year'] = event_start.year
        event['month'] = event_start.month
        event['day'] = event_start.day
        
        # Campos opcionales
        description = component.get('DESCRIPTION')
        location = component.get('LOCATION')
        event['description'] = str(description) if description else ''
        event['location'] = str(location) if location else ''
        
        # Color basado en título
        event['color'] = get_event_color(str(summary))
        
        return event
        
    except Exception as e:
        print(f"❌ Error parseando componente: {str(e)}")
        return None

def get_event_color(event_title):
    """Asignar colores basado en el contenido del evento"""
    if not event_title:
        return "#8b5cf6"
        
    title_lower = event_title.lower()
    
    if any(word in title_lower for word in ['chest', 'bench', 'press']):
        return "#6366f1"
    elif any(word in title_lower for word in ['back', 'pull', 'row']):
        return "#f59e0b"
    elif any(word in title_lower for word in ['legs', 'squat', 'deadlift']):
        return "#10b981"
    elif any(word in title_lower for word in ['shoulders', 'press', 'raise']):
        return "#8b5cf6"
    elif any(word in title_lower for word in ['cardio', 'run', 'bike', 'swim']):
        return "#ef4444"
    elif any(word in title_lower for word in ['rest', 'recovery', 'off']):
        return "#64748b"
    elif any(word in title_lower for word in ['yoga', 'stretch', 'flexibility']):
        return "#06b6d4"
    else:
        return "#8b5cf6"

# ==============================
# 🚀 RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)