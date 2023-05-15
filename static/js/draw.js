var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

var painting = document.getElementById('canvas');
var paint_style = getComputedStyle(painting);
canvas.width = parseInt(paint_style.getPropertyValue('width'));
canvas.height = parseInt(paint_style.getPropertyValue('height'));

var mouse = {x: 0, y: 0};

var drawing = false;

var dhistory = [];
var dhistoryIndex = 0;

canvas.addEventListener('mousedown', function(e) {
  drawing = true;
  ctx.beginPath();
  ctx.moveTo(mouse.x, mouse.y);
}, false);

canvas.addEventListener('mouseup', function() {
  drawing = false;
  dhistory.push(canvas.toDataURL()); // Save state to dhistory.
}, false);

canvas.addEventListener('mousemove', function(e) {
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;

  if (drawing) {
    ctx.lineTo(mouse.x, mouse.y);
    ctx.stroke();
  }
}, false);

document.getElementById('save').addEventListener('click', function() {
  var dataURL = canvas.toDataURL('image/png');
  $.post("/save", { data: dataURL }, function(res) {
    console.log(res);
  });
});

document.getElementById('undo').addEventListener('click', function() {
  if (dhistory.length > 1) {
    dhistory.pop(); // Remove current state.
    dhistoryIndex = dhistory.length - 1; // Go to the previous state.
    var imgData = dhistory[dhistoryIndex];
    var img = new Image();
    img.src = imgData;
    img.onload = function () {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
    };
  }
});
