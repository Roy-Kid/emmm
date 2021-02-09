import * as THREE from './build/three.module.js';
import {OrbitControls} from './build/OrbitControls.js';
import {GUI} from './build/dat.gui.module.js';
import { get_universe, get_atoms } from "./build/dataInterface.js";

function main() {
    // hold canvas
  const canvas = document.querySelector('#c');

  // init WebGLRenderer
  const renderer = new THREE.WebGLRenderer({canvas});

  const universeRaw = get_universe();

// init camera and controller 
  const fov = 45;
  const aspect = 2;  // the canvas default
  const near = 1;
  const far = 500;
  const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
  camera.position.set(
    universeRaw.xhi * 1.5,
    universeRaw.yhi*1.5,
    universeRaw.zhi*1.5
  );
  camera.up.set(0,0,1);


  class MinMaxGUIHelper {
    constructor(obj, minProp, maxProp, minDif) {
      this.obj = obj;
      this.minProp = minProp;
      this.maxProp = maxProp;
      this.minDif = minDif;
    }
    get min() {
      return this.obj[this.minProp];
    }
    set min(v) {
      this.obj[this.minProp] = v;
      this.obj[this.maxProp] = Math.max(this.obj[this.maxProp], v + this.minDif);
    }
    get max() {
      return this.obj[this.maxProp];
    }
    set max(v) {
      this.obj[this.maxProp] = v;
      this.min = this.min;  // this will call the min setter
    }
  }

  function updateCamera() {
    camera.updateProjectionMatrix();
  }

  const gui = new GUI();
  gui.add(camera, 'fov', 1, 180).onChange(updateCamera);
  const minMaxGUIHelper = new MinMaxGUIHelper(camera, 'near', 'far', 0.1);
  gui.add(minMaxGUIHelper, 'min', 0.1, 50, 0.1).name('near').onChange(updateCamera);
  gui.add(minMaxGUIHelper, 'max', 0.1, 1000, 0.1).name('far').onChange(updateCamera);


  const controller = new OrbitControls(camera, canvas);
  controller.target.set(0, 0, 0);
  controller.update();


  // init scene
  const scene = new THREE.Scene();

  // init light
  {
    const color = 0xFFFFFF;
    const intensity = 0.5;
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.set(0, 10, 0);
    light.target.position.set(-5, 0, 0);
    scene.add(light);
    scene.add(light.target);


    const ambientlight = new THREE.AmbientLight(color, intensity);
    scene.add(ambientlight);
  }

  // init simulation cell

  const width = universeRaw.xhi - universeRaw.xlo;
  const height = universeRaw.yhi - universeRaw.ylo;
  const depth = universeRaw.zhi - universeRaw.zlo;
  const boxGeometry =  new THREE.BoxBufferGeometry(width, height, depth);
  const edge = new THREE.EdgesGeometry(boxGeometry);
  const line = new THREE.LineSegments(edge, new THREE.LineBasicMaterial({color: 0xffffff}));

  line.position.set(width/2, height/2, depth/2);
  
  const universe = new THREE.Object3D()
  universe.add(line);
  scene.add(universe);


  // add axisHelper
  // red: x; green: y; blue: z;
  {
    const axisHelper = new THREE.AxesHelper(3);
    scene.add(axisHelper);
  }

  // add gridHelper
  {
      const size = 10;
      const step = 10;

      const gridHelper = new THREE.GridHelper(size, step, 0xAAAAAA);
      scene.add(gridHelper);
  }

  // add atoms

  let atoms = get_atoms();
  let atomGeometries = [];
  for (let atom of atoms) {
    console.log(atom);
    const atomGeometry = new THREE.SphereGeometry(0.3);
    const material = new THREE.MeshPhongMaterial();
    const atomMesh = new THREE.Mesh(atomGeometry, material);
    atomMesh.position.set(atom.x, atom.y, atom.z);
    atomGeometries.push(atomMesh);
    scene.add(atomMesh);
  }

  // add bonds

  let bonds = get_bonds();
  let bondGeometries = [];
  


  // render section
  function resizeRendererToDisplaySize(renderer) {
    const canvas = renderer.domElement;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    const needResize = canvas.width !== width || canvas.height !== height;
    if (needResize) {
      renderer.setSize(width, height, false);
    }
    return needResize;
  }

  function render(time) {
    time *= 0.001;

    if (resizeRendererToDisplaySize(renderer)) {
      const canvas = renderer.domElement;
      camera.aspect = canvas.clientWidth / canvas.clientHeight;
      camera.updateProjectionMatrix();
    }


    renderer.render(scene, camera);

    requestAnimationFrame(render);

  }

  requestAnimationFrame(render);
}

main();