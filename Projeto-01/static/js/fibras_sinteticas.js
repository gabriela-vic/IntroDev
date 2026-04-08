// static/js/fibras_sinteticas.js
// Carrossel para a página de fibras sintéticas

document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('carrosselTrack');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const indicatorsContainer = document.getElementById('carrosselIndicators');
    
    if (!track || !prevBtn || !nextBtn || !indicatorsContainer) return;
    
    let currentIndex = 0;
    let cardsPerView = getCardsPerView();
    let totalCards = track.children.length;
    
    function getCardsPerView() {
        if (window.innerWidth < 640) return 1;
        if (window.innerWidth < 1024) return 2;
        return 3;
    }
    
    function updateCarrossel() {
        const cardWidth = track.children[0]?.offsetWidth || 300;
        const gap = 24;
        const scrollAmount = currentIndex * (cardWidth + gap);
        track.style.transform = `translateX(-${scrollAmount}px)`;
        updateIndicators();
    }
    
    function updateIndicators() {
        const totalPages = Math.ceil(totalCards / cardsPerView);
        const indicators = document.querySelectorAll('.indicator-dot');
        indicators.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }
    
    function createIndicators() {
        const totalPages = Math.ceil(totalCards / cardsPerView);
        indicatorsContainer.innerHTML = '';
        for (let i = 0; i < totalPages; i++) {
            const dot = document.createElement('button');
            dot.classList.add('indicator-dot');
            if (i === currentIndex) dot.classList.add('active');
            dot.addEventListener('click', () => {
                currentIndex = i;
                updateCarrossel();
            });
            indicatorsContainer.appendChild(dot);
        }
    }
    
    prevBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(totalCards / cardsPerView);
        if (currentIndex > 0) {
            currentIndex--;
            updateCarrossel();
        }
    });
    
    nextBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(totalCards / cardsPerView);
        if (currentIndex < totalPages - 1) {
            currentIndex++;
            updateCarrossel();
        }
    });
    
    window.addEventListener('resize', () => {
        const newCardsPerView = getCardsPerView();
        if (newCardsPerView !== cardsPerView) {
            cardsPerView = newCardsPerView;
            currentIndex = 0;
            track.style.transform = 'translateX(0)';
            createIndicators();
        }
    });
    
    if (totalCards > 0) {
        createIndicators();
    }
});