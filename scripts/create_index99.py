import os

svg_path = r'c:\Users\Matheus Gabriel\Desktop\Instituto Clio\template\logo svg.svg'
with open(svg_path, 'r', encoding='utf-8') as f:
    svg_content = f.read()

# Replace the svg width and height to be responsive
svg_content = svg_content.replace('width="1514" height="1500"', 'viewBox="0 0 1514 1500" width="100%" height="100%" preserveAspectRatio="xMinYMid meet"')

html_template = f'''<!DOCTYPE html>
<html lang="pt-BR" class="lenis lenis-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instituto Clio | Preservação da Memória e Inovação</title>
    <meta name="description" content="Preservando a memória histórico-cultural e fomentando a transformação social com tecnologia.">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- Splitting.js -->
    <link rel="stylesheet" href="https://unpkg.com/splitting/dist/splitting.css">
    <link rel="stylesheet" href="https://unpkg.com/splitting/dist/splitting-cells.css">

    <style>
        :root {{
            /* === PALETA INSTITUTO CLIO === */
            --color-bg:          #FFFFFF;   /* Branco — fundo principal */
            --color-bg-warm:     #EEF7F9;   /* Teal glacial — fundo alternativo */
            --color-primary:     #3E89A3;   /* Teal profundo — identidade da marca */
            --color-primary-alt: #519BB5;   /* Teal médio — hover/ênfase */
            --color-text:        #1A3D4F;   /* Teal quase-preto — headings e textos */
            --color-text-light:  #2D607A;   /* Teal médio-escuro — subtextos */
            --color-bg-alt:      #C3E4E9;   /* Teal pálido — fundos secundários */
            --color-bg-alt2:     #E6F4F7;   /* Teal quase-branco — divisores, cards */
            --color-accent:      #7AC1D7;   /* Teal claro — hover, glows, acentos */
            --color-accent-alt:  #C3E4E9;   /* Teal pálido — backgrounds sutis */

            /* Typography */
            --font-display: 'Cormorant Garamond', serif;
            --font-body: 'Outfit', sans-serif;
            
            /* Spacing & Layout */
            --container-padding: clamp(1.5rem, 5vw, 4rem);
            --header-height: 80px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--color-bg);
            color: var(--color-text);
            font-family: var(--font-body);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            overflow-x: hidden;
            cursor: none;
        }}

        /* Noise Overlay */
        .noise-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none;
            z-index: 9999;
            opacity: 0.03;
            background: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
        }}

        /* Custom Cursor */
        .custom-cursor {{
            position: fixed;
            top: 0; left: 0;
            width: 12px; height: 12px;
            background-color: var(--color-primary);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transform: translate(-50%, -50%);
            transition: width 0.3s cubic-bezier(0.25, 1, 0.5, 1), height 0.3s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.3s ease, background-color 0.3s ease;
            mix-blend-mode: multiply;
        }}
        .custom-cursor.hovering {{
            width: 40px; height: 40px;
            opacity: 0.5;
            background-color: var(--color-accent);
        }}

        /* Typography Styles (Matching Design System scaling) */
        h1, .h1 {{ font-family: var(--font-display); font-weight: 300; line-height: 1.1; letter-spacing: -0.02em; font-size: clamp(3rem, 7vw, 6.5rem); }}
        h2, .h2 {{ font-family: var(--font-display); font-weight: 300; line-height: 1.2; letter-spacing: -0.01em; font-size: clamp(2rem, 4vw, 3.5rem); }}
        p {{ font-weight: 300; line-height: 1.6; font-size: clamp(1rem, 1.2vw, 1.125rem); color: var(--color-text-light); }}
        
        .italic-accent {{ font-style: italic; font-weight: 400; color: var(--color-primary); }}

        /* Container */
        .container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 0 var(--container-padding);
        }}

        /* Navbar */
        .navbar {{
            position: fixed;
            top: 0; left: 0; right: 0;
            height: var(--header-height);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 var(--container-padding);
            z-index: 100;
            transition: background 0.4s ease, backdrop-filter 0.4s ease;
        }}
        .navbar.scrolled {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--color-bg-alt2);
        }}

        .brand-logo {{
            display: flex;
            align-items: center;
            height: 48px;
            z-index: 101;
            position: relative;
        }}
        .brand-logo svg {{
            height: 100%;
            width: auto;
            max-width: 200px;
            display: block;
        }}

        .nav-links {{
            display: flex;
            gap: 2.5rem;
            align-items: center;
        }}
        @media (max-width: 1024px) {{
            .nav-links {{ display: none; }}
        }}

        .nav-link {{
            text-decoration: none;
            color: var(--color-text);
            font-weight: 500;
            font-size: 0.95rem;
            position: relative;
            padding: 0.5rem 0;
            overflow: hidden;
        }}
        .nav-link::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0;
            width: 100%; height: 1px;
            background-color: var(--color-primary);
            transform: scaleX(0);
            transform-origin: right;
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .nav-link:hover::after {{
            transform: scaleX(1);
            transform-origin: left;
        }}

        /* Buttons */
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.875rem 2rem;
            border-radius: 999px;
            font-family: var(--font-body);
            font-weight: 500;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            border: none;
            cursor: pointer;
            z-index: 1;
        }}
        .btn-primary {{
            background-color: var(--color-primary);
            color: #fff;
            box-shadow: 0 4px 14px rgba(62, 137, 163, 0.15);
        }}
        .btn-primary::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(120deg, transparent, rgba(255,255,255,0.2), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
            z-index: -1;
        }}
        .btn-primary:hover {{
            background-color: var(--color-primary-alt);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(62, 137, 163, 0.25);
        }}
        .btn-primary:hover::before {{
            transform: translateX(100%);
        }}

        .btn-secondary {{
            background-color: transparent;
            color: var(--color-primary);
            border: 1px solid var(--color-primary);
        }}
        .btn-secondary::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: var(--color-bg-alt2);
            transform: scaleY(0);
            transform-origin: bottom;
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: -1;
        }}
        .btn-secondary:hover {{
            color: var(--color-primary);
            border-color: var(--color-primary-alt);
            transform: translateY(-2px);
        }}
        .btn-secondary:hover::before {{
            transform: scaleY(1);
            transform-origin: top;
        }}

        .btn-nav {{
            padding: 0.6rem 1.5rem;
            font-size: 0.9rem;
        }}

        /* Hamburger Menu */
        .menu-btn {{
            display: none;
            background: none;
            border: none;
            cursor: pointer;
            width: 44px;
            height: 44px;
            position: relative;
            z-index: 101;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 6px;
        }}
        .menu-btn span {{
            display: block;
            width: 24px;
            height: 1.5px;
            background-color: var(--color-text);
            transition: transform 0.3s, opacity 0.3s;
        }}
        @media (max-width: 1024px) {{
            .menu-btn {{ display: flex; }}
            .nav-actions {{ display: none; }}
        }}

        /* Hero Section */
        .hero {{
            position: relative;
            min-height: 100vh;
            display: grid;
            grid-template-columns: 1fr 1fr;
            align-items: center;
            overflow: hidden;
            padding-top: var(--header-height);
        }}
        
        @media (max-width: 1024px) {{
            .hero {{
                grid-template-columns: 1fr;
                grid-template-rows: 1fr 1fr;
                padding-top: calc(var(--header-height) + 2rem);
            }}
        }}

        /* Bg Decor */
        .hero-bg-decor {{
            position: absolute;
            top: -20%; left: -10%;
            width: 60vw; height: 60vw;
            background: radial-gradient(circle, var(--color-bg-alt) 0%, transparent 70%);
            border-radius: 50%;
            opacity: 0.6;
            filter: blur(80px);
            z-index: 0;
            pointer-events: none;
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            padding-left: var(--container-padding);
            padding-right: 2rem;
        }}
        @media (max-width: 1024px) {{
            .hero-content {{
                padding-right: var(--container-padding);
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: var(--color-bg-warm);
            border: 1px solid var(--color-bg-alt);
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--color-primary);
            margin-bottom: 2rem;
            opacity: 0;
            transform: translateY(20px);
        }}
        .hero-badge-dot {{
            width: 6px; height: 6px;
            background-color: var(--color-accent);
            border-radius: 50%;
            animation: pulse-dot 2s infinite ease-in-out;
        }}
        @keyframes pulse-dot {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.5); opacity: 0.5; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        .hero-title {{
            margin-bottom: 1.5rem;
            max-width: 800px;
        }}
        .hero-title .word {{
            overflow: hidden;
            display: inline-block;
        }}
        .hero-title .word .char {{
            display: inline-block;
            transform: translateY(100%);
            will-change: transform;
        }}

        .hero-desc {{
            margin-bottom: 3rem;
            max-width: 540px;
            font-size: 1.125rem;
            opacity: 0;
            transform: translateY(20px);
        }}

        .hero-ctas {{
            display: flex;
            gap: 1rem;
            margin-bottom: 4rem;
            opacity: 0;
            transform: translateY(20px);
        }}
        @media (max-width: 768px) {{
            .hero-ctas {{
                flex-direction: column;
                width: 100%;
                max-width: 320px;
            }}
        }}

        .hero-stats {{
            display: flex;
            gap: 3rem;
            border-top: 1px solid var(--color-bg-alt2);
            padding-top: 2rem;
            opacity: 0;
            transform: translateY(20px);
        }}
        .stat-item {{ display: flex; flex-direction: column; gap: 0.25rem; }}
        .stat-num {{ font-family: var(--font-display); font-size: 2.5rem; color: var(--color-text); line-height: 1; }}
        .stat-label {{ font-size: 0.875rem; color: var(--color-text-light); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500; }}

        /* Visual Element - Option C: Generative Organic Shapes */
        .hero-visual {{
            position: relative;
            height: 100%;
            min-height: 500px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1;
        }}
        @media (max-width: 1024px) {{
            .hero-visual {{
                min-height: 400px;
                order: -1;
            }}
        }}

        .blob-container {{
            position: absolute;
            width: 120%;
            height: 120%;
            left: -10%;
            top: -10%;
            filter: blur(40px);
            opacity: 0.8;
            will-change: transform;
        }}
        
        .blob {{
            position: absolute;
            border-radius: 50%;
            mix-blend-mode: multiply;
            animation: breathe 12s infinite alternate cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .blob-1 {{
            top: 10%; left: 20%;
            width: 60%; height: 60%;
            background: var(--color-accent-alt);
            animation-delay: 0s;
        }}
        
        .blob-2 {{
            top: 30%; right: 10%;
            width: 50%; height: 50%;
            background: var(--color-accent);
            opacity: 0.7;
            animation-delay: -3s;
            animation-duration: 15s;
        }}
        
        .blob-3 {{
            bottom: 10%; left: 30%;
            width: 55%; height: 55%;
            background: var(--color-primary-alt);
            opacity: 0.4;
            animation-delay: -6s;
            animation-duration: 18s;
        }}

        @keyframes breathe {{
            0% {{ transform: translate(0, 0) scale(1); }}
            100% {{ transform: translate(10%, 10%) scale(1.1); }}
        }}

        /* Scroll Indicator */
        .scroll-indicator {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
            color: var(--color-text-light);
            font-size: 0.8rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            z-index: 10;
            opacity: 0;
        }}
        .scroll-line {{
            width: 1px;
            height: 40px;
            background: rgba(45, 96, 122, 0.2);
            position: relative;
            overflow: hidden;
            display: block;
        }}
        .scroll-line::after {{
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 50%;
            background: var(--color-primary);
            animation: scrollDown 2s cubic-bezier(0.77, 0, 0.175, 1) infinite;
        }}

        @keyframes scrollDown {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(200%); }}
        }}

    </style>
</head>
<body>

    <div class="noise-overlay"></div>
    <div class="custom-cursor" id="custom-cursor"></div>

    <header class="navbar" id="navbar">
        <a href="#" class="brand-logo" aria-label="Instituto Clio Home">
            {svg_content}
        </a>

        <nav class="nav-links" role="navigation" aria-label="Navegação Principal">
            <a href="#" class="nav-link interactive">Sobre o Instituto</a>
            <a href="#" class="nav-link interactive">Pesquisa & Memória</a>
            <a href="#" class="nav-link interactive">Soluções Tecnológicas</a>
            <a href="#" class="nav-link interactive">Impacto Social</a>
        </nav>

        <div class="nav-actions">
            <a href="#" class="btn btn-primary btn-nav interactive">Conecte-se</a>
        </div>

        <button class="menu-btn interactive" aria-label="Abrir menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </header>

    <main>
        <section class="hero" aria-label="hero">
            <div class="hero-bg-decor" data-parallax data-speed="0.6"></div>
            
            <div class="hero-content">
                <div class="hero-badge hover-lift">
                    <div class="hero-badge-dot"></div>
                    <span>Tecnologia a favor da história</span>
                </div>

                <h1 class="hero-title h1" data-splitting>Inteligência que preserva.<br><span class="italic-accent">Tecnologia que transforma.</span></h1>
                
                <p class="hero-desc">
                    Democratizamos o acesso à memória histórico-cultural conectando pesquisa científica, inovação tecnológica e impacto social sustentável.
                </p>

                <div class="hero-ctas">
                    <a href="#" class="btn btn-primary interactive">Conheça Nossas Ações</a>
                    <a href="#" class="btn btn-secondary interactive">Nossa Metodologia</a>
                </div>

                <div class="hero-stats">
                    <div class="stat-item">
                        <span class="stat-num">1M+</span>
                        <span class="stat-label">Acervos Digitais</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-num">40+</span>
                        <span class="stat-label">Instituições Parceiras</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-num">100%</span>
                        <span class="stat-label">Acesso Aberto</span>
                    </div>
                </div>
            </div>

            <div class="hero-visual" data-parallax data-speed="0.3">
                <div class="blob-container" id="blob-container">
                    <div class="blob blob-1"></div>
                    <div class="blob blob-2"></div>
                    <div class="blob blob-3"></div>
                </div>
            </div>

            <div class="scroll-indicator" id="scroll-indicator">
                <span>Scroll</span>
                <div class="scroll-line"></div>
            </div>
        </section>
        
        <!-- Mock section to allow scrolling to test Lenis and ScrollTrigger -->
        <section style="height: 100vh; background: var(--color-bg-warm); padding: var(--container-padding); display:flex; align-items:center; justify-content:center;">
             <h2 class="h2" style="color: var(--color-primary);" data-parallax data-speed="0.2">Preservando o futuro.</h2>
        </section>
    </main>

    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/splitting/dist/splitting.min.js"></script>
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>

    <script>
        document.addEventListener("DOMContentLoaded", () => {{
            // 1. Initialize Lenis Smooth Scroll
            const lenis = new Lenis({{
                duration: 1.2,
                easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
                direction: 'vertical',
                gestureDirection: 'vertical',
                smooth: true,
                mouseMultiplier: 1,
                smoothTouch: false,
                touchMultiplier: 2,
                infinite: false,
            }});

            function raf(time) {{
                lenis.raf(time);
                requestAnimationFrame(raf);
            }}
            requestAnimationFrame(raf);

            // Connect Lenis with GSAP ScrollTrigger
            lenis.on('scroll', ScrollTrigger.update);
            gsap.ticker.add((time) => {{
                lenis.raf(time * 1000);
            }});
            gsap.ticker.lagSmoothing(0);

            // 2. Initialize Custom Cursor
            const cursor = document.getElementById('custom-cursor');
            const hoverTargets = document.querySelectorAll('a, button, .interactive');
            
            let mouseX = window.innerWidth / 2;
            let mouseY = window.innerHeight / 2;
            let cursorX = mouseX;
            let cursorY = mouseY;
            
            // Allow cursor to be toggled by user preference
            const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            
            if(!mediaQuery.matches) {{
                window.addEventListener('mousemove', (e) => {{
                    mouseX = e.clientX;
                    mouseY = e.clientY;
                }});

                function updateCursor() {{
                    const dx = mouseX - cursorX;
                    const dy = mouseY - cursorY;
                    cursorX += dx * 0.15; // easing
                    cursorY += dy * 0.15;
                    
                    cursor.style.transform = `translate(${{cursorX}}px, ${{cursorY}}px)`;
                    requestAnimationFrame(updateCursor);
                }}
                updateCursor();

                hoverTargets.forEach(target => {{
                    target.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
                    target.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
                }});
            }} else {{
                cursor.style.display = 'none';
                document.body.style.cursor = 'auto';
            }}

            // 3. Navbar scroll effect
            const navbar = document.getElementById('navbar');
            window.addEventListener('scroll', () => {{
                if (window.scrollY > 50) {{
                    navbar.classList.add('scrolled');
                }} else {{
                    navbar.classList.remove('scrolled');
                }}
            }});

            // 4. Blob Mouse Interaction (Subtle Parallax)
            const blobContainer = document.getElementById('blob-container');
            if(!mediaQuery.matches) {{
                window.addEventListener('mousemove', (e) => {{
                    const x = (e.clientX / window.innerWidth - 0.5) * 30;
                    const y = (e.clientY / window.innerHeight - 0.5) * 30;
                    gsap.to(blobContainer, {{
                        x: x,
                        y: y,
                        duration: 2,
                        ease: "power2.out"
                    }});
                }});
            }}

            // 5. GSAP Entrance Animations
            gsap.registerPlugin(ScrollTrigger);
            Splitting({{ target: "[data-splitting]", by: "chars" }});

            const tl = gsap.timeline({{ 
                defaults: {{ ease: "power4.out" }}
            }});

            if(!mediaQuery.matches) {{
                // Navbar
                tl.from(".navbar", {{
                    y: -100,
                    opacity: 0,
                    duration: 1.2,
                    delay: 0.1
                }})
                // Badge
                .to(".hero-badge", {{
                    y: 0,
                    opacity: 1,
                    duration: 1
                }}, "-=0.6")
                // Headline Text Reveal
                .to(".hero-title .char", {{
                    y: "0%",
                    duration: 1.2,
                    stagger: 0.02,
                    ease: "power3.out"
                }}, "-=0.8")
                // Subheadline
                .to(".hero-desc", {{
                    y: 0,
                    opacity: 1,
                    duration: 1
                }}, "-=0.8")
                // CTAs
                .to(".hero-ctas", {{
                    y: 0,
                    opacity: 1,
                    duration: 1
                }}, "-=0.9")
                // Stats
                .to(".hero-stats", {{
                    y: 0,
                    opacity: 1,
                    duration: 1
                }}, "-=0.8")
                // Visual Blobs
                .from(".blob", {{
                    scale: 0.4,
                    opacity: 0,
                    duration: 2.5,
                    stagger: 0.2,
                    ease: "power2.out"
                }}, "-=2")
                // Scroll Indicator
                .to("#scroll-indicator", {{
                    opacity: 1,
                    duration: 1
                }}, "-=1");
            }} else {{
                // Reduced motion fallback
                gsap.set([".hero-badge", ".hero-title .char", ".hero-desc", ".hero-ctas", ".hero-stats", "#scroll-indicator"], {{
                    opacity: 1, y: 0, transform: "none"
                }});
                gsap.set(".blob", {{ scale: 1, opacity: 1 }});
            }}

            // 6. Scroll Parallax effects
            if(!mediaQuery.matches) {{
                const parallaxElements = document.querySelectorAll('[data-parallax]');
                parallaxElements.forEach(el => {{
                    const speed = el.getAttribute('data-speed') || 0.3;
                    gsap.to(el, {{
                        y: () => -(window.innerHeight * speed),
                        ease: "none",
                        scrollTrigger: {{
                            trigger: ".hero",
                            start: "top top",
                            end: "bottom top",
                            scrub: true
                        }}
                    }});
                }});

                // Headline subtle move on scroll
                gsap.to(".hero-content", {{
                    y: -100,
                    opacity: 0.3,
                    ease: "none",
                    scrollTrigger: {{
                        trigger: ".hero",
                        start: "top top",
                        end: "bottom top",
                        scrub: true
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
'''

output_path = r'c:\Users\Matheus Gabriel\Desktop\Instituto Clio\lumina-digital.aura.build\index99.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print('File index99.html successfully created.')
