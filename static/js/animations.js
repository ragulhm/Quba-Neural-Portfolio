document.addEventListener('DOMContentLoaded', () => {
    gsap.registerPlugin(ScrollTrigger);

    // Initial page load animations
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Reveal Hero content sequentially
    tl.fromTo('.gs-fade-up', 
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 1, stagger: 0.2 }
    );

    // Scroll Animations for sections
    const scrollElements = document.querySelectorAll('.gs-scroll');
    scrollElements.forEach((el) => {
        gsap.fromTo(el, 
            { y: 50, opacity: 0 },
            { 
                y: 0, 
                opacity: 1, 
                duration: 1,
                scrollTrigger: {
                    trigger: el,
                    start: "top 80%", // slightly before the element enters the viewport
                    toggleActions: "play none none reverse" 
                }
            }
        );
    });

    // Custom glowing spotlight logic for cards
    // This replicates the `card-spotlight.tsx` effect in vanilla JS
    const spotlightCards = document.querySelectorAll('.vanilla-spotlight');
    spotlightCards.forEach((card) => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
});
