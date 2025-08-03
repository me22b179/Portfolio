import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import re
import os
import smtplib
from email.message import EmailMessage

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
    "https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap"
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
            }
            html { scroll-behavior: smooth; }
            .custom-card {
                box-shadow: 0 8px 24px rgba(0,0,0,0.10);
                border-radius: 18px;
                background: #f5f5dc;
                border: 1px solid #a0522d;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .custom-card:hover {
                transform: translateY(-8px) scale(1.03);
                box-shadow: 0 16px 32px rgba(64,0,0,0.15);
                border-color: #800000;
            }
            .project-card:hover {
                transform: scale(1.05);
                box-shadow: 0 12px 24px rgba(64,0,0,0.18);
                cursor: pointer;
            }
            .navbar-brand {
                font-size: 2rem !important;
                letter-spacing: 2px;
                color: #f5f5dc !important;
            }
            .nav-link {
                font-size: 1.1rem !important;
                margin-right: 10px;
                color: #f5f5dc !important;
            }
            .profile-img {
                border: 4px solid #800000;
                box-shadow: 0 4px 16px rgba(128,0,0,0.2);
            }
            .footer-link:hover {
                color: #a0522d !important;
            }
            .btn-custom {
                background: linear-gradient(90deg, #800000 0%, #a0522d 100%);
                color: #f5f5dc;
                border: none;
                font-weight: bold;
                border-radius: 25px;
                padding: 0.75rem 2rem;
                box-shadow: 0 2px 8px rgba(128,0,0,0.12);
            }
            .btn-custom:hover {
                background: linear-gradient(90deg, #a0522d 0%, #800000 100%);
                color: #f5f5dc;
            }
            .scroll-top-btn {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 999;
                background: #800000;
                color: #f5f5dc;
                border: none;
                border-radius: 50%;
                width: 48px;
                height: 48px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12);
                font-size: 1.5rem;
                display: none;
                align-items: center;
                justify-content: center;
            }
            .scroll-top-btn.show {
                display: flex;
            }
        </style>
        <script>
            window.onscroll = function() {
                var btn = document.getElementById('scroll-top-btn');
                if (btn) {
                    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
                        btn.classList.add('show');
                    } else {
                        btn.classList.remove('show');
                    }
                }
            };
            function scrollToTop() {
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        </script>
    </head>
    <body>
        {%app_entry%}
        <button id="scroll-top-btn" class="scroll-top-btn" onclick="scrollToTop()">
            <i class="fas fa-arrow-up"></i>
        </button>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

page_bg = {
    "home": "linear-gradient(135deg, #111 0%, #444 100%)",
    "about": "linear-gradient(135deg, #800000 0%, #a0522d 100%)",
    "projects": "linear-gradient(135deg, #a0522d 0%, #f5f5dc 100%)",
    "contact": "#f5f5dc"
}

navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("", href="/", style={"fontWeight": "bold"}),
        dbc.Nav([
            dbc.NavLink("Home", href="/"),
            dbc.NavLink("About", href="/about"),
            dbc.NavLink("Projects", href="/projects"),
            dbc.NavLink("Contact", href="/contact"),
        ], navbar=True),
    ]),
    color="dark",
    dark=True,
    fixed="top",
    style={"boxShadow": "0 4px 16px rgba(0,0,0,0.18)", "background": "#222"}
)

home_layout = html.Section(
    className="py-5",
    style={"background": page_bg["home"], "minHeight": "100vh"},
    children=[
        dbc.Container([
            html.Div([
                html.Img(
                    src="/assets/profile.jpg",
                    className="profile-img",
                    style={
                        "width": "200px",
                        "height": "200px",
                        "borderRadius": "50%",
                        "marginBottom": "20px"
                    }
                ),
                html.H1("Purva Pratapwar", className="text-center mb-3", style={
                    "color": "#f5f5dc",
                    "fontWeight": "bold",
                    "textShadow": "2px 2px #800000"
                }),
                html.P("Hey all, welcome to my portfolio!!", className="text-center lead", style={
                    "fontSize": "1.3rem",
                    "color": "#f5f5dc"
                }),
                html.P(
                    "I am a B.Tech Mechanical Engineering student at IIT Madras (Batch of 2026), passionate about technology. I love building intuitive solutions—whether it's a dashboard, app, or automation script. I have field of software development and have worked on various projects that showcase my skills in Python, web development, and data analysis. I also have completed an internship in software development role at Bank of New York",
                    className="text-center",
                    style={"color": "#ccc"}
                ),
            ], className="d-flex flex-column align-items-center")
        ], style={
            "marginTop": "5.5rem",
            "borderRadius": "1rem",
            "padding": "2rem"
        })
    ]
)

about_layout = html.Section(
    className="py-5",
    style={"background": page_bg["about"], "minHeight": "100vh"},
    children=[
        dbc.Container([
            html.H2("About Me", className="text-center mb-4", style={"color": "#f5f5dc", "fontWeight": "bold"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H3("Skills", style={"color": "#800000"})),
                        dbc.CardBody([
                            dbc.ListGroup([
                                dbc.ListGroupItem([html.I(className="fab fa-html5 me-2 text-danger"), "HTML"], className="bg-transparent text-dark"),
                                dbc.ListGroupItem([html.I(className="fab fa-css3-alt me-2 text-primary"), "CSS"], className="bg-transparent text-dark"),
                                dbc.ListGroupItem([html.I(className="fab fa-python me-2 text-info"), "Python"], className="bg-transparent text-dark"),
                                dbc.ListGroupItem([html.I(className="fas fa-cogs me-2 text-warning"), "Data Structures and Algorithms"], className="bg-transparent text-dark"),
                                dbc.ListGroupItem(["🐧 Linux OS"], className="bg-transparent text-dark")
                            ])
                        ])
                    ], className="custom-card")
                ], md=6, lg=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Resume", style={"color": "#800000"})),
                        dbc.CardBody([
                            html.P("I am looking forward to have more professional experiences.", style={"color": "#a0522d"}),
                            html.P("Here's my resume !!", style={"color": "#a0522d"}),
                            dbc.Button("Download My Resume", id="resume-download-btn", className="btn-custom"),
                            dcc.Download(id="resume-download"),
                        ])
                    ], className="custom-card mb-3"),
                    dbc.Card([
                        dbc.CardHeader(html.H4("Tools & Softwares (Technical)", style={"color": "#800000"})),
                        dbc.CardBody([
                            html.Ul([
                                html.Li("Git, GitHub"),
                                html.Li("Latex, Excel"),
                                html.Li("PowerPoint, AutoCAD"),
                                html.Li("MS Word, VScode")
                            ], style={"color": "#a0522d"})
                        ])
                    ], className="custom-card mb-3"),
                    dbc.Card([
                        dbc.CardHeader(html.H4("Tools & Softwares (Design)", style={"color": "#800000"})),
                        dbc.CardBody([
                            html.Ul([
                                html.Li("Canva Pro, Figma"),
                                html.Li("Illustrator, Photoshop"),
                                html.Li("MS Clipchamp")
                            ], style={"color": "#a0522d"})
                        ])
                    ], className="custom-card")
                ], md=6, lg=8),
            ])
        ], style={"marginTop": "5.5rem"})
    ]
)

projects_layout = html.Section(
    className="py-5",
    style={"background": page_bg["projects"], "minHeight": "100vh"},
    children=[
        dbc.Container([
            html.H2("Projects", className="text-center mb-4", style={"color": "#800000", "fontWeight": "bold"}),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardImg(src="https://picsum.photos/300/200?random=5", top=True, style={"borderRadius": "18px 18px 0 0"}),
                    dbc.CardBody([
                        html.I(className="fas fa-laptop-code fa-2x text-primary mb-2"),
                        html.H4("Portfolio", style={"color": "#800000"}),
                        html.P("Designed a responsive collapsible personal portfolio website", style={"color": "#a0522d"})
                    ])
                ], className="custom-card project-card"), md=6, lg=3),
                dbc.Col(dbc.Card([
                    dbc.CardImg(src="https://picsum.photos/300/200?random=6", top=True, style={"borderRadius": "18px 18px 0 0"}),
                    dbc.CardBody([
                        html.I(className="fas fa-pencil-alt fa-2x text-success mb-2"),
                        html.H4("Ball Screw Drive System", style={"color": "#800000"}),
                        html.P("Ball Screw Drive System (Course Project)", style={"color": "#a0522d"})
                    ])
                ], className="custom-card project-card"), md=6, lg=3),
                dbc.Col(dbc.Card([
                    dbc.CardImg(src="https://picsum.photos/300/200?random=7", top=True, style={"borderRadius": "18px 18px 0 0"}),
                    dbc.CardBody([
                        html.I(className="fas fa-gamepad fa-2x text-success mb-2"),
                        html.H4("Game", style={"color": "#800000"}),
                        html.P("User-friendly TicTacToe Game", style={"color": "#a0522d"})
                    ])
                ], className="custom-card project-card"), md=6, lg=3),
                dbc.Col(dbc.Card([
                    dbc.CardImg(src="https://picsum.photos/300/200?random=8", top=True, style={"borderRadius": "18px 18px 0 0"}),
                    dbc.CardBody([
                        html.I(className="fas fa-bars fa-2x text-success mb-2"),
                        html.H4("Cash Flow Minimizer", style={"color": "#800000"}),
                        html.P("Cash Flow Minimizer Project", style={"color": "#a0522d"})
                    ])
                ], className="custom-card project-card"), md=6, lg=3),
            ], className="gy-4")
        ], style={"marginTop": "5.5rem"})
    ]
)

contact_layout = html.Section(
    className="py-5",
    style={"background": page_bg["contact"], "minHeight": "100vh"},
    children=[
        dbc.Container([
            html.H2("Contact Me", className="text-center mb-4", style={"color": "#800000", "fontWeight": "bold"}),
            dbc.Form([
                dbc.Row([dbc.Col([
                    dbc.Label("Name", className="text-dark"),
                    dbc.Input(type="text", id="contact-name", placeholder="Your Name", style={"borderRadius": "12px"})
                ])], className="mb-3"),
                dbc.Row([dbc.Col([
                    dbc.Label("Email", className="text-dark"),
                    dbc.Input(type="email", id="contact-email", placeholder="Your Email", style={"borderRadius": "12px"})
                ])], className="mb-3"),
                dbc.Row([dbc.Col([
                    dbc.Label("Message", className="text-dark"),
                    dbc.Textarea(id="contact-message", placeholder="Your Message", style={"borderRadius": "12px"})
                ])], className="mb-3"),
                dbc.Button("Send Message", id="send-message-btn", color="info", className="btn-custom mt-3"),
                html.Div(id="contact-response", className="mt-3")
            ], style={"background": "rgba(255,255,255,0.7)", "padding": "2rem", "borderRadius": "18px", "boxShadow": "0 4px 16px rgba(0,0,0,0.08)"})
        ], style={"marginTop": "5.5rem"})
    ]
)

footer = html.Footer(
    className="py-2 text-center footer",
    style={"background": "#222"},
    children=[
        dbc.Container([
            html.Div([
                html.I(className="fas fa-envelope me-2"),
                html.A("pratapwarpurva@gmail.com", href="mailto:pratapwarpurva@gmail.com", className="text-light footer-link")
            ]),
            html.Div([
                html.A(html.I(className="fab fa-instagram fa-2x mx-2"), href="https://www.instagram.com/purva_p_1109/", className="text-light footer-link"),
                html.A(html.I(className="fab fa-linkedin fa-2x mx-2"), href="https://www.linkedin.com/in/purva-pratapwar-8a6362263", className="text-light footer-link"),
                html.A(html.I(className="fab fa-github fa-2x mx-2"), href="https://github.com/me22b179", className="text-light footer-link")
            ], className="mt-2")
        ])
    ]
)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content"),
    footer
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/about":
        return about_layout
    elif pathname == "/projects":
        return projects_layout
    elif pathname == "/contact":
        return contact_layout
    else:
        return home_layout

@app.callback(
    Output("resume-download", "data"),
    Input("resume-download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_resume(n_clicks):
    if n_clicks:
        return dcc.send_file("assets/F2_Resume.pdf")
    return dash.no_update

def send_email(name, email, message):
    try:
        sender_email = os.environ.get("SENDER_EMAIL")
        sender_password = os.environ.get("SENDER_PASSWORD")
        recipient_email = email

        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        msg["Subject"] = "Portfolio Contact Form Submission"
        msg["From"] = sender_email
        msg["To"] = recipient_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

@app.callback(
    [
        Output("contact-response", "children"),
        Output("contact-name", "value"),
        Output("contact-email", "value"),
        Output("contact-message", "value"),
    ],
    Input("send-message-btn", "n_clicks"),
    State("contact-name", "value"),
    State("contact-email", "value"),
    State("contact-message", "value"),
    prevent_initial_call=True
)
def handle_contact(n_clicks, name, email, message):
    if n_clicks:
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return (
                dbc.Alert("Please enter a valid email address.", color="danger"),
                name, email, message
            )
        success, info = send_email(name, email, message)
        if success:
            return (
                dbc.Alert("Thank you for reaching out! An email has been sent to you.", color="success"),
                "", "", ""
            )
        else:
            return (
                dbc.Alert(info, color="danger"),
                name, email, message
            )
    return "", dash.no_update, dash.no_update, dash.no_update

if __name__ == "__main__":
    app.run(debug=True)