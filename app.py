from datetime import datetime, timedelta
import requests
import json
import os
from icalendar import Calendar
import urllib.request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ==============================
# 💪 WORKOUT DATA CONFIGURATION
# ==============================
exercises = {
    "chest_triceps": {
        "day1": {
            "chest": [
                {
                    "name": "Bench Press prueba",
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
                },
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
# 🗓️ CALENDAR CONFIG - URL REAL DE TU CALENDARIO
# ==============================
# Esta es la URL pública de tu calendario iCloud
ICAL_URL = "https://p162-caldav.icloud.com/published/2/NDM1NjgzNzQwNDM1NjgzN9K8AFwQL0suOvwYnQC10mKli_j_u4hAzrX6GT07Fb15_-VeOkUxk1uiakayFx7wCv6PONa07SfUVQLFlrJ4EHo"

# ==============================
# 🖥️ ROUTES
# ==============================
@app.route('/')
def home():
    """Página de inicio"""
    return render_template('home.html', calendar_url=ICAL_URL)

@app.route('/workout')
def workout():
    """Página de ejercicios"""
    category = request.args.get('category')
    day = request.args.get('day')
    selected = None

    if category and day:
        selected = exercises.get(category, {}).get(day, {})

    return render_template('workout.html', selected=selected, category=category, day=day)

@app.route('/api/workout-progress')
def workout_progress():
    """API para datos de progreso"""
    progress_data = {
        'completed_workouts': 12,
        'total_workouts': 16,
        'strength_increase': 18,
        'consistency_score': 85
    }
    return jsonify(progress_data)

@app.route('/api/real-calendar-events')
def real_calendar_events():
    """API para obtener eventos REALES del calendario iCloud"""
    try:
        events = get_real_ical_events()
        return jsonify({
            'success': True,
            'events': events,
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error fetching calendar: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'events': get_fallback_events()
        })

def get_real_ical_events():
    """Obtener eventos reales del calendario iCloud"""
    events = []
    
    try:
        # Descargar el archivo iCal
        response = requests.get(ICAL_URL, timeout=10)
        response.raise_for_status()
        
        # Parsear el calendario iCal
        cal = Calendar.from_ical(response.text)
        
        today = datetime.now().date()
        start_date = today - timedelta(days=7)  # Una semana atrás
        end_date = today + timedelta(days=30)   # Un mes adelante
        
        for component in cal.walk():
            if component.name == "VEVENT":
                start_dt = component.get('dtstart').dt
                end_dt = component.get('dtend').dt
                summary = str(component.get('summary', ''))
                description = str(component.get('description', ''))
                
                # Convertir a datetime si es solo date
                if isinstance(start_dt, datetime):
                    event_date = start_dt
                else:
                    event_date = datetime.combine(start_dt, datetime.min.time())
                
                # Filtrar eventos en el rango de fechas
                if start_date <= event_date.date() <= end_date:
                    event_data = {
                        'title': summary,
                        'start': event_date.isoformat(),
                        'end': end_dt.isoformat() if end_dt else event_date.isoformat(),
                        'description': description,
                        'color': get_event_color(summary),
                        'allDay': not isinstance(start_dt, datetime),
                        'location': str(component.get('location', ''))
                    }
                    events.append(event_data)
        
        # Ordenar eventos por fecha
        events.sort(key=lambda x: x['start'])
        
    except Exception as e:
        print(f"Error parsing iCal: {e}")
        raise e
    
    return events

def get_event_color(event_title):
    """Asignar colores basado en el contenido del evento"""
    title_lower = event_title.lower()
    
    if any(word in title_lower for word in ['chest', 'bench', 'press']):
        return "#6366f1"  # Primary
    elif any(word in title_lower for word in ['back', 'pull', 'row']):
        return "#f59e0b"  # Warning
    elif any(word in title_lower for word in ['legs', 'squat', 'deadlift']):
        return "#10b981"  # Success
    elif any(word in title_lower for word in ['shoulders', 'press', 'raise']):
        return "#8b5cf6"  # Purple
    elif any(word in title_lower for word in ['rest', 'recovery', 'off']):
        return "#64748b"  # Gray
    elif any(word in title_lower for word in ['cardio', 'run', 'bike']):
        return "#ef4444"  # Danger
    else:
        return "#06b6d4"  # Cyan

def get_fallback_events():
    """Eventos de respaldo si falla la conexión al calendario"""
    today = datetime.now()
    events = []
    
    workout_days = [
        ("Chest & Triceps - Day 1", 0, "#6366f1"),
        ("Back & Biceps - Day 1", 1, "#f59e0b"),
        ("Legs & Shoulders - Day 1", 2, "#10b981"),
        ("Cardio - 30min", 3, "#ef4444"),
        ("Chest & Triceps - Day 2", 4, "#6366f1"),
        ("Back & Biceps - Day 2", 5, "#f59e0b"),
        ("Rest Day", 6, "#64748b")
    ]
    
    for title, day_offset, color in workout_days:
        event_date = today + timedelta(days=day_offset)
        events.append({
            'title': title,
            'start': event_date.replace(hour=7, minute=0, second=0).isoformat(),
            'end': event_date.replace(hour=8, minute=0, second=0).isoformat(),
            'color': color,
            'allDay': False,
            'description': 'Workout session',
            'isFallback': True
        })
    
    return events

# ==============================
# 🚀 RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)