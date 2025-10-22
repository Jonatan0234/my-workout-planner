from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import requests
import re

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
# 🗓️ CALENDAR CONFIG - URL REAL
# ==============================
APPLE_CALENDAR_URL = "webcal://p162-caldav.icloud.com/published/2/NDM1NjgzNzQwNDM1NjgzN9K8AFwQL0suOvwYnQC10mKli_j_u4hAzrX6GT07Fb15_-VeOkUxk1uiakayFx7wCv6PONa07SfUVQLFlrJ4EHo"

# ==============================
# 🖥️ ROUTES
# ==============================
@app.route('/')
def home():
    return render_template('home.html', calendar_url=APPLE_CALENDAR_URL)

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
    """SOLO eventos REALES del calendario - SIN eventos smart"""
    try:
        events = get_real_iphone_calendar_events()
        
        if events:
            return jsonify({
                'success': True,
                'events': events,
                'count': len(events),
                'message': f'✅ Cargados {len(events)} eventos REALES de tu iPhone',
                'source': 'iphone'
            })
        else:
            return jsonify({
                'success': False,
                'events': [],
                'count': 0,
                'message': '📭 No se encontraron eventos en tu calendario de iPhone',
                'source': 'iphone'
            })
            
    except Exception as e:
        print(f"Error cargando calendario real: {str(e)}")
        return jsonify({
            'success': False,
            'events': [],
            'count': 0,
            'message': f'❌ Error conectando a tu calendario: {str(e)}',
            'source': 'error'
        })

def get_real_iphone_calendar_events():
    """Obtener eventos REALES del calendario de iPhone"""
    try:
        # Convertir webcal:// a https://
        ical_url = APPLE_CALENDAR_URL.replace('webcal://', 'https://')
        print(f"Intentando conectar a: {ical_url}")
        
        # Headers para simular un navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        }
        
        # Descargar el archivo iCal
        response = requests.get(ical_url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        print(f"✅ Calendario descargado. Tamaño: {len(response.text)} caracteres")
        
        # Parsear eventos del iCal
        events = parse_ical_events(response.text)
        print(f"✅ Eventos parseados: {len(events)}")
        
        return events
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {str(e)}")
        raise Exception(f"No se pudo conectar al calendario: {str(e)}")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        raise e

def parse_ical_events(ical_content):
    """Parsear eventos desde contenido iCal REAL"""
    events = []
    
    # Buscar todos los eventos en el contenido iCal
    event_blocks = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', ical_content, re.DOTALL)
    
    print(f"Encontrados {len(event_blocks)} bloques de evento")
    
    for block in event_blocks:
        try:
            event_data = parse_event_block(block)
            if event_data and is_recent_event(event_data):
                events.append(event_data)
        except Exception as e:
            print(f"Error parseando evento: {str(e)}")
            continue
    
    # Ordenar eventos por fecha
    events.sort(key=lambda x: x['start'])
    
    return events

def parse_event_block(block):
    """Parsear un bloque de evento individual"""
    event = {}
    
    # Extraer campos principales
    summary_match = re.search(r'SUMMARY:(.*?)(?:\n|$)', block)
    dtstart_match = re.search(r'DTSTART(?:;VALUE=DATE)?:(.*?)(?:\n|$)', block)
    dtend_match = re.search(r'DTEND(?:;VALUE=DATE)?:(.*?)(?:\n|$)', block)
    description_match = re.search(r'DESCRIPTION:(.*?)(?:\n|$)', block)
    location_match = re.search(r'LOCATION:(.*?)(?:\n|$)', block)
    
    if summary_match:
        event['title'] = clean_ical_text(summary_match.group(1))
    else:
        return None
    
    # Parsear fechas
    if dtstart_match:
        event['start'] = parse_ical_datetime(dtstart_match.group(1))
        event['allDay'] = len(dtstart_match.group(1)) == 8  # YYYYMMDD = todo el día
    else:
        return None
    
    if dtend_match:
        event['end'] = parse_ical_datetime(dtend_match.group(1))
    else:
        # Si no hay end, asumir 1 hora de duración
        event['end'] = event['start'] + timedelta(hours=1)
    
    # Campos opcionales
    if description_match:
        event['description'] = clean_ical_text(description_match.group(1))
    
    if location_match:
        event['location'] = clean_ical_text(location_match.group(1))
    
    # Información adicional
    event['color'] = get_event_color(event['title'])
    event['isReal'] = True
    event['date'] = event['start'].strftime("%Y-%m-%d")
    event['day_name'] = event['start'].strftime("%A")
    event['day_number'] = event['start'].day
    event['month_name'] = event['start'].strftime("%B")
    
    return event

def parse_ical_datetime(datetime_str):
    """Parsear fecha/hora desde formato iCal"""
    try:
        # Formato: YYYYMMDDTHHMMSS o YYYYMMDD
        if 'T' in datetime_str:
            # Con hora
            return datetime.strptime(datetime_str, '%Y%m%dT%H%M%S')
        else:
            # Solo fecha (todo el día)
            return datetime.strptime(datetime_str, '%Y%m%d')
    except ValueError:
        # Intentar formato alternativo
        try:
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except:
            print(f"⚠️ No se pudo parsear fecha: {datetime_str}")
            return datetime.now()

def clean_ical_text(text):
    """Limpiar texto iCal (quitar secuencias de escape)"""
    # Reemplazar secuencias escapadas
    text = text.replace('\\n', ' ').replace('\\,', ',').replace('\\;', ';')
    # Quitar espacios extra
    return text.strip()

def is_recent_event(event):
    """Filtrar solo eventos recientes o futuros"""
    now = datetime.now()
    event_date = event['start']
    
    # Mostrar eventos desde 7 días atrás hasta 30 días en el futuro
    start_range = now - timedelta(days=7)
    end_range = now + timedelta(days=30)
    
    return start_range <= event_date <= end_range

def get_event_color(event_title):
    """Asignar colores basado en el contenido del evento"""
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
        return "#8b5cf6"  # Color por defecto

# ==============================
# 🚀 RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)