<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SAPTAK.exe — 3D Midnight Protocol</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html, body { width:100%; height:100%; overflow:hidden; background:#05070D; font-family: Consolas, monospace; }
    #c { display:block; width:100%; height:100%; }
    .hud {
      position:fixed; left:20px; top:20px; z-index:10;
      color:#C9D4E5; background:rgba(5,7,13,.7);
      border:1px solid #00F5FF; border-radius:12px; padding:16px 18px;
      box-shadow:0 0 20px rgba(0,245,255,.25); max-width:90vw;
    }
    .hud h1 { color:#00F5FF; font-size:28px; margin-bottom:6px; text-shadow:0 0 10px #00F5FF; }
    .hud p { font-size:13px; line-height:1.5; }
    .mag { color:#FF2BD6; }
    .btn {
      display:inline-block; margin-top:10px; padding:8px 12px;
      border:1px solid #00F5FF; color:#00F5FF; text-decoration:none; border-radius:8px;
    }
  </style>
</head>
<body>
  <div class="hud">
    <h1>SAPTAK.exe</h1>
    <p>Saptak Chaki</p>
    <p>Python Full Stack Developer</p>
    <p class="mag">3D MIDNIGHT PROTOCOL // R34</p>
    <a class="btn" href="https://github.com/saptak-chaki" target="_blank">GitHub Profile</a>
  </div>
  <canvas id="c"></canvas>

  <script type="importmap">
  {
    "imports": {
      "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
      "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
    }
  }
  </script>

  <script type="module">
    import * as THREE from 'three';
    import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
    import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
    import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

    const canvas = document.getElementById('c');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias:true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
    renderer.setSize(innerWidth, innerHeight);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x05070D);
    scene.fog = new THREE.Fog(0x05070D, 12, 70);

    const camera = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, 0.1, 200);
    camera.position.set(4, 2, -8);

    scene.add(new THREE.AmbientLight(0x6688aa, 0.35));
    const moon = new THREE.DirectionalLight(0x88aaff, 0.6);
    moon.position.set(-10, 20, 10);
    scene.add(moon);

    // Road
    const road = new THREE.Mesh(
      new THREE.PlaneGeometry(14, 200),
      new THREE.MeshStandardMaterial({ color:0x0a0f18, metalness:0.6, roughness:0.4 })
    );
    road.rotation.x = -Math.PI/2;
    scene.add(road);

    // Center dashes
    const dashes = [];
    for (let i=0;i<20;i++){
      const d = new THREE.Mesh(
        new THREE.BoxGeometry(0.25,0.02,3),
        new THREE.MeshBasicMaterial({ color:0xC9D4E5 })
      );
      d.position.set(0,0.02, -i*8 + 20);
      scene.add(d); dashes.push(d);
    }

    // Side neon lamps
    const lamps = [];
    for (let i=0;i<12;i++){
      for (const side of [-1,1]){
        const g = new THREE.Group();
        const pole = new THREE.Mesh(
          new THREE.BoxGeometry(0.12,5,0.12),
          new THREE.MeshStandardMaterial({ color:0x1a2333 })
        );
        pole.position.y = 2.5;
        const light = new THREE.Mesh(
          new THREE.BoxGeometry(1.4,0.15,0.3),
          new THREE.MeshBasicMaterial({ color: side>0 ? 0x00F5FF : 0xFF2BD6 })
        );
        light.position.set(side*-0.6, 5, 0);
        g.add(pole, light);
        g.position.set(side*6.5, 0, -i*12 + 20);
        scene.add(g); lamps.push(g);
      }
    }

    // Buildings
    const buildings = [];
    for (let i=0;i<16;i++){
      for (const side of [-1,1]){
        const h = 8 + (i%5)*3;
        const b = new THREE.Mesh(
          new THREE.BoxGeometry(5, h, 5),
          new THREE.MeshStandardMaterial({
            color:0x0A1020,
            emissive: i%2?0x00F5FF:0xFF2BD6,
            emissiveIntensity:0.08
          })
        );
        b.position.set(side*(12+(i%3)), h/2, -i*10 + 30);
        scene.add(b); buildings.push(b);
      }
    }

    // Car group (R34-inspired simple 3D body + real motion)
    const car = new THREE.Group();
    const bodyMat = new THREE.MeshStandardMaterial({ color:0x9bb4d0, metalness:0.9, roughness:0.25 });
    const darkMat = new THREE.MeshStandardMaterial({ color:0x0b1018, metalness:0.8, roughness:0.3 });

    const chassis = new THREE.Mesh(new THREE.BoxGeometry(1.9,0.45,4.4), bodyMat);
    chassis.position.y = 0.55;
    const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.55,0.4,2.1), darkMat);
    cabin.position.set(0,0.95,0.2);
    const wing = new THREE.Mesh(new THREE.BoxGeometry(1.7,0.06,0.5), darkMat);
    wing.position.set(0,1.25,1.9);

    // lights
    const headL = new THREE.Mesh(new THREE.BoxGeometry(0.35,0.14,0.06), new THREE.MeshBasicMaterial({color:0xE8FFFF}));
    const headR = headL.clone();
    headL.position.set(-0.6,0.6,-2.2);
    headR.position.set(0.6,0.6,-2.2);
    const tail = new THREE.Mesh(new THREE.BoxGeometry(1.5,0.1,0.05), new THREE.MeshBasicMaterial({color:0xFF2BD6}));
    tail.position.set(0,0.65,2.2);

    car.add(chassis, cabin, wing, headL, headR, tail);

    // wheels
    const wheels = [];
    const wgeo = new THREE.CylinderGeometry(0.38,0.38,0.28,20);
    const wmat = new THREE.MeshStandardMaterial({ color:0x111111, roughness:0.9 });
    [[-0.95,0.38,-1.4],[0.95,0.38,-1.4],[-0.95,0.38,1.4],[0.95,0.38,1.4]].forEach((p)=>{
      const w = new THREE.Mesh(wgeo, wmat);
      w.rotation.z = Math.PI/2;
      w.position.set(...p);
      car.add(w); wheels.push(w);
    });

    // light beams
    car.add(new THREE.PointLight(0xBFFFFF, 60, 28, 2).translateZ(-4).translateY(0.8));
    car.add(new THREE.PointLight(0xFF2BD6, 20, 10, 2).translateZ(3).translateY(0.8));
    car.add(new THREE.PointLight(0x00F5FF, 12, 7, 2).translateY(0.1));
    car.position.set(0,0,0);
    scene.add(car);

    // camera shots
    const shots = [
      { p:new THREE.Vector3(3.8,1.4,-7.5), t:new THREE.Vector3(0,0.8,0) },
      { p:new THREE.Vector3(6.5,1.2,0.5), t:new THREE.Vector3(0,0.8,0) },
      { p:new THREE.Vector3(0.2,2.0,7.5), t:new THREE.Vector3(0,0.9,-2) },
      { p:new THREE.Vector3(-9,4.5,-12), t:new THREE.Vector3(0,0.6,-1) },
    ];
    const look = new THREE.Vector3();

    // bloom
    const composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    composer.addPass(new UnrealBloomPass(new THREE.Vector2(innerWidth,innerHeight), 0.85, 0.8, 0.7));

    const speed = 26;
    const clock = new THREE.Clock();
    function scroll(obj, span=120){
      obj.position.z += speed * 0.016;
      if (obj.position.z > 35) obj.position.z -= span;
    }

    function animate(){
      requestAnimationFrame(animate);
      const t = clock.getElapsedTime();
      const dt = 0.016;

      // world moves toward camera = car driving feel
      dashes.forEach(d=>{ d.position.z += speed*dt; if(d.position.z>30)d.position.z-=160; });
      lamps.forEach(l=>{ l.position.z += speed*dt; if(l.position.z>30)l.position.z-=144; });
      buildings.forEach(b=>{ b.position.z += speed*dt; if(b.position.z>40)b.position.z-=160; });

      // wheels rotate + engine vibration
      wheels.forEach(w=> w.rotation.x -= dt * speed / 0.38);
      car.position.y = Math.sin(t*55)*0.012;

      // camera transitions every 6s
      const shot = shots[Math.floor(t/6)%shots.length];
      camera.position.lerp(shot.p, 0.03);
      look.lerp(shot.t, 0.03);
      camera.lookAt(look);

      composer.render();
    }
    animate();

    addEventListener('resize', ()=>{
      camera.aspect = innerWidth/innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
      composer.setSize(innerWidth, innerHeight);
    });
  </script>
</body>
</html>
