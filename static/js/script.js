// workout-planner.js
class WorkoutPlanner {
    constructor() {
        this.init();
    }

    init() {
        this.initEventListeners();
        this.initAnimations();
        this.loadUserPreferences();
    }

    initEventListeners() {
        // Mobile menu toggle
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        const sidebar = document.getElementById('sidebar');

        if (mobileMenuToggle && sidebar) {
            mobileMenuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('active');
                document.body.classList.toggle('menu-open');
            });
        }

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Exercise card interactions
        this.initExerciseCards();
    }

    initExerciseCards() {
        const exerciseCards = document.querySelectorAll('.exercise-card');
        
        exerciseCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });

            // Click to flip card (if needed)
            card.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
        });
    }

    initAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.feature-card, .workout-card, .progress-item').forEach(el => {
            observer.observe(el);
        });

        // Initialize progress bar animations
        this.animateProgressBars();
    }

    animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');
        
        progressBars.forEach(bar => {
            const width = bar.style.width || bar.getAttribute('data-width');
            if (width) {
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 500);
            }
        });
    }

    loadUserPreferences() {
        // Load theme preference
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-bs-theme', savedTheme);

        // Load other user preferences...
    }

    saveUserPreferences(key, value) {
        localStorage.setItem(key, value);
    }

    // Workout timer functionality
    startTimer(duration, display) {
        let timer = duration, minutes, seconds;
        
        const interval = setInterval(() => {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                this.timerComplete();
            }
        }, 1000);
    }

    timerComplete() {
        // Play sound or show notification
        if (Notification.permission === 'granted') {
            new Notification('Workout Timer Complete!');
        }
        
        // Vibrate if supported
        if (navigator.vibrate) {
            navigator.vibrate([200, 100, 200]);
        }
    }

    // Progress tracking
    updateProgress(workoutId, completed) {
        const progress = JSON.parse(localStorage.getItem('workoutProgress') || '{}');
        progress[workoutId] = completed;
        localStorage.setItem('workoutProgress', JSON.stringify(progress));
        
        this.updateProgressUI();
    }

    updateProgressUI() {
        const progress = JSON.parse(localStorage.getItem('workoutProgress') || '{}');
        const completedWorkouts = Object.values(progress).filter(Boolean).length;
        const totalWorkouts = Object.keys(progress).length;
        
        // Update progress bars and counters
        const completionRate = totalWorkouts > 0 ? (completedWorkouts / totalWorkouts) * 100 : 0;
        document.querySelectorAll('.completion-rate').forEach(el => {
            el.textContent = Math.round(completionRate) + '%';
        });
    }

    // Export workout data
    exportWorkoutPlan() {
        const workoutData = {
            exercises: this.getCurrentWorkout(),
            timestamp: new Date().toISOString(),
            version: '1.0'
        };
        
        const dataStr = JSON.stringify(workoutData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `workout-plan-${new Date().getTime()}.json`;
        link.click();
    }

    getCurrentWorkout() {
        // Extract current workout data from the page
        const exercises = [];
        document.querySelectorAll('.exercise-card').forEach(card => {
            const name = card.querySelector('.exercise-name')?.textContent;
            const sets = card.querySelector('.exercise-sets')?.textContent;
            const reps = card.querySelector('.exercise-reps')?.textContent;
            
            if (name) {
                exercises.push({ name, sets, reps });
            }
        });
        
        return exercises;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    window.workoutPlanner = new WorkoutPlanner();
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // Register service worker for PWA capabilities
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    }
});