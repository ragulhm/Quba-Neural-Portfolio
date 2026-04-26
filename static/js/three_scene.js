import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

class GlobeScene {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        // Scene setup
        this.scene = new THREE.Scene();
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(60, this.container.clientWidth / this.container.clientHeight, 0.1, 100);
        this.camera.position.z = 6;

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.container.appendChild(this.renderer.domElement);

        // Mouse tracking
        this.mouse = { x: 0, y: 0 };
        this.targetMouse = { x: 0, y: 0 };
        window.addEventListener('mousemove', (e) => {
            this.targetMouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            this.targetMouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
        });

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        this.scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0xE0AAFF, 0.8);
        pointLight1.position.set(-5, 5, 5);
        this.scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0x9D4EDD, 0.6);
        pointLight2.position.set(5, -5, 5);
        this.scene.add(pointLight2);

        // 1. The Core Orb (Icosahedron)
        const orbGeom = new THREE.IcosahedronGeometry(1.5, 1);
        const orbMat = new THREE.MeshStandardMaterial({
            color: 0x7B2CBF,
            roughness: 0.1,
            metalness: 0.8,
            emissive: 0x3c096c,
            emissiveIntensity: 0.4,
            flatShading: true
        });
        this.orb = new THREE.Mesh(orbGeom, orbMat);

        // 2. The Holographic Wireframe
        const wireGeom = new THREE.IcosahedronGeometry(1.52, 1);
        const wireMat = new THREE.MeshBasicMaterial({
            color: 0xC77DFF,
            wireframe: true,
            transparent: true,
            opacity: 0.2
        });
        this.wireframe = new THREE.Mesh(wireGeom, wireMat);
        this.orb.add(this.wireframe);

        // 3. Particle Nebula
        const particleCount = 1500;
        const particleGeom = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount; i++) {
            const r = 3 + Math.random() * 3;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            
            positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
            positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
            positions[i * 3 + 2] = r * Math.cos(phi);
        }
        
        particleGeom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const particleMat = new THREE.PointsMaterial({
            color: 0xE0AAFF,
            size: 0.015,
            transparent: true,
            opacity: 0.5,
            sizeAttenuation: true
        });
        this.particles = new THREE.Points(particleGeom, particleMat);

        // 4. Glow Atmosphere
        const glowGeom = new THREE.SphereGeometry(1.5, 32, 32);
        const glowMat = new THREE.MeshBasicMaterial({
            color: 0x9D4EDD,
            transparent: true,
            opacity: 0.05
        });
        this.glow = new THREE.Mesh(glowGeom, glowMat);
        this.glow.scale.set(1.4, 1.4, 1.4);

        // Grouping
        this.group = new THREE.Group();
        this.group.add(this.orb);
        this.group.add(this.particles);
        this.group.add(this.glow);
        this.scene.add(this.group);

        // Resize handler
        window.addEventListener('resize', this.onWindowResize.bind(this));

        // Start animation loop
        this.clock = new THREE.Clock();
        this.animate();
    }

    onWindowResize() {
        if (!this.container || !this.camera || !this.renderer) return;
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));

        const t = this.clock.getElapsedTime();

        // Smooth mouse parallax
        this.mouse.x += (this.targetMouse.x - this.mouse.x) * 0.05;
        this.mouse.y += (this.targetMouse.y - this.mouse.y) * 0.05;

        // Rotate orb and wireframe
        if (this.orb) {
            this.orb.rotation.y = t * 0.15;
            this.orb.rotation.z = t * 0.1;
            
            // Mouse influence
            this.orb.rotation.x = this.mouse.y * 0.5;
            this.orb.rotation.y += this.mouse.x * 0.5;
        }

        if (this.wireframe) {
            this.wireframe.rotation.y = -t * 0.2;
        }

        // Rotate particles
        if (this.particles) {
            this.particles.rotation.y = t * 0.05;
            this.particles.rotation.x = t * 0.02;
        }

        // Pulse glow and particles opacity
        if (this.glow) {
            this.glow.scale.setScalar(1.4 + Math.sin(t * 0.5) * 0.05);
        }

        // Float entire group
        if (this.group) {
            this.group.position.y = Math.sin(t * 0.5) * 0.15;
            this.group.position.x = Math.cos(t * 0.3) * 0.1;
        }

        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new GlobeScene('canvas-container');
});
