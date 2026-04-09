(function() {
    function init() {
        const track = document.getElementById('carrosselTrack');
        const prevBtn = document.getElementById('btnPrev');
        const nextBtn = document.getElementById('btnNext');
        if (!track || !prevBtn || !nextBtn) return;

        let currentIndex = 0;
        let cardsPerView = getCardsPerView();

        function getCardsPerView() {
            if (window.innerWidth <= 768) return 1;
            if (window.innerWidth <= 1024) return 2;
            return 3;
        }

        function getCardWidth() {
            const firstCard = track.querySelector('.fibra-card');
            if (!firstCard) return 0;
            const style = window.getComputedStyle(firstCard);
            const gap = parseFloat(window.getComputedStyle(track).columnGap || 20);
            return firstCard.getBoundingClientRect().width + gap;
        }

        function getMaxIndex() {
            return Math.max(0, track.children.length - cardsPerView);
        }

        function updateCarrossel() {
            const cardWidth = getCardWidth();
            if (!cardWidth) return;
            const maxIndex = getMaxIndex();
            if (currentIndex > maxIndex) currentIndex = 0;
            if (currentIndex < 0) currentIndex = maxIndex;
            track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
        }

        prevBtn.onclick = () => {
            const maxIndex = getMaxIndex();
            currentIndex = currentIndex <= 0 ? maxIndex : currentIndex - 1;
            updateCarrossel();
        };

        nextBtn.onclick = () => {
            const maxIndex = getMaxIndex();
            currentIndex = currentIndex >= maxIndex ? 0 : currentIndex + 1;
            updateCarrossel();
        };

        window.addEventListener('resize', function() {
            const newCardsPerView = getCardsPerView();
            if (newCardsPerView !== cardsPerView) {
                cardsPerView = newCardsPerView;
                currentIndex = 0;
                updateCarrossel();
            }
        });

        updateCarrossel();
    }

    document.addEventListener('DOMContentLoaded', init);
    document.body.addEventListener('htmx:afterOnLoad', init);
})();