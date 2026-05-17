from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():

    return '''

<!DOCTYPE html>
<html>

<head>

<title>Password Strength Analyzer</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial;
}

body{

    background:#0f172a;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    color:white;

}

.container{

    width:500px;
    background:#111827;
    padding:35px;
    border-radius:20px;
    box-shadow:0px 0px 30px rgba(59,130,246,0.25);

}

h1{

    text-align:center;
    color:#60a5fa;
    margin-bottom:10px;

}

.subtitle{

    text-align:center;
    color:#94a3b8;
    margin-bottom:30px;

}

.input-box{

    position:relative;

}

input{

    width:100%;
    padding:15px;
    border:none;
    border-radius:12px;
    background:#1e293b;
    color:white;
    font-size:16px;
    outline:none;
    border:1px solid #334155;

}

.toggle{

    position:absolute;
    right:15px;
    top:15px;
    cursor:pointer;

}

button{

    width:100%;
    padding:15px;
    margin-top:20px;
    border:none;
    border-radius:12px;
    background:#2563eb;
    color:white;
    font-size:16px;
    font-weight:bold;
    cursor:pointer;

}

button:hover{

    background:#1d4ed8;

}

.result{

    margin-top:30px;
    display:none;

}

.meter{

    width:100%;
    height:22px;
    background:#1e293b;
    border-radius:20px;
    overflow:hidden;

}

.fill{

    height:100%;
    width:0%;
    transition:0.5s;

}

#strength{

    text-align:center;
    margin-top:15px;
    font-size:24px;
    font-weight:bold;

}

.suggestions{

    margin-top:25px;

}

.suggestions p{

    background:#1e293b;
    padding:12px;
    border-radius:10px;
    margin-top:10px;

}

.better{

    margin-top:25px;
    background:#1e293b;
    padding:18px;
    border-radius:12px;

}

.better h3{

    color:#60a5fa;
    margin-bottom:10px;

}

#betterPassword{

    color:#22c55e;
    font-size:18px;
    font-weight:bold;

}

</style>

</head>

<body>

<div class="container">

    <h1>Password Strength Analyzer</h1>

    <p class="subtitle">
        Check your password security instantly
    </p>

    <div class="input-box">

        <input 
            type="password"
            id="password"
            placeholder="Enter Password"
        >

        <span class="toggle" onclick="togglePassword()">
            👁
        </span>

    </div>

    <button onclick="analyzePassword()">
        Analyze Password
    </button>

    <div class="result" id="resultBox">

        <div class="meter">

            <div class="fill" id="fill"></div>

        </div>

        <div id="strength"></div>

        <div class="suggestions" id="suggestions"></div>

        <div class="better">

            <h3>Suggested Better Password</h3>

            <div id="betterPassword"></div>

        </div>

    </div>

</div>

<script>

function togglePassword(){

    let password = document.getElementById("password");

    if(password.type === "password"){
        password.type = "text";
    }
    else{
        password.type = "password";
    }

}

async function analyzePassword(){

    let password = document.getElementById("password").value;

    let response = await fetch("/analyze",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            password:password
        })

    });

    let data = await response.json();

    document.getElementById("resultBox").style.display = "block";

    let fill = document.getElementById("fill");

    fill.style.width = data.width + "%";
    fill.style.background = data.color;

    let strength = document.getElementById("strength");

    strength.innerHTML = data.strength;
    strength.style.color = data.color;

    let suggestions = document.getElementById("suggestions");

    suggestions.innerHTML = "";

    if(data.feedback.length == 0){

        suggestions.innerHTML =
        "<p>Excellent Password Security</p>";

    }
    else{

        data.feedback.forEach(item => {

            suggestions.innerHTML +=
            `<p>${item}</p>`;

        });

    }

    document.getElementById("betterPassword").innerHTML =
    data.better_password;

}

</script>

</body>

</html>

'''

@app.route('/analyze', methods=['POST'])
def analyze():

    data = request.get_json()

    password = data['password']

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add numbers.")

    special = "!@#$%^&*"

    if any(char in special for char in password):
        score += 1
    else:
        feedback.append("Add special characters.")

    if score <= 2:
        strength = "Weak"
        color = "#ef4444"

    elif score <= 4:
        strength = "Medium"
        color = "#f59e0b"

    else:
        strength = "Strong"
        color = "#22c55e"

    width = score * 20

    better_password = (
        password.capitalize() +
        "@469#"
    )

    return jsonify({

        "strength":strength,
        "color":color,
        "width":width,
        "feedback":feedback,
        "better_password":better_password

    })

if __name__ == '__main__':
    app.run(debug=True)