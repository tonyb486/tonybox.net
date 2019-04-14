
function STLViewer(model, elementID) {
    elem = document.getElementById(elementID)

    camera = new THREE.PerspectiveCamera(70, elem.clientWidth / elem.clientHeight, 1, 1000);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(elem.clientWidth, elem.clientHeight);
    elem.appendChild(renderer.domElement);

    window.addEventListener('resize', function () {
        renderer.setSize(elem.clientWidth, elem.clientHeight);
        camera.aspect = elem.clientWidth / elem.clientHeight;
        camera.updateProjectionMatrix();
    }, false);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.enableZoom = true;
    controls.autoRotate = true;

    scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xffffff, 1.5));

    (new THREE.STLLoader()).load(model, function (geometry) {
        material = new THREE.MeshPhongMaterial({ color: 0xff5533, specular: 100, shininess: 100 });
        mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // Compute the middle
        middle = new THREE.Vector3();
        geometry.computeBoundingBox();
        geometry.boundingBox.getCenter(middle);

        // Center it
        mesh.position.x = -1 * middle.x;
        mesh.position.y = -1 * middle.y;
        mesh.position.z = -1 * middle.z;

        // Pull the camera away as needed
        largestDimension = Math.max(geometry.boundingBox.max.x,
            geometry.boundingBox.max.y, geometry.boundingBox.max.z)
        camera.position.z = largestDimension * 1.5;

        animate = function () {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }; animate();
    });
}
