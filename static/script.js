// Global variables
let mealsData = {
    bulking: [],
    cutting: []
};

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize the application
async function initializeApp() {
    setupNavigation();
    await loadMealsData();
    renderMeals();
    setupScrollEffects();
}

// Navigation functionality
function setupNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navbar = document.getElementById('navbar');

    // Mobile menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Close mobile menu when clicking on links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
}

// Smooth scrolling function
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        const offsetTop = element.offsetTop - 80; // Account for fixed navbar
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// Load meals data from API
async function loadMealsData() {
    try {
        // Load bulking meals
        const bulkingResponse = await fetch('/api/meals?category=bulking');
        if (bulkingResponse.ok) {
            mealsData.bulking = await bulkingResponse.json();
        }

        // Load cutting meals
        const cuttingResponse = await fetch('/api/meals?category=cutting');
        if (cuttingResponse.ok) {
            mealsData.cutting = await cuttingResponse.json();
        }
    } catch (error) {
        console.error('Error loading meals data:', error);
        // Fallback to local data if API fails
        loadFallbackData();
    }
}

// Fallback data in case API is not available
function loadFallbackData() {
    mealsData.bulking = [
        {
            id: "1",
            title: "Whole Milk and Cottage Cheese",
            description: "High-protein dairy combination for muscle building",
            calories: "850 cal",
            protein: "45g protein",
            image: "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "2",
            title: "Nuts and Nut Butters",
            description: "Calorie-dense healthy fats and proteins",
            calories: "720 cal",
            protein: "25g protein",
            image: "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "3",
            title: "Whole Eggs",
            description: "Complete protein with essential amino acids",
            calories: "680 cal",
            protein: "42g protein",
            image: "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "4",
            title: "Rice",
            description: "Complex carbohydrates for energy and recovery",
            calories: "450 cal",
            protein: "8g protein",
            image: "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "5",
            title: "Chicken and Mutton",
            description: "Lean protein sources for muscle development",
            calories: "650 cal",
            protein: "65g protein",
            image: "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        }
    ];

    mealsData.cutting = [
        {
            id: "6",
            title: "Carbohydrates",
            description: "Complex carbs for sustained energy during cuts",
            calories: "320 cal",
            protein: "12g protein",
            image: "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "7",
            title: "Lean Fish",
            description: "Low-calorie, high-protein white fish",
            calories: "280 cal",
            protein: "45g protein",
            image: "https://images.unsplash.com/photo-1485963631004-f2f00b1d6606?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "8",
            title: "Eggs",
            description: "High-quality protein with essential nutrients",
            calories: "180 cal",
            protein: "24g protein",
            image: "https://images.unsplash.com/photo-1525351484163-7529414344d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "9",
            title: "Dairy",
            description: "Low-fat dairy products for protein",
            calories: "250 cal",
            protein: "28g protein",
            image: "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "10",
            title: "Pulses (Lentils, Beans, Peas)",
            description: "Plant-based protein and fiber",
            calories: "200 cal",
            protein: "18g protein",
            image: "https://images.unsplash.com/photo-1586795158095-e891c9e1a42b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        },
        {
            id: "11",
            title: "Tofu, Seeds & Nuts",
            description: "Plant-based proteins and healthy fats",
            calories: "290 cal",
            protein: "22g protein",
            image: "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600"
        }
    ];
}

// Render meals in their respective sections
function renderMeals() {
    renderMealSection('bulking-meals', mealsData.bulking);
    renderMealSection('cutting-meals', mealsData.cutting);
}

// Render meals for a specific section
function renderMealSection(containerId, meals) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';

    meals.forEach(meal => {
        const mealCard = createMealCard(meal);
        container.appendChild(mealCard);
    });
}

// Create a meal card element
function createMealCard(meal) {
    const card = document.createElement('div');
    card.className = 'meal-card';
    card.setAttribute('data-aos', 'fade-up');
    
    card.innerHTML = `
        <img src="${meal.image}" alt="${meal.title}" class="meal-image" loading="lazy">
        <div class="meal-content">
            <h3 class="meal-title">${meal.title}</h3>
            <p class="meal-description">${meal.description}</p>
            <div class="meal-stats">
                <span class="meal-calories">${meal.calories}</span>
                <span class="meal-protein">${meal.protein}</span>
            </div>
        </div>
    `;

    return card;
}

// Setup scroll effects and animations
function setupScrollEffects() {
    // Add intersection observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all meal cards and sections
    document.querySelectorAll('.meal-card, .feature-item, .evidence-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Utility function to handle API errors
function handleApiError(error, fallbackAction) {
    console.error('API Error:', error);
    if (typeof fallbackAction === 'function') {
        fallbackAction();
    }
}

// Add event listeners for buttons
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn')) {
        // Add ripple effect
        const btn = e.target;
        const rect = btn.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        btn.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimized scroll handler
const handleScroll = debounce(() => {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}, 10);

window.addEventListener('scroll', handleScroll);