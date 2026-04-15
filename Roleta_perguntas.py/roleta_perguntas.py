import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Roleta Profissional", page_icon="🎡")

st.title("🎡 Roleta de Perguntas")

# Estado
if "perguntas" not in st.session_state:
    st.session_state.perguntas = []

# Input
nova = st.text_input("Digite uma pergunta")

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Adicionar"):
        if nova.strip():
            st.session_state.perguntas.append(nova)

with col2:
    if st.button("🗑️ Limpar"):
        st.session_state.perguntas = []

st.subheader("📋 Lista")
st.write(st.session_state.perguntas)

# Só mostra se tiver perguntas
if st.session_state.perguntas:

    perguntas_json = json.dumps(st.session_state.perguntas)

    components.html(f"""
    <html>
    <body style="text-align:center; font-family:sans-serif;">

    <h3>Gire a roleta</h3>

    <!-- SETA -->
    <div style="
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-bottom: 30px solid red;
        margin: auto;
    "></div>

    <canvas id="roleta" width="400" height="400"></canvas>

    <br><br>
    <button onclick="girar()" style="
        padding:10px 20px;
        font-size:16px;
        border:none;
        background:#111;
        color:white;
        border-radius:8px;
        cursor:pointer;
    ">
        Girar 🎡
    </button>

    <p id="resultado" style="font-size:14px; font-weight:bold; margin-top:20px;"></p>

    <script>
    let perguntas = {perguntas_json};
    let canvas = document.getElementById("roleta");
    let ctx = canvas.getContext("2d");

    let anguloAtual = 0;

    function desenhar() {{
        let total = perguntas.length;
        let anguloSetor = 2 * Math.PI / total;

        for (let i = 0; i < total; i++) {{
            ctx.beginPath();
            ctx.moveTo(200,200);
            ctx.arc(200,200,200, i*anguloSetor, (i+1)*anguloSetor);
            
            ctx.fillStyle = i % 2 === 0 ? "#6C5CE7" : "#00CEC9";
            ctx.fill();

            ctx.save();
            ctx.translate(200,200);
            ctx.rotate(i*anguloSetor + anguloSetor/2);

            ctx.fillStyle = "white";
            ctx.font = "12px Arial";
            ctx.textAlign = "right";

            ctx.fillText(perguntas[i], 180, 5);
            ctx.restore();
        }}
    }}

    function easeOut(t) {{
        return 1 - Math.pow(1 - t, 3);
    }}

    function girar() {{
        let total = perguntas.length;
        let anguloSetor = 2 * Math.PI / total;

        let giroFinal = Math.random() * 360 + 1440; // várias voltas
        let duracao = 4000;

        let inicio = null;

        function animar(timestamp) {{
            if (!inicio) inicio = timestamp;
            let progresso = timestamp - inicio;
            let t = Math.min(progresso / duracao, 1);

            let ease = easeOut(t);

            let angulo = (giroFinal * ease) * Math.PI / 180;

            ctx.clearRect(0,0,400,400);

            ctx.save();
            ctx.translate(200,200);
            ctx.rotate(angulo);
            ctx.translate(-200,-200);

            desenhar();

            ctx.restore();

            if (t < 1) {{
                requestAnimationFrame(animar);
            }} else {{
                let graus = giroFinal % 360;
                let setor = Math.floor((360 - graus) / (360 / total)) % total;

                document.getElementById("resultado").innerText =
                    "🎯 " + perguntas[setor];
            }}
        }}

        requestAnimationFrame(animar);
    }}

    desenhar();

    </script>

    </body>
    </html>
    """, height=600)