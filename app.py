from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import requests
import json

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
# 🗓️ CALENDAR CONFIG
# ==============================
APPLE_CALENDAR_URL = "webcal://p162-caldav.icloud.com/published/2/NDM1NjgzNzQwNDM1NjgzN9K8AFwQL0suOvwYnQC10mKli_j_u4hAzrX6GT07Fb15_-VeOkUxk1uiakayFx7wCv6PONa07SfUVQLFlrJ4EHo"

# ==============================
# 🖥️ ROUTES
# ==============================
@app.route('/')
def home():
    """Página de inicio simplificada"""
    return render_template('home.html', calendar_url=APPLE_CALENDAR_URL)

@app.route('/workout')
def workout():
    """Página de ejercicios con imágenes completas"""
    category = request.args.get('category')
    day = request.args.get('day')
    selected = None

    if category and day:
        selected = exercises.get(category, {}).get(day, {})

    return render_template('workout.html', selected=selected, category=category, day=day)

@app.route('/api/workout-progress')
def workout_progress():
    """API para datos de progreso (opcional)"""
    progress_data = {
        'completed_workouts': 12,
        'total_workouts': 16,
        'strength_increase': 18,
        'consistency_score': 85
    }
    return jsonify(progress_data)

@app.route('/api/real-calendar-events')
def real_calendar_events():
    """API para obtener eventos REALES del calendario"""
    try:
        # Intentar obtener eventos reales del calendario iCloud
        events = get_real_calendar_events()
        return jsonify({
            'success': True,
            'events': events,
            'count': len(events),
            'message': f'Successfully loaded {len(events)} events from your calendar'
        })
    except Exception as e:
        print(f"Error fetching real calendar: {str(e)}")
        # Fallback a eventos de ejemplo
        events = get_fallback_events()
        return jsonify({
            'success': False,
            'events': events,
            'count': len(events),
            'message': 'Using sample data - Could not connect to your iPhone calendar',
            'error': str(e)
        })

def get_real_calendar_events():
    """Obtener eventos reales del calendario iCloud"""
    try:
        # Convertir webcal:// a https://
        ical_url = APPLE_CALENDAR_URL.replace('webcal://', 'https://')
        
        # Descargar el archivo iCal
        response = requests.get(ical_url, timeout=10)
        response.raise_for_status()
        
        # Parsear manualmente el contenido iCal (simplificado)
        events = parse_ical_content(response.text)
        return events
        
    except Exception as e:
        print(f"Error in get_real_calendar_events: {str(e)}")
        raise e

def parse_ical_content(ical_content):
    """Parsear contenido iCal manualmente"""
    events = []
    lines = ical_content.split('\n')
    
    current_event = {}
    in_event = False
    
    for line in lines:
        line = line.strip()
        
        if line == 'BEGIN:VEVENT':
            in_event = True
            current_event = {}
        elif line == 'END:VEVENT':
            in_event = False
            if current_event.get('summary') and current_event.get('dtstart'):
                # Solo incluir eventos que parezcan ser workouts
                if is_workout_event(current_event.get('summary', '')):
                    events.append(process_calendar_event(current_event))
            current_event = {}
        elif in_event and ':' in line:
            key, value = line.split(':', 1)
            current_event[key] = value
    
    return events

def is_workout_event(summary):
    """Determinar si un evento es un workout basado en el título"""
    workout_keywords = [
        'workout', 'training', 'exercise', 'gym', 'fitness',
        'chest', 'back', 'legs', 'shoulders', 'arms',
        'squat', 'deadlift', 'bench', 'press', 'row', 'pull',
        'cardio', 'run', 'bike', 'swim', 'yoga'
    ]
    summary_lower = summary.lower()
    return any(keyword in summary_lower for keyword in workout_keywords)

def process_calendar_event(event_data):
    """Procesar datos del evento del calendario"""
    summary = event_data.get('summary', 'Workout')
    start_str = event_data.get('dtstart', '')
    end_str = event_data.get('dtend', '')
    
    # Parsear fecha (formato simplificado)
    start_date = parse_ical_date(start_str)
    end_date = parse_ical_date(end_str) if end_str else start_date
    
    return {
        'title': summary,
        'start': start_date.isoformat() if start_date else datetime.now().isoformat(),
        'end': end_date.isoformat() if end_date else start_date.isoformat() if start_date else datetime.now().isoformat(),
        'color': get_event_color(summary),
        'allDay': len(start_str) == 8,  # Si es solo fecha (YYYYMMDD)
        'description': event_data.get('description', ''),
        'location': event_data.get('location', ''),
        'isReal': True
    }

def parse_ical_date(date_str):
    """Parsear fecha desde formato iCal"""
    try:
        if len(date_str) == 8:  # YYYYMMDD
            return datetime.strptime(date_str, '%Y%m%d')
        elif 'T' in date_str:  # YYYYMMDDTHHMMSS
            date_str = date_str.split('T')[0]
            return datetime.strptime(date_str, '%Y%m%d')
        else:
            return datetime.now()
    except:
        return datetime.now()

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
    """Eventos de respaldo si falla la conexión al calendario real"""
    today = datetime.now()
    events = []
    
    # Crear eventos de ejemplo para la próxima semana
    workout_schedule = [
        ("Chest & Triceps - Day 1", 0, "#6366f1"),
        ("Back & Biceps - Day 1", 1, "#f59e0b"),
        ("Legs & Shoulders - Day 1", 2, "#10b981"),
        ("Cardio - 30min Running", 3, "#ef4444"),
        ("Chest & Triceps - Day 2", 4, "#6366f1"),
        ("Back & Biceps - Day 2", 5, "#f59e0b"),
        ("Rest Day - Active Recovery", 6, "#64748b")
    ]
    
    for title, day_offset, color in workout_schedule:
        event_date = today + timedelta(days=day_offset)
        start_time = event_date.replace(hour=7, minute=0, second=0)
        end_time = event_date.replace(hour=8, minute=0, second=0)
        
        events.append({
            'title': title,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'color': color,
            'allDay': False,
            'description': 'Workout session from your training plan',
            'location': 'Gym',
            'isReal': False
        })
    
    return events

# ==============================
# 🚀 RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)