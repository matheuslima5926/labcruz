console.log("JAvva");

var csrftoken = Cookies.get('csrftoken');
console.log(csrftoken);

function cancelAreaSelected() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
}

function confirmAreaSelected() {
    console.log("Confirming selected area !!!!")
    var initX = rect.startX
    var initY = rect.startY
    var areaWidth = rect.w
    var areaHeight = rect.h
    var animal = $('#dropdown_animal').val()
    // alert(animal);
    console.log(animal);
    $.ajax({
        type: "POST",
        url: "/getROI",
        data: {
            'initX': initX,
            'initY': initY,
            'areaWidth': areaWidth,
            'areaHeight': areaHeight,
            'animal_value': animal,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        dataType: 'json',
        success: function (data) {
        }
    });
}

function startTest() {
    $.ajax({
        type: "POST",
        url: "/analyse",
        data: {
            'startTest': "true",
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        dataType: 'json',
        success: function (data) {
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#fileInput").change( function(event) {
    var dale = event.target.files[0];
    $("#filecomponent").css("display", "block");
    $("#filepath_value").val(dale.name);
    } 
)



var canvas = document.getElementById('myCanvas');
if (canvas != null) {
    var ctx = canvas.getContext('2d'),
    rect = {},
    drag = false;
}
    

function init() {
    if (canvas != null) {
        canvas.addEventListener('mousedown', mouseDown, false);
        canvas.addEventListener('mouseup', mouseUp, false);
        canvas.addEventListener('mousemove', mouseMove, false);
    } 
}

function mouseDown(e) {
  rect.startX = e.pageX - this.offsetLeft;
  rect.startY = e.pageY - this.offsetTop;
  drag = true;
}

function mouseUp() {
  drag = false;
    //ctx.clearRect(0,0,canvas.width,canvas.height);
    console.log(canvas.width, canvas.height);
    console.log("inicial X: " + rect.startX);
    console.log("inicial Y: " + rect.startY);
    console.log("rect Width: " + rect.w);
    console.log("rect Height: " + rect.h);
    var initX = rect.startX
    var initY = rect.startY
    var areaWidth = rect.w
    var areaHeight = rect.h
    $.ajax({
        type: "POST",
        url: "/getROI",
        data: {
            'initX': initX,
            'initY': initY,
            'areaWidth': areaWidth,
            'areaHeight': areaHeight,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        dataType: 'json',
        success: function (data) {
        }
    });
}
function mouseMove(e) {
  if (drag) {
    rect.w = (e.pageX - this.offsetLeft) - rect.startX;
    rect.h = (e.pageY - this.offsetTop) - rect.startY ;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    draw();
  }
}

function draw() {
    ctx.setLineDash([6]);
  ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
}

function editClicked(nickname, code_number) {
    document.getElementById("apelido").value = nickname;
    var codigo = document.getElementById("codigo");
    codigo.disabled = true;
    codigo.value = code_number;
    document.getElementById('alterar').disabled = false;
    document.getElementById('salvar').disabled = true;
}

function alterarAniaml(event) {
    event.preventDefault();
    var apelido = document.getElementById('apelido').value;
    var codigo = document.getElementById('codigo').value;
    $.ajax({
        type: "POST",
        url: "/updateAnimal",
        data: {
            'nickname': apelido,
            'code_number': codigo,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        dataType: 'json',
        success: function (data) {
            
        }
    });
    console.log("Reload data!!!");
    location.reload(true);
}

init();