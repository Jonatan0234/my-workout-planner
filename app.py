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
    """Página de inicio"""
    return render_template('home.html', calendar_url=APPLE_CALENDAR_URL)

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

@app.route('/api/calendar-events')
def calendar_events():
    """API para obtener eventos del calendario - SOLUCIÓN REAL"""
    try:
        # SOLUCIÓN 1: Intentar cargar calendario real
        real_events = try_load_real_calendar()
        if real_events:
            return jsonify({
                'success': True,
                'events': real_events,
                'count': len(real_events),
                'message': f'✅ Cargados {len(real_events)} eventos REALES de tu iPhone',
                'source': 'iphone'
            })
        
        # SOLUCIÓN 2: Eventos de ejemplo inteligentes
        smart_events = create_smart_calendar_events()
        return jsonify({
            'success': True,
            'events': smart_events,
            'count': len(smart_events),
            'message': '📅 Usando calendario inteligente - Agrega eventos en tu iPhone para verlos aquí',
            'source': 'smart'
        })
        
    except Exception as e:
        # SOLUCIÓN 3: Fallback robusto
        fallback_events = create_fallback_events()
        return jsonify({
            'success': False,
            'events': fallback_events,
            'count': len(fallback_events),
            'message': '⚠️ No se pudo conectar al calendario - Usando datos de ejemplo',
            'error': str(e),
            'source': 'fallback'
        })

def try_load_real_calendar():
    """Intentar cargar calendario real - MÉTODO DIRECTO"""
    try:
        # Convertir webcal a https
        ical_url = APPLE_CALENDAR_URL.replace('webcal://', 'https://')
        
        # Intentar descargar el calendario
        response = requests.get(ical_url, timeout=10)
        
        if response.status_code == 200:
            # Si tenemos contenido, procesarlo
            return parse_ical_content(response.text)
        else:
            return None
            
    except Exception as e:
        print(f"No se pudo cargar calendario real: {e}")
        return None

def parse_ical_content(ical_text):
    """Parsear contenido iCal de forma simple"""
    events = []
    lines = ical_text.split('\n')
    
    current_event = {}
    in_event = False
    
    for line in lines:
        line = line.strip()
        
        if line == 'BEGIN:VEVENT':
            in_event = True
            current_event = {}
        elif line == 'END:VEVENT':
            in_event = False
            if current_event.get('SUMMARY'):
                event = create_event_from_ical(current_event)
                if event:
                    events.append(event)
            current_event = {}
        elif in_event and ':' in line:
            key, value = line.split(':', 1)
            current_event[key] = value
    
    return events

def create_event_from_ical(ical_event):
    """Crear evento desde datos iCal"""
    try:
        summary = ical_event.get('SUMMARY', 'Workout')
        start_str = ical_event.get('DTSTART', '')
        
        # Parsear fecha básica
        start_date = parse_basic_ical_date(start_str)
        
        return {
            'title': summary,
            'start': start_date.isoformat(),
            'end': (start_date + timedelta(hours=1)).isoformat(),
            'color': get_event_color(summary),
            'allDay': len(start_str) == 8,  # YYYYMMDD
            'description': ical_event.get('DESCRIPTION', ''),
            'isReal': True
        }
    except:
        return None

def parse_basic_ical_date(date_str):
    """Parsear fecha iCal básica"""
    try:
        if len(date_str) == 8:  # YYYYMMDD
            return datetime.strptime(date_str, '%Y%m%d')
        else:
            return datetime.now()
    except:
        return datetime.now()

def create_smart_calendar_events():
    """Crear eventos de calendario inteligentes basados en tu rutina"""
    today = datetime.now()
    events = []
    
    # Tu rutina de entrenamiento semanal
    workout_routine = [
        ("🏋️ Chest & Triceps - Day 1", 0, "#6366f1", "Bench Press, Incline Press, Triceps Dips"),
        ("💪 Back & Biceps - Day 1", 1, "#f59e0b", "Pull-ups, Barbell Rows, Bicep Curls"), 
        ("🦵 Legs & Shoulders - Day 1", 2, "#10b981", "Squats, Lunges, Overhead Press"),
        ("🏃 Cardio & Core", 3, "#ef4444", "Running 30min, Abs workout"),
        ("🏋️ Chest & Triceps - Day 2", 4, "#6366f1", "Chest Fly, Push-ups, Cable Pushdowns"),
        ("💪 Back & Biceps - Day 2", 5, "#f59e0b", "Lat Pulldowns, Seated Rows, Hammer Curls"),
        ("🦵 Legs & Shoulders - Day 2", 6, "#10b981", "Leg Press, RDL, Arnold Press"),
        ("🧘 Rest & Recovery", 7, "#64748b", "Active recovery, Stretching")
    ]
    
    for i in range(14):  # Próximos 14 días
        for title, day_offset, color, description in workout_routine:
            if i % 7 == day_offset:
                event_date = today + timedelta(days=i)
                start_time = event_date.replace(hour=18, minute=0, second=0)
                end_time = start_time + timedelta(hours=1)
                
                events.append({
                    'title': title,
                    'start': start_time.isoformat(),
                    'end': end_time.isoformat(),
                    'color': color,
                    'allDay': False,
                    'description': description,
                    'isReal': False,
                    'isSmart': True
                })
    
    return events[:20]  # Limitar a 20 eventos

def create_fallback_events():
    """Eventos de respaldo"""
    today = datetime.now()
    events = []
    
    basic_workouts = [
        ("Morning Workout", 0, "#6366f1"),
        ("Evening Training", 1, "#f59e0b"),
        ("Cardio Session", 2, "#10b981"),
        ("Strength Training", 3, "#8b5cf6"),
        ("Rest Day", 6, "#64748b")
    ]
    
    for title, day_offset, color in basic_workouts:
        event_date = today + timedelta(days=day_offset)
        start_time = event_date.replace(hour=9, minute=0, second=0)
        
        events.append({
            'title': title,
            'start': start_time.isoformat(),
            'end': (start_time + timedelta(hours=1)).isoformat(),
            'color': color,
            'allDay': False,
            'isReal': False
        })
    
    return events

def get_event_color(event_title):
    """Asignar colores a eventos"""
    title_lower = event_title.lower()
    
    if any(word in title_lower for word in ['chest', 'bench', 'press']):
        return "#6366f1"
    elif any(word in title_lower for word in ['back', 'pull', 'row']):
        return "#f59e0b"
    elif any(word in title_lower for word in ['legs', 'squat', 'deadlift']):
        return "#10b981"
    elif any(word in title_lower for word in ['cardio', 'run', 'bike']):
        return "#ef4444"
    elif any(word in title_lower for word in ['rest', 'recovery']):
        return "#64748b"
    else:
        return "#8b5cf6"

# ==============================
# 🚀 RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)