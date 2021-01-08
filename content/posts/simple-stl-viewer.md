---
title: "A Simple STL Viewer with Three.js"
date: 2019-04-14
tags: ["Programming", "3D Models", "Web Dev"]
plugins: ["threejs", "stlviewer"]
#downloads: ["stlviewer.tar.gz"]
description: "Implementing a simple WebGL viewer for STL files using Three.JS."
---

Here's a simple part that I made in Fusion 360:
<div class="stlviewer" data-src="/objects/keystone/keystone.stl" data-rotate="x" data-zdistance="2"></div>

It's a <a href="/objects/keystone/">simple bracket</a> to mount keystone jacks to a wall. This article isn't about that, it's about the viewer used to display it above.  It uses WebGL to render it in your browser, and the three.js library makes it easy to implement.  It's part of my [hugo](https://gohugo.io/) template now, since I'd like to post some of the objects that I make for 3D printing.

Here's the code for the initial version, in roughly literate programming style.

### Getting Started

First, include the three.js libraries that we'll be using.  We'll need to get these from the [three.js repository](https://github.com/mrdoob/three.js/).  We'll be using [three.js itself](https://github.com/mrdoob/three.js/blob/dev/build/three.min.js), the [STL Loader plugin](https://github.com/mrdoob/three.js/blob/dev/examples/js/loaders/STLLoader.js), and the [Orbit Controls plugin](https://github.com/mrdoob/three.js/blob/dev/examples/js/controls/OrbitControls.js), so you can drag it around.

{{< highlight html>}}
<script src="/build/three.min.js"></script>
<script src="/examples/js/loaders/STLLoader.js"></script>
<script src="/examples/js/controls/OrbitControls.js"></script>
{{< / highlight >}}

We'll create a div for our viewer as well.
{{< highlight html>}}
<div id="model" style="width: 500px; height: 500px"> </div>
{{< / highlight >}}

### Setting up Three.js

Now we can actually start writing JavaScript.  We'll be defining a simple function to act as the STL viewer, given the path to the STL file, and the ID of the element that it takes.

{{< highlight js>}}
function STLViewer(model, elementID) {
    var elem = document.getElementById(elementID)
{{< / highlight >}}

Then, we create the camera using three.js.  We use information about the element's size to determine the aspect ratio, and we use arguments 1 and 1000 to indicate that the camera should clip things closer than 1 unit away and further than 1000 units away.

{{< highlight js>}}
var camera = new THREE.PerspectiveCamera(70, 
    elem.clientWidth/elem.clientHeight, 1, 1000);
{{< / highlight >}}

Now, we can create the renderer object.  I set alpha to true, so that it would have no background, and just use the page's background.  We also set the size of the renderer to the element's size, and add the renderer's object to our element with addChild.

{{< highlight js>}}
var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(elem.clientWidth, elem.clientHeight);
elem.appendChild(renderer.domElement);
{{< / highlight >}}

We want it to be able to handle the page being resized, since this blog is designed to be responsive, so we add an event listener that resets the renderer's size as needed.

{{< highlight js>}}
window.addEventListener('resize', function () {
    renderer.setSize(elem.clientWidth, elem.clientHeight);
    camera.aspect = elem.clientWidth/elem.clientHeight;
    camera.updateProjectionMatrix();
}, false);
{{< / highlight >}}

Next, we'll configure the controls using OrbitControls.

{{< highlight js>}}
var controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.rotateSpeed = 0.05;
controls.dampingFactor = 0.1;
controls.enableZoom = true;
controls.autoRotate = true;
controls.autoRotateSpeed = .75;
{{< / highlight >}}

### Setting the Scene

Finally, we can start to set the scene.  We'll start with some simple lighting - in this case, a hemisphere light from above.  It won't light the bottom of the model, but it is easy enough to add additional lights here if that is an issue.

{{< highlight js>}}
var scene = new THREE.Scene();
scene.add(new THREE.HemisphereLight(0xffffff, 1.5));
{{< / highlight >}}

Next, we can load our STL file using three.js's STL loader.  The loader only returns a geometry, so we also need to generate a material for it - in this case, it is a somewhat shiny orange, since I like to 3D print in orange PLA.

{{< highlight js>}}
(new THREE.STLLoader()).load(model, function (geometry) {
    var material = new THREE.MeshPhongMaterial({ 
        color: 0xff5533, 
        specular: 100, 
        shininess: 100 });
    var mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
{{< / highlight >}}

### Placing the Model

Now our mesh is loaded, but we need to figure out a way to center it.  I used three.js's computeBoundingBox and getCenter helper functions to find the center of the mesh's bounding box, and then just translated it's position there:

{{< highlight js>}}
var middle = new THREE.Vector3();
geometry.computeBoundingBox();
geometry.boundingBox.getCenter(middle);
mesh.geometry.applyMatrix(new THREE.Matrix4().makeTranslation( 
                              -middle.x, -middle.y, -middle.z ) );
{{< / highlight >}}

We also want to pull the camera away so that it is a reasonable size.  Again I used the element's bounding box, picked the largest dimension, and pulled the camera away by 1.5 times that.  This may not be ideal, but it seems to work well enough so far.

{{< highlight js>}}
var largestDimension = Math.max(geometry.boundingBox.max.x,
                            geometry.boundingBox.max.y, 
                            geometry.boundingBox.max.z)
camera.position.z = largestDimension * 1.5;
{{< / highlight >}}

Now we animate it, by creating a callback function (in our closure) for three.js to repeatedly call.  The callback function updates the scene (in this case, just calling the control's update function) and tells three.js to render it.

{{< highlight js>}}
var animate = function () {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}; 
{{< / highlight >}}

### Finishing Up

And, that's it!  We call our animate() function in our callback (since that is called once the STL file is loaded), finish up our callback, and finish up our function.

{{< highlight js>}}
    animate();
    });
}
{{< / highlight >}}

We can use our function to place the renderer in the div from earlier.

{{< highlight html>}}
<script type="text/javascript">
window.onload = function() {
    STLViewer("hook.stl", "model")
}
</script>
{{< / highlight >}}

Please note that this won't work as a local file, since it won't be able to load the stl file.  You'll need to start up a HTTP server. 

As a free bonus tip, you can serve the current directory over HTTP with python:

{{< highlight bash>}}
python2 -m SimpleHTTPServer
{{< / highlight >}}

<b>Updated</b>: 2020-05-25, to update the model shown and the way the model is centered
