// static/js/particles.js
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.js';

let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
camera.position.z = 5;

let renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Particles
let particles = new THREE.BufferGeometry();
let particleCount = 1000;
let positions = [];

for (let i = 0; i < particleCount; i++) {
    positions.push((Math.random() - 0.5) * 10);
    positions.push((Math.random() - 0.5) * 10);
    positions.push((Math.random() - 0.5) * 10);
}

particles.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

let material = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.05,
    transparent: true
});

let pointCloud = new THREE.Points(particles, material);
scene.add(pointCloud);

// Animation
function animate() {
    requestAnimationFrame(animate);
    pointCloud.rotation.y += 0.0015;
    pointCloud.rotation.x += 0.001;
    renderer.render(scene, camera);
}

animate();

// Responsive
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
